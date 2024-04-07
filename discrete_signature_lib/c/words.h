#ifndef WORDS_H
#define WORDS_H
#include <stdbool.h>
#include <stdio.h>

typedef struct {
    int i; 
    bool head;
}Index;
/*List of indexes*/
typedef struct{
    //int prev_word_index;
    Index ** indexes;
    int length,prev_word_index,num_times;
    double *value;
    bool *is_calculated;
} Word;

Word create_word_from_scratch(int length,int num_times); //Creates struct Word
void destroy_word(Word *word); //Frees memory of struct Word
unsigned long long factorial(int n); //Calculates factorial of n
unsigned long long combinatory(int n, int k) ;
void print_word(Word word);
void add_index(Word *word, Word *new_word,  Index *index);
void reset_is_calculated(Word * word);
char* word_to_string(Word word);
#endif
