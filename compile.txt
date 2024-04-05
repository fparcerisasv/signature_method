gcc -c -Wall -Werror -fpic data.c -o data.o
gcc -c -Wall -Werror -fpic words.c -o words.o
gcc -c -Wall -Werror -fpic signature.c -o signature.o
gcc -shared -o signature.so data.o words.o signature.o -lm
