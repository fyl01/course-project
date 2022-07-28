#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include <string>
//
// NOTE(casey): Step 1 - include the meow_hash header for your platform
//

#include "meow_invertibility_aesni.h"

//
// NOTE(casey): Step 2 - use the Meow hash in a variety of ways!
//
// Example functions below:
//   PrintHash - how to print a Meow hash to stdout, from highest-order 32-bits to lowest
//   HashTestBuffer - how to have Meow hash a buffer of data
//   HashOneFile - have Meow hash the contents of a file
//   CompareTwoFiles - have Meow hash the contents of two files, and check for equivalence
//

static void
PrintHash(meow_u128 Hash)
{
	printf("    %08X-%08X-%08X-%08X\n",
		MeowU32From(Hash, 3),
		MeowU32From(Hash, 2),
		MeowU32From(Hash, 1),
		MeowU32From(Hash, 0));
}

static void
HashTestBuffer(void)
{
	// NOTE(casey): Make a buffer with repeating numbers.
	int Size = 16000;
	char* Buffer = (char*)malloc(Size);
	for (int Index = 0;
		Index < Size;
		++Index)
	{
		Buffer[Index] = (char)Index;
	}

	// NOTE(casey): Ask Meow for the hash
	meow_u128 Hash = MeowHash(MeowDefaultSeed, Size, Buffer);

	// NOTE(casey): Extract example smaller hash sizes you might want:
	long long unsigned Hash64 = MeowU64From(Hash, 0);
	int unsigned Hash32 = MeowU32From(Hash, 0);

	// NOTE(casey): Print the hash
	printf("  Hash of a test buffer:\n");
	PrintHash(Hash);

	free(Buffer);
}

//
// NOTE(casey): That's it!  Everything else below here is just boilerplate for starting up
// and loading files with the C runtime library.
//

int main(int ArgCount, char** Args)
{
	const char* message = "Fu Yulin 201900460014";
	const char* hashvalue = "sdu_cst_20220610";   // hex:7364755f6373745f3230323230363130
	static meow_u8 hashvalue_padding[128] =          // 随意按一种方式填充至128字节（此处直接将defaultseed的前16字节替换为真正的hash值）
	{
		0x73, 0x64, 0x75, 0x5F, 0x63, 0x73, 0x74, 0x5f,
		0x32, 0x30, 0x32, 0x32, 0x30, 0x36, 0x31, 0x30,
		0x4A, 0x40, 0x93, 0x82, 0x22, 0x99, 0xF3, 0x1D,
		0x00, 0x82, 0xEF, 0xA9, 0x8E, 0xC4, 0xE6, 0xC8,
		0x94, 0x52, 0x82, 0x1E, 0x63, 0x8D, 0x01, 0x37,
		0x7B, 0xE5, 0x46, 0x6C, 0xF3, 0x4E, 0x90, 0xC6,
		0xCC, 0x0A, 0xC2, 0x9B, 0x7C, 0x97, 0xC5, 0x0D,
		0xD3, 0xF8, 0x4D, 0x5B, 0x5B, 0x54, 0x70, 0x91,
		0x79, 0x21, 0x6D, 0x5D, 0x98, 0x97, 0x9F, 0xB1,
		0xBD, 0x13, 0x10, 0xBA, 0x69, 0x8D, 0xFB, 0x5A,
		0xC2, 0xFF, 0xD7, 0x2D, 0xBD, 0x01, 0xAD, 0xFB,
		0x7B, 0x8E, 0x1A, 0xFE, 0xD6, 0xA2, 0x67, 0xE9,
		0x6B, 0xA7, 0xC9, 0x04, 0x5F, 0x12, 0xC7, 0xF9,
		0x92, 0x4A, 0x19, 0x94, 0x7B, 0x39, 0x16, 0xCF,
		0x70, 0x80, 0x1F, 0x2E, 0x28, 0x58, 0xEF, 0xC1,
		0x66, 0x36, 0x92, 0x0D, 0x87, 0x15, 0x74, 0xE6
	};
	printf("Given message: %s\n", message);
	printf("    hashvalue: %s\n", hashvalue);
	printf("\nUsing invertibility, computing the key:\n");
	meow_umm len = strlen(message);
	meow_inv(message, len, hashvalue_padding);

	return 0;
}