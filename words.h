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
    int length,prev_word_index;
} Word;

/*All combination of words*/
typedef struct {
    int k;
    int d;
    Word ** combinations;
    int num_combinations;
    Index *possible_indexes;
} Words;

Words *create_words(int k, int d); //Creates struct Words
void destroy_words(Words *words); //Frees memory of struct Words
Word create_word(int length); //Creates struct Word
void destroy_word(Word *word); //Frees memory of struct Word
void generate_combinations(Words *words); //Generates all possible combinations of words for given k and d
unsigned long long factorial(int n); //Calculates factorial of n
unsigned long long combinatory(int n, int k) ;
void print_word(Word word);
Word* add_index(Word *word,  Index *index);

#endif
