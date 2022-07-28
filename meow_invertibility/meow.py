import struct


meow_default_seed = bytes.fromhex(
    "3243f6a8885a308d313198a2e03707344a4093822299f31d0082efa98ec4e6c8"
    "9452821e638d01377be5466cf34e90c6cc0ac29b7c97c50dd3f84d5b5b547091"
    "79216d5d98979fb1bd1310ba698dfb5ac2ffd72dbd01adfb7b8e1afed6a267e9"
    "6ba7c9045f12c7f9924a19947b3916cf70801f2e2858efc16636920d871574e6"
)

aes_sbox_inverse = list(bytes.fromhex(
    "52096ad53036a538bf40a39e81f3d7fb7ce339829b2fff87348e4344c4dee9cb"
    "547b9432a6c2233dee4c950b42fac34e082ea16628d924b2765ba2496d8bd125"
    "72f8f66486689816d4a45ccc5d65b6926c704850fdedb9da5e154657a78d9d84"
    "90d8ab008cbcd30af7e45805b8b34506d02c1e8fca3f0f02c1afbd0301138a6b"
    "3a9111414f67dcea97f2cfcef0b4e67396ac7422e7ad3585e2f937e81c75df6e"
    "47f11a711d29c5896fb7620eaa18be1bfc563e4bc6d279209adbc0fe78cd5af4"
    "1fdda8338807c731b11210592780ec5f60517fa919b54a0d2de57a9f93c99cef"
    "a0e03b4dae2af5b0c8ebbb3c83539961172b047eba77d626e169146355210c7d"
))

def gf_multiply(a: int, b: int) -> int:
    r = 0
    for i, bit in enumerate(bin(b)[-1:1:-1]):
        r ^= int(bit) * (a << i)
    while r.bit_length() > 8:
        r ^= 0x11b << (r.bit_length() - 9)
    return r

gf_table = {(a, b): gf_multiply(a, b) for a in (9, 11, 13, 14) for b in range(256)}

def inverse_mix_column(col: bytearray):
    a, b, c, d = col
    return (
        gf_table[14, a] ^ gf_table[11, b] ^ gf_table[13, c] ^ gf_table[ 9, d],
        gf_table[ 9, a] ^ gf_table[14, b] ^ gf_table[11, c] ^ gf_table[13, d],
        gf_table[13, a] ^ gf_table[ 9, b] ^ gf_table[14, c] ^ gf_table[11, d],
        gf_table[11, a] ^ gf_table[13, b] ^ gf_table[ 9, c] ^ gf_table[14, d],
    )

def aesdec(a: bytearray, b: bytearray):
    # Inverse shift rows.
    for row_index in range(4):
        row = a[row_index::4]
        for _ in range(row_index):
            row = row[-1:] + row[:-1]
        a[row_index::4] = row
    # Inverse sbox.
    for i in range(16):
        a[i] = aes_sbox_inverse[a[i]]
    # Inverse mix columns.
    for column_index in range(4):
        a[column_index*4 : column_index*4 + 4] = \
            inverse_mix_column(a[column_index*4 : column_index*4 + 4])
    # Xor round key.
    for i in range(16):
        a[i] ^= b[i]

def paddq(a: bytearray, b: bytearray):
    mask64 = 2**64 - 1
    a0, a1 = struct.unpack("<QQ", a)
    b0, b1 = struct.unpack("<QQ", b)
    a[:] = struct.pack("<QQ", (a0 + b0) & mask64, (a1 + b1) & mask64)

def pxor(a: bytearray, b: bytearray):
    for i in range(16):
        a[i] ^= b[i]

def meow_hash(key_bytes: bytes, input_bytes: bytes) -> bytes:
    assert len(key_bytes) == 128
    lanes = [
        bytearray(key_bytes[i*16 : i*16 + 16])
        for i in range(8)
    ]
    get_lane = lambda i: lanes[i % 8]
    # print("get_lane",get_lane(0))
    def meow_mix_reg(i, reads):
        aesdec(get_lane(i + 0), get_lane(i + 4))
        paddq (get_lane(i + 6), reads[0])
        pxor  (get_lane(i + 4), reads[1])
        aesdec(get_lane(i + 4), get_lane(i + 1))
        paddq (get_lane(i + 2), reads[2])
        pxor  (get_lane(i + 1), reads[3])

    def meow_mix(i, block):
        meow_mix_reg(i, [
            block[offset : offset + 16] for offset in (15, 0, 1, 16)
        ])

    def meow_mix_funky(i, block):
        meow_mix_reg(i, (
            b"\0" + block[:15], block[:16], block[17:] + block[:1], block[16:],
        ))

    def meow_shuffle(i):
        aesdec(get_lane(i + 0), get_lane(i + 4))
        paddq (get_lane(i + 1), get_lane(i + 5))
        pxor  (get_lane(i + 4), get_lane(i + 6))
        aesdec(get_lane(i + 4), get_lane(i + 1))
        paddq (get_lane(i + 5), get_lane(i + 6))
        pxor  (get_lane(i + 1), get_lane(i + 2))

    # Pad the input to a multiple of 32 bytes; but add a full block of zeros if we're already a multiple.
    original_length = len(input_bytes)
    # print(original_length)
    target_length = ((len(input_bytes) // 32) + 1) * 32
    input_bytes += b"\0" * (target_length - original_length)
    # Cut off the last block, which we will absorb differently.
    input_bytes, tail_block = input_bytes[:-32], input_bytes[-32:]

    # Absorb all complete 256-byte blocks.
    off = 0
    # print(len(tail_block))
    while off + 256 <= len(input_bytes):
        for _ in range(8):
            meow_mix(off // 32, input_bytes[off : off+32])
            off += 32

    # Absorb the tail block and message length in a funky way that's different than all other absorptions.
    meow_mix_funky(0, tail_block)
    message_length_block = struct.pack("<QQQQ", 0, 0, original_length, 0)
    meow_mix_funky(1, message_length_block)

    # Now return to absorbing any remaining 32-byte blocks.
    while off + 32 <= len(input_bytes):
        meow_mix(2 + off // 32, input_bytes[off : off + 32])
        off += 32

    # Finalize.
    for i in range(12):
        meow_shuffle(i)

    # Aggregate the state down into a single lane.
    paddq(lanes[0], lanes[2])
    paddq(lanes[4], lanes[6])
    paddq(lanes[1], lanes[3])
    paddq(lanes[5], lanes[7])
    pxor(lanes[0], lanes[1])
    pxor(lanes[4], lanes[5])
    paddq(lanes[0], lanes[4])

    return lanes[0]


if __name__ == '__main__':
    key = bytes.fromhex(
        "17180fbeaaaf6095c0b5ebd24f9e9fe9a7aac518ff05b230d29b74137467bc4a"
        "a611dfaf465a50c44b0dbf171f6c8242242800c887d20830ff2f96340099f735"
        "8590e7f8db60479d6c92cecad24deeef16d19e9ef67a680782dedbf2766587ba"
        "f1d9572b0117e02d13c23eadc14a0c1f27a4d6fa9fdb5067241d2488c99beff9"
    )
    # print("key",key[0],key[1],key[2],key[3],key[4],key[5],key[6],key[7],key[8],key[9],key[10],key[11],key[12],key[13],key[14],key[15],key[16])
    message = bytes(
        "Arbitrary example input: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed"
        " do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,"
        " quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",'utf-8'
    )
    print(meow_hash(key, message))