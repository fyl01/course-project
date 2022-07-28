# course-project
cyberspace security practice of innovation and entrepreneurship course  
**所有项目均个人（傅宇琳 201900460014）完成，以下是项目清单，具体实现原理步骤等见对应文件夹中的README.md文件**  
## Project 1：implement the Rho method of reduced SM3（实现32 bits第二原象攻击）  
**Environment:** Ubuntu 20.04  
**Testing Result：**
| Collision bit | Running time |
|---|---|
| 8 bits | $\approx$ 0.0002 seconds |
| 16 bits | $\approx$ 0.1 seconds |
| 24 bits | $\approx$ 10 seconds |
| 32 bits | $\approx$ 30 minutes |

<font size="1">The above data vary greatly with the change of the initial value.</font><br />  
- [Pollardrho.py](https://github.com/fyl01/course-project/blob/main/the%20Rho%20method%20of%20reduced%20SM3/Pollardrho.py): 利用rho思想实现的整数分解，与破解SM3无关。
- [Rho_for_SM3.c](https://github.com/fyl01/course-project/blob/main/the%20Rho%20method%20of%20reduced%20SM3/Rho_for_SM3.c): 利用rho思想实现了reduced SM3的碰撞。  

## Project 2: naïve birthday attack of reduced SM3（实现48 bits碰撞攻击）  
#### 利用朴素算法对SM3进行碰撞攻击，直接寻找两个哈希相同的字符串，因为攻击难度远小于Project 1，所以实现效果好，在可接受的时间里实现了$48$比特的碰撞攻击。  
**Environment:** Pycharm 4.5.3 Python 3.9  
**Testing Result：**
| Collision bit | Running time |
|---|---|
| 8 bits | $\approx$ 0.005 seconds |
| 16 bits | $\approx$ 0.01 seconds |
| 24 bits | $\approx$ 3 seconds |
| 32 bits | $\approx$ 30 seconds |
| 36 bits | $\approx$ 85 seconds |
| 40 bits | $\approx$ 26 minutes |
| 48 bits | $\approx$ 1.6 hours |

## Project 3: length extension attack for SM3 
### 哈希长度扩展攻击(Hash Length Extension Attacks)
当知道hash(message)的值及message长度的情况下，可以推算出hash(message||padding||m’)。在这里m’是任意数据，||是连接符，可以为空,padding是message后的填充字节。hash的padding字节包含整个消息的长度，因此，为了能准确计算出padding的值，message的长度我们也是需要知道的。
当我们填充后，服务器算出的原始hash值，正好与我们添加扩展字符串并覆盖初始链变量所计算出来的一样。

## Project 4：meow invertibility
利用meow哈希的可逆性，通过哈希值和消息值推算出密钥。
