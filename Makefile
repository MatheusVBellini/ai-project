FILE=main.c
OUT=main

all : $(OUT)

$(OUT) : $(FILE)
	gcc -o $@ $^

clean :
	rm -r main
