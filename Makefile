# 自定义依赖关系，源文件（后缀为.c)经过编译汇编生成目标文件（后缀为.o)
# 目标文件执行生成可执行文件（类似与mytool）
test:Rho_for_SM3.o
	gcc Rho_for_SM3.o -o test -lcrypto

Rho_for_SM3.o:Rho_for_SM3.c
	gcc Rho_for_SM3.c -c -g -o Rho_for_SM3.o -lcrypto

clean:
	rm *.o test -rf

