# Project 5: Impl Merkle Tree following RFC6962
依据RFC6962，创建一个Merkle Tree，并实现以下三点：  
1. Construct a Merkle tree with 10w leaf nodes
2. Build inclusion proof for specified element
3. Build exclusion proof for specified element

## 代码说明
Merkle Tree本质上是二叉树，利用类这个数据结构，建立起一个Merkle Tree。其中，哈希函数采用sha256。  
测试阶段，随机产生了100,000个数据，转化为16进制字符串作为叶子结点的值，构建出Merkle Tree。  
测试存在性时，分别测试了根节点、两个随机数、一个叶子结点，最后结果为根节点和叶子结点均在Merkle Tree中，两个随机数不在Merkle Tree中，符合预期。

## 运行指导
**运行环境：** Pycharm 4.5.3 Python 3.9  
直接运行.py文件，建立10w个叶子结点的Merkle Tree，并测试了四个数据的存在性。  

## 运行结果
运行结果截图如下  
（第一条为根节点，最后一条为叶子结点，中间两个数据是随机数，结果符合预期）
![image](https://github.com/fyl01/course-project/blob/main/MerkleTree/result.png)

## 参考资料
**RFC6962** https://www.rfc-editor.org/rfc/rfc6962
