#include <stdio.h>
#include <string.h>
#include<openssl/evp.h>
#include<string.h>
#include<time.h>

static unsigned int HASH_RESULT_LEN = 32;  //原始hash长度 32*8=256bits
static unsigned int HASH_TRUNCATED_LEN = 32/8;   // 截断后的长度为32bits（原hash结果的前4位）

/**
 * @brief 计算一段数据的哈希值（原始、截断）
 * 
 * @param str 数据
 * @param len 数据长度
 * @param hash_result 哈希值
 * @return unsigned int 原始哈希值长度
 */
unsigned int hash_str(const char* str, const size_t len, unsigned char* hash_result)
{
    unsigned int ret;
    const EVP_MD* alg = EVP_sm3();
    EVP_Digest(str, len, hash_result, &ret, alg, NULL);
    return ret;
}

unsigned int hashhash_str(const char* str, const size_t len, unsigned char* hash_result)
{
    unsigned int ret1, ret2;
    const EVP_MD* alg = EVP_sm3();
    unsigned char middle[HASH_RESULT_LEN];
    EVP_Digest(str, len, (unsigned char*)middle, &ret1, alg, NULL);
    EVP_Digest(middle, ret1, hash_result, &ret2, alg, NULL);
    return ret2;
}

/**
 * @brief 生成随机字符串
 * 
 * @param length 产生字符串的长度
 * @return char* 随机字符串
 */
unsigned char* strRand(int length) 
{
    int tmp;							// tmp: 暂存一个随机数
    char* buffer;						// buffer: 保存返回值
    buffer = (char*)malloc(sizeof(char)*length);        
    
    srand((unsigned)time(NULL));
    for (int i = 0; i < length; i++) {
        tmp = rand() % 62;	// 随机一个小于 62 的整数，0-9、a-z、A-Z 共 62 种字符
        if (tmp < 10) {			// 如果随机数小于 10，变换成一个阿拉伯数字的 ASCII
            tmp += '0';
        } 
        else if(tmp<36){
            tmp -= 10;
            tmp += 'a';
        }
        else {				// 否则，变换成一个大写字母的 ASCII
            tmp -= 36;
            tmp += 'A';
        }
        buffer[i]=tmp;
    }
    return buffer;
}


int main(int argc, char const* argv[])
{
    srand((unsigned)time(NULL));
    int length = rand()%100;
    unsigned char* sr = strRand(length);        // 生成随机字符串sr
/**
 * 符号定义
 * H1 = Hash(sr), H1_ = H1
 * H1 = hash(H1), H1_ = hash(hash(H1_))
 */
    unsigned char H1[HASH_RESULT_LEN];
    hash_str(sr, strlen(sr), H1);      // H1 = Hash(sr)
    unsigned char H1_[HASH_RESULT_LEN];
    strncpy(H1_, H1, HASH_RESULT_LEN);     // H1_ = H1


    hash_str(H1, HASH_RESULT_LEN, H1);     // H1 = hash(H1)
    hashhash_str(H1_, HASH_RESULT_LEN, H1_);     // H1_ = hash(hash(H1_))

    clock_t start = clock();
    unsigned char a[HASH_RESULT_LEN];     // 记录产生碰撞的字符串
    unsigned char b[HASH_RESULT_LEN];
    while(memcmp(H1, H1_, HASH_TRUNCATED_LEN))    // 当相等时，返回值为0  不能用strncmp？？？
    {
        strncpy(a, H1, HASH_RESULT_LEN);
        strncpy(b, H1_, HASH_RESULT_LEN);
        hash_str(H1, HASH_RESULT_LEN, H1);     // H1 = hash(H1)
        hashhash_str(H1_, HASH_RESULT_LEN, H1_);     // H1_ = hash(hash(H1_))
    }
    clock_t end = clock();

    printf("Find the collision!(%d bits)\n",HASH_TRUNCATED_LEN*8);
    /*      print collision      */
    printf("Initial string:%s\n",sr);
    printf("a(in hex) = ");
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", a[i]);
    }
    printf("\n");
    printf("b(in hex) = ");
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", b[i]);
    }
    printf("\nhash(b)(in hex) = ");
    hash_str(b, HASH_RESULT_LEN, b);
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", b[i]);
    }
    printf("\nH1 = hash(a) = ");
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", H1[i]);
    }
    printf("\n");
    printf("H1_ = hash(hash(b)) = ");
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", H1_[i]);
    }

    printf("\nRunning time = %f seconds\n", (double)(end - start) / CLOCKS_PER_SEC);
    return 0;
}
