gcc -c  data.c -o data.o
gcc -c   words.c -o words.o
gcc -c  signature.c -o signature.o
gcc -shared -o signature.so data.o words.o signature.o -lm
python classes_sig_c.py
python main.py