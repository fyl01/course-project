# course-project
cyberspace security practice of innovation and entrepreneurship course
## Project 1：implement the Rho method of reduced SM3
**Environment:** Ubuntu 20.04  
**Result：**
| Collision bit | Running time |
|---|---|
| 8 bits | 0.000536 seconds |
| 16 bits | 0.110520 seconds |
| 24 bits | $\approx$ 12 seconds |
| 32 bits | $\approx$ 5 hours |

<font size="1">The above data vary greatly with the change of the initial value.</font><br />  
- [Pollardrho.py](https://github.com/fyl01/course-project/blob/main/Pollardrho.py): 利用rho思想实现的整数分解，与破解SM3无关。
- [Rho_for_SM3.c](https://github.com/fyl01/course-project/blob/main/Rho_for_SM3.c): 利用rho思想实现了reduced SM3的碰撞。  

已编写Makefile文件  
```shell
$ make
$ ./test
```
可得到产生碰撞的两个字符串（转化为16进制形式）和找到此次碰撞所需的时间。
