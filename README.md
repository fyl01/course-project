# course-project
cyberspace security practice of innovation and entrepreneurship course
## Project 1：implement the Rho method of reduced SM3
#### 利用Pollard Rho算法实现了第二原象攻击，即对于指定的字符串，找到与之哈希相同的字符串。最终，在可接受的时间里，实现了$32$比特的第二原象攻击。   
**Environment:** Ubuntu 20.04  
**Testing Result：**
| Collision bit | Running time |
|---|---|
| 8 bits | 0.000536 seconds |
| 16 bits | 0.110520 seconds |
| 24 bits | $\approx$ 10 seconds |
| 32 bits | $\approx$ 5 hours |

<font size="1">The above data vary greatly with the change of the initial value.</font><br />  
- [Pollardrho.py](https://github.com/fyl01/course-project/blob/main/the%20Rho%20method%20of%20reduced%20SM3/Pollardrho.py): 利用rho思想实现的整数分解，与破解SM3无关。
- [Rho_for_SM3.c](https://github.com/fyl01/course-project/blob/main/the%20Rho%20method%20of%20reduced%20SM3/Rho_for_SM3.c): 利用rho思想实现了reduced SM3的碰撞。  

已编写Makefile文件，以下是几个指令    
```shell
$ make
$ ./test
$ make clean
```
test文件已上传（32bit碰撞），可直接./test运行程序。
可得到产生碰撞的两个字符串（转化为16进制形式）和找到此次碰撞所需的时间。

## Project 2: naïve birthday attack of reduced SM3  
#### 利用朴素算法对SM3进行碰撞攻击，直接寻找两个哈希相同的字符串，因为攻击难度远小于Project 1，所以实现效果好，在可接受的时间里实现了$48$比特的碰撞攻击。  
**Environment:** Pycharm 4.5.3 Python 3.9  
**Testing Result：**
| Collision bit | Running time |
|---|---|
| 8 bits | 0.006836 seconds |
| 16 bits | 0.057584 seconds |
| 24 bits | $\approx$ 4.33 seconds |
| 32 bits | $\approx$ 30 seconds |
| 36 bits | $\approx$ 85 seconds |
| 40 bits | $\approx$ 26 minutes |
| 48 bits | $\approx$ 1.6 hours |

## Project 3: length extension attack for SM3 
### Introduction
### 哈希长度扩展攻击(Hash Length Extension Attacks)

当知道hash(message)的值及message长度的情况下，可以推算出hash(message||padding||m’)。在这里m’是任意数据，||是连接符，可以为空,padding是message后的填充字节。hash的padding字节包含整个消息的长度，因此，为了能准确计算出padding的值，message的长度我们也是需要知道的。
当我们填充后，服务器算出的原始hash值，正好与我们添加扩展字符串并覆盖初始链变量所计算出来的一样。

### SM3算法过程

官方文档 [SM3密码杂凑算法](https://www.oscca.gov.cn/sca/xxgk/2010-12/17/1002389/files/302a3ada057c4a73830536d03e683110.pdf)

#### 消息填充

SM3的消息扩展步骤是以512位的数据分组作为输入的。因此，我们需要在一开始就把数据长度填充至512位的倍数。数据填充规则和MD5一样，具体步骤如下：

1. 先填充一个“1”，后面加上k个“0”。其中k是满足(n+1+k) mod 512 = 448的最小正整数。

1. 追加64位的数据长度（bit为单位，大端序存放。观察算法标准原文附录A运算示例可以推知。）

填充完的数据大概长这样：  

<img src="https://pic3.zhimg.com/v2-366d5284c75a6ac92fdbc12ce5b45a2a_r.jpg" style="zoom:60%;" />

#### 迭代过程

将填充后的消息m′按512比特进行分组：$m′= B^{(0)}B^{(1)} ···B^{(n−1)}$
其中$ n=(l+k+65)/512 $
对m′按下列方式迭代：

```python
FOR i=0 TO n-1
$$V^{(i+1)} = CF(V^{(i)}, B^{(i)})$$
END FOR
```

其中CF是压缩函数，$V^{(0)}$为256比特初始值IV，$B^{(i)}$为填充后的消息分组，迭代压缩的结果为$V ^{(n)}$

#### 消息扩展

SM3的迭代压缩步骤没有直接使用数据分组进行运算，而是使用这个步骤产生的132个消息字。（一个消息字的长度为32位）概括来说，先将一个512位数据分组划分为16个消息字，并且作为生成的132个消息字的前16个。再**用这16个消息字递推生成剩余的116个消息字**。

在最终得到的132个消息字中，前68个消息字构成数列 ![[公式]](https://www.zhihu.com/equation?tex=%5C%7B+W_%7Bj%7D+%5C%7D) ，后64个消息字构成数列 ![[公式]](https://www.zhihu.com/equation?tex=%5C%7B+W%5E%7B%27%7D_%7Bj%7D+%5C%7D) ，其中下标j从0开始计数。

#### 压缩函数

令A,B,C,D,E,F,G,H为字寄存器,SS1,SS2,TT1,TT2为中间变量,压缩函数$V^{i+1} = CF (V^{(i)}, B^{(i)


### Attack Step  
1.	随机生成一个消息(secret)，用SM3函数算出hash值(hash1)
2.	生成一个附加消息(m')。首先用hash1推算出这一次加密结束后8个向量的值，再以它们作为初始向量，去加密m’，得到另一个hash值(hash2)
3.	计算secret + padding + m'的hash值(hash3)，如果攻击成功，hash2应该和hash3相等  

可执行文件已上传，输入以下指令，即可得到攻击过程和结果  
```shell
$ ./sm3
```
