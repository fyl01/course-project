__author__ = 'DELL'
import time
import random
from gmssl import sm3, func

def generate_random_str(randomlength=16):
  """
  生成一个指定长度的随机字符串
  """
  random_str =''
  base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789`~!@#$%^&*'
  length =len(base_str) -1
  for i in range(randomlength):
    random_str +=base_str[random.randint(0, length)]
  return random_str


if __name__ == '__main__':
    a = dict()
    n = 12   # 碰撞前 n*4 比特
    #数据和加密后数据为bytes类型
    data = b"201900460014" # bytes类型
    h = sm3.sm3_hash(func.bytes_to_list(data))
    start = time.time()
    while(a.get(h[:n]) is None):
        a[h[:n]] = data
        s = generate_random_str()
        data = bytes(s.encode())
        h = sm3.sm3_hash(func.bytes_to_list(data))
    end = time.time()
    print("\nFind the collision!(",n*4,"bits)\n")
    print("str1:",data,"\nhash(str1):",h)
    print("str2:",a[h[:n]],"\nhash(str2):",sm3.sm3_hash(func.bytes_to_list(a[h[:n]])))
    print("Running time:",end-start,"seconds")
