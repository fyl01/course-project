# Project 1：implement the Rho method of reduced SM3（实现32 bits第二原象攻击）
## 原理
**第二原像攻击**，即给定消息M1时，攻击者能够找到另一条消息M2,其哈希值与M1的哈希值相同。理论上复杂度为$O(2^n)$  
本实验利用Pollard Rho算法实现了**第二原象攻击**，即对于指定的字符串，找到与之哈希相同的字符串。最终，在可接受的时间里，实现了$32$比特的第二原象攻击。      
Rho攻击（来自Pollard Rho算法），流程如下  
1. 给定具有n比特哈希值的哈希函数，选择一些随机哈希值H1,设H1'=H1
2. 计算H2=Hash(H1),H2'=Hash(Hash(H1'))
3. 迭代该过程并计算Hi+1=Hash(Hi)，Hi+1'=Hash(Hash(Hi'))，直到有一个i可以满足Hi+1=Hi+1'  
对应的示意图如下  
![image](https://github.com/fyl01/course-project/blob/main/the%20Rho%20method%20of%20reduced%20SM3/headImg.png)  

## 代码说明
- [Pollardrho.py](https://github.com/fyl01/course-project/blob/main/the%20Rho%20method%20of%20reduced%20SM3/Pollardrho.py): 利用rho思想实现的整数分解，与破解SM3无关。
- [Rho_for_SM3.c](https://github.com/fyl01/course-project/blob/main/the%20Rho%20method%20of%20reduced%20SM3/Rho_for_SM3.c): 利用rho思想实现了reduced SM3的碰撞。  
在Rho_for_SM3.c中，利用openssl密码库，分别实现了一次SM3哈希函数hash_str()和两次SM3哈希函数hashhash_str()

## 运行指导
**运行环境：** Ubuntu 20.04  
已编写Makefile文件，以下是几个指令    
```shell
$ make
$ ./test
$ make clean
```
test文件已上传（32bit碰撞），可直接./test运行程序，得到产生碰撞的两个字符串（转化为16进制形式）和找到此次碰撞所需的时间。  
也可以修改全局变量HASH_TRUNCATED_LEN来控制寻找碰撞的比特数，HASH_TRUNCATED_LEN*8即为要碰撞的比特数。

## 运行结果
**Testing Result：**
| Collision bit | Running time |
|---|---|
| 8 bits | $\approx$ 0.0002 seconds |
| 16 bits | $\approx$ 0.1 seconds |
| 24 bits | $\approx$ 10 seconds |
| 32 bits | $\approx$ 30 minutes |

<font size="1">The above data vary greatly with the change of the initial value.</font><br />  
8比特运行结果截图
![image](https://github.com/fyl01/course-project/blob/main/the%20Rho%20method%20of%20reduced%20SM3/rhoresult_8.png)
16比特运行结果截图
![image](https://github.com/fyl01/course-project/blob/main/the%20Rho%20method%20of%20reduced%20SM3/rhoresult_16.png)
24比特运行结果截图
![image](https://github.com/fyl01/course-project/blob/main/the%20Rho%20method%20of%20reduced%20SM3/rhoresult_24.png)
32比特运行结果截图
![image](https://github.com/fyl01/course-project/blob/main/the%20Rho%20method%20of%20reduced%20SM3/rhoresult_32.png)
