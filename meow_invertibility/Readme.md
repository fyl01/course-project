# Project 4：meow_invertibility
**个人项目，完成人：傅宇琳 201900460014**  
 ### 原理

对该算法，观察到对于任何固定的 32 字节消息块，Meow算法具有易于计算的逆，并且最终轮次也是可逆的。这在现代MD散列函数中极为常见。

但是，通常这种可逆构造会修复全部或部分初始内部状态，而 Meow 哈希使用 1024 位密钥作为1024 位初始状态。因此，可以通过给定的一条消息$m$和目标哈希值$h$，一个人可以计算一个密钥$k$，满足$MeowHash(k,m) = h$，其只需通过从输出状态一直反向运行哈希函数的所有步骤到初始状态。

### 代码说明
通过上述原理分析，根据官方实现代码，将MeowHash()函数从输出结果开始反向运行即可。  
其中，aesdec()函数反向运行即为aesenc()，xor操作反向即为再做一次xor，add操作反向即为sub操作

### 运行指导
该项目建立在windows10 下的 visual studio2019，直接通过.sln文件建立代码项目后，运行即可（有关哈希值、消息值均已硬编码在代码里）  

### 运行结果

给定哈希值和消息如下  

hash value: sdu_cst_20220610  

message: Fu Yulin 201900460014  

最终利用可逆性计算出密钥（$128 bit*8$）  

![result](https://github.com/fyl01/course-project/blob/main/meow_invertibility/result.png)

### 参考资料 

官方实现代码 https://github.com/cmuratori/meow_hash  

meow算法性质 https://peter.website/meow-hash-cryptanalysis
