# Project 5: Impl Merkle Tree following RFC6962
依据RFC6962，创建一个Merkle Tree，并实现以下三点：  
1. Construct a Merkle tree with 10w leaf nodes
2. Build inclusion proof for specified element
3. Build exclusion proof for specified element

## 代码说明
Merkle Tree本质上是二叉树，利用类这个数据结构，建立起一个Merkle Tree。  
其中，哈希函数采用sha256

## 运行指导
**运行环境：** Pycharm 4.5.3 Python 3.9  
直接运行.py文件，建立10w个叶子结点的Merkle Tree，并测试了四个数据的存在性。  

## 运行结果
运行结果截图如下  
![image](https://github.com/fyl01/course-project/blob/main/MerkleTree/result.png)

## 参考资料
**RFC6962** https://www.rfc-editor.org/rfc/rfc6962
