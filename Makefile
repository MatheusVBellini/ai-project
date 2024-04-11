FILE=main.c
OUT=main
LIBS=lswipl

all : $(OUT)

$(OUT) : $(FILE)
	gcc -o $@ -I/usr/lib/swi-prolog/include $^ -L/usr/lib/swi-prolog/lib/x86_64-linux -lswipl

clean :
	rm -r main
