import numpy as np
import random
import hashlib

class MerkleTreeNode:
    def __init__(self, value):
        self.lchild = None    # 左子节点
        self.rchild = None    # 右子节点
        self.parent = None    # 父节点
        self.value = value    # 每个节点的哈希值

class MerkleTree:
    def __init__(self, leaf):
        self.leaf = leaf
        self.root = None

    # following RFC 6962
    def sha256_leaf(self,value):   # 级联0x00
        return hashlib.sha256((value[0:2] + "00" + value[2:]).encode('utf-8')).hexdigest()

    def sha256_node(self,value):   # 级联0x01
        return hashlib.sha256((value[0:2] + "01" + value[2:]).encode('utf-8')).hexdigest()

    def create_MerkleTree(self):
        leafhash = []
        count = len(self.leaf)
        for i in range(count):
            hashvalue = self.sha256_leaf(self.leaf[i].value)
            leafhash_node = MerkleTreeNode(hashvalue)
            leafhash.append(leafhash_node)

        # 中间节点是左右子节点级联再按规则hash
        node = []    # 元素是节点
        node.append(leafhash)
        if count == 1:    # 根节点就是叶子结点的hash
            self.root = leafhash[0]
            return  self.root

        while len(leafhash) > 1:
            t = []
            for i in range(0, len(leafhash), 2):
                lchild = leafhash[i]
                if (i+1)>=len(leafhash):
                    parenthash = self.sha256_node(lchild.value+lchild.value)
                    parentnode = MerkleTreeNode(parenthash)
                    parentnode.lchild = lchild
                    parentnode.rchild = lchild
                    lchild.parent = parentnode
                    t.append(parentnode)
                else:
                    rchild = leafhash[i+1]
                    parenthash = self.sha256_node(lchild.value+rchild.value)
                    parentnode = MerkleTreeNode(parenthash)
                    parentnode.lchild = lchild
                    parentnode.rchild = rchild
                    lchild.parent = parentnode
                    rchild.parent = parentnode
                    # node.append(parenthash)
                    t.append(parentnode)
            leafhash = t
        self.root = leafhash[0]
        return self.root

    # 中序遍历得到整个Merkle Tree的节点值
    def Inorder(self, root):
        mtlist = []
        if(root == None):
            return
        self.Inorder(root.lchild)
        # print(root.value," ")
        mtlist.append(root.value)
        self.Inorder(root.rchild)
        return mtlist

    def proof(self, root, nodevalue):
        mtlist = self.Inorder(root)
        # print(len(mtlist))
        if nodevalue in mtlist:   # inclusive
            print("    Node:",nodevalue,"  This node is in the Merkle Tree")
        else:          # exclusive
            print("    Node:",nodevalue,"  This node is not in the Merkle Tree")


if __name__ == '__main__':
    leafdata = np.random.randint(low = 0, high = 10**6, size=10**5)  # 生成10万个随机数作为叶子结点的值
    leafhex = [ hex(i) for i in leafdata ]
    leafnode = [ MerkleTreeNode(i) for i in leafhex ]
    # print(leafhex[1][0:2] + "00" + leafhex[1][2:])
    mt = MerkleTree(leafnode)

    root = mt.create_MerkleTree()
    print("Root of the Merkle Tree:\n   ",root.value)
    print("Inclusion and Exclusion Proof")
    mt.proof(root,root.value)
    number1 = hex(random.randint(0,10**6))
    numberhash1 = hashlib.sha256(number1.encode('utf-8')).hexdigest()
    mt.proof(root,numberhash1)
    number2 = hex(random.randint(0,10**6))
    numberhash2 = hashlib.sha256(number2.encode('utf-8')).hexdigest()
    mt.proof(root,numberhash2)


