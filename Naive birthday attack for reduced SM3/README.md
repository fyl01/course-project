# Project 2: naïve birthday attack of reduced SM3（实现48 bits碰撞攻击） 
## 原理
**碰撞攻击**，找到两个任意不同的消息m1和m2，使hash（m1）= hash（m2）。 理论复杂度为$O(2^{n \over 2})$  
朴素的生日攻击方案如下：
1. 计算任意选择的2^(n/2)个消息的哈希，并将所有的消息-哈希对存下来
2. 重排哈希值列表
3. 搜索排序后的列表以查找具有相同哈希值的两个连续条目  
可以看到，这种方法需要大量的内存，同时对大量元素进行排序会减慢搜索的速度。  
利用朴素生日攻击算法对SM3进行碰撞攻击，直接寻找两个哈希相同的字符串，因为攻击难度远小于Project 1，所以实现效果好，在可接受的时间里实现了$48$比特的碰撞攻击。  

## 代码说明
利用**字典**这个数据结构，省去朴素生日攻击的排序时间。  
以哈希值前x位为键，对应的字符串为值，不断生成随机字符串并计算哈希值，存入字典中，当出现键值冲突时，即找到碰撞。

## 运行指导
**运行环境：** Pycharm 4.5.3 Python 3.9  
直接运行.py文件即为寻找48比特的SM3碰撞  
可通过修改主函数中变量$n$的值（$n\times 4$即为要碰撞的比特数），来修改碰撞的比特数。

## 运行结果
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

8比特运行结果截图
![image](https://github.com/fyl01/course-project/blob/main/Naive%20birthday%20attack%20for%20reduced%20SM3/naiveresult_8.png)
16比特运行结果截图
![image](https://github.com/fyl01/course-project/blob/main/Naive%20birthday%20attack%20for%20reduced%20SM3/naiveresult_16.png)
24比特运行结果截图
![image](https://github.com/fyl01/course-project/blob/main/Naive%20birthday%20attack%20for%20reduced%20SM3/naiveresult_24.png)
32比特运行结果截图
![image](https://github.com/fyl01/course-project/blob/main/Naive%20birthday%20attack%20for%20reduced%20SM3/naiveresult_32.png)
48比特运行结果截图
![image](https://github.com/fyl01/course-project/blob/main/Naive%20birthday%20attack%20for%20reduced%20SM3/naiveresult_48.png)
