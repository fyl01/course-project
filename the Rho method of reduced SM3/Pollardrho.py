import random
import math
import time
from functools import reduce
import gmpy2

##判断素数
def MillerRabinPrime(n):
    #判断素数
    if n % 2 == 0 or n % 3 == 0 or n % 5 == 0 or n % 7 == 0 or n % 11 == 0:
        return False
    #循环次数m
    m = 5
    t = 0
    u = n-1
    while u % 2 == 0:        #变成奇数再判断
        t += 1
        u //= 2
    for i in range(0,m):
        a = random.randint(2,n-1)     #随机选取一个a∈(2,n-1)
        r = Pow_Mod(a,u,n)
        if r != 1:
            while t > 1 and r != n - 1:
                r = (r * r) % n
                t -= 1
            if r != n - 1:
                return False
        return True

def isPrime(n):
    k = int(math.sqrt(n))
    for i in range(2, k+2):
        if n % i == 0:
            return False
    return True

def Pow_Mod(a,b,p):
    #快速幂
    res = 1
    base = a%p
    while (b > 0):
        tmp = b&1
        if (tmp):
            res = (res*base)%p
        base = (base*base)%p
        b >>= 1
    return res      #a^b%p

##穷举法
def phi(p):
    count = 0
    for i in range(1,p):
        if math.gcd(p,i) == 1:
            count += 1
    return count

def findDLP(p,g,t):
    a = 0
    for i in range(0,p-1):    #due to Miller Rabin => p is prime => phi(p)=p-1
        if Pow_Mod(g,i,p) == t:     #use math.pow lead to overflow,so use quickmod
            a=i
            break
    return a

#分解大整数
def f(x):
    return x**2 + 1

def pollard_rho(N):
    xn = 2
    x2n = 2
    d = 1
    while d == 1:
        xn = f(xn) % N
        x2n = f(f(x2n)) % N
        abs_val = abs(xn - x2n)
        d = gcd(abs_val, N)
    return d

def Factor(n):
    ans = []
    while True:
        temp = pollard_rho(n)
        ans.append(temp)
        n = n//temp
        if n == 1:return ans
        if isPrime(n):
            ans.append(n)
            return ans


if __name__ == '__main__':
    p = int(input("Please enter the Module："))
    g = int(input("Please enter the Primitive Root:"))
    t = int(input("Please enter an integer："))
    start = time.time()
    d = findDLP(p, g, t)
    end = time.time()
    print("The discrete logarithm is",d)
    print("Running time:",end-start,"seconds")