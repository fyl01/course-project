import numpy as np
import random
import hashlib

class MerkleTreeNode:
    def __init__(self, value, num):
        self.lChild = None    # 左子节点
        self.rChild = None    # 右子节点
        self.parent = None    # 父节点
        self.value = value


    def getroot(self):


    def proof(self, nodevalue):
        if nodevalue in :   # inclusive
            print("    Node:",nodevalue,"\n    This node is in the Merkle Tree")
        else:          # exclusive
            print("    Node:",nodevalue,"\n    This node is not in the Merkle Tree")



class MerkleTree:
    def __init__(self, leaf):
        self.leaf = leaf
        self.root = None

    # following RFC 6962
    def sha256_leaf(self,value):   # 级联0x00
        return hashlib.sha256((value[0:2] + "00" + value[2:]).encode('utf-8')).hexdigest()

    def sha256_node(self,value):   # 级联0x01
        return hashlib.sha256((value[0:2] + "01" + value[2:]).encode('utf-8')).hexdigest()

    def creat_MerkleTree(self):
        leafhash = []
        count  = len(self.leaf)
        for i in range(count):
            hashvalue = self.sha256_leaf(self.leaf[i])
            leafhash.append(hashvalue)

        if count == 1:    # 根节点就是叶子结点的hash级联hash 再hash
            self.root = self.sha256_node(leafhash[0]+leafhash[0])

            return  self.root
        # 中间节点是左右子节点级联再hash
        midnode = []
        midnode.append(leafhash)
        while (count > 1):
            for i in range(0, count, 2):
                lchild = leafhash[i]
                if i+1 < count:
                    rchild = leafhash[i+1]
                    parenthash = self.sha256_node(lchild+rchild)
                    midnode.append(parenthash)
                else:           # 右子节点是左子节点的复制
                    parenthash = self.sha256_node(lchild+lchild)
                    midnode.append(parenthash)

            count -= 2

        if count == 1:





if __name__ == '__main__':
    leafnode = np.random.randint(low = 0, high = 10**6, size=10**5)  # 生成10万个随机数作为叶子结点的值
    leafhex = [ hex(i) for i in leafnode]
    # print(leafhex[1][0:2] + "00" + leafhex[1][2:])
    mtn = MerkleTree(leafhex)
    
    root = mtn.creat_MerkleTree()
    print("Root of the Merkle Tree:",root)
    print("Inclusion Proof\n",MerkleTree.proof(root))
    number = hashlib.sha256(hex(random.randint(0,10**6))).hexdigest()
    print("Exclusion Proof\n",MerkleTree.proof(number))

