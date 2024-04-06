// words.c

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "words.h"
#include <stdio.h>

void destroy_word(Word *word){
    free(word->indexes);
}
Word create_word_from_scratch(int length,int num_times){ // Create a word with given length and number of times
    Word word;
    word.indexes = malloc(length * sizeof(Index *));// allocate memory for n pointers to indexes
    word.length = length;
    word.num_times = num_times;
    word.value = malloc(num_times * sizeof(double)); // allocate memory for n values
    word.is_calculated = malloc(num_times * sizeof(bool)); // allocate memory for n booleans
    reset_is_calculated(&word);
    return word;
}

void reset_is_calculated(Word * word){
    for (int i = 0; i < word->num_times; i++) {
        word->is_calculated[i] = false;
    }
}

unsigned long long factorial(int n) { // Calculate factorial
    unsigned long long fact = 1;
    for (int i = 1; i <= n; ++i) {
        fact *= i;
    }
    return fact;
}
unsigned long long combinatory(int n, int k) { // Calculate combinatory number
    return factorial(n) / (factorial(k) * factorial(n - k));
}
void print_word(Word word){
    printf("\'");
    
    for(int i = 0; i<word.length; i++){
        printf("%d", word.indexes[i]->i);
        printf("%s", word.indexes[i]->head ? "-" : "+");
    }
    printf("\' ");
};

void add_index(Word *word,Word *new_word, Index *index){ // Creates new word from indexes from previous word
    if (word == NULL){
        new_word->length = 0;
        return ;
    }
    new_word->length = word->length + 1;

    new_word->indexes = malloc((new_word->length) * sizeof(Index *));
    
    *new_word->indexes = *word->indexes; // first n indexes are the same
    new_word->indexes[word->length] = malloc(sizeof(Index*));
    new_word->indexes[word->length] = index; 

   new_word->num_times = (int) word->num_times + 0;
    
    new_word->value = malloc(new_word->num_times * sizeof(double)); // allocate memory for n values
    new_word->is_calculated = malloc(new_word->num_times * sizeof(bool)); // allocate memory for n booleans
    reset_is_calculated(new_word);
   }
