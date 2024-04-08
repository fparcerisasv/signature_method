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
    //reset_is_calculated(&word);
    return word;
}

void reset_is_calculated(Word * word){
    for (int i = 0; i < word->num_times; i++) {
        word->is_calculated[i] = false;
    }
}


unsigned long long combinatory(int n, int k) { // Calculate combinatory number
    int sum = 1, mult = 1;
    for (int i = 1; i <=k; i++) {
        mult = n*mult;
        sum +=mult;
    }
    return sum;
}
void print_word(Word word){
    printf("\'");
    
    for(int i = 0; i<word.length; i++){
        printf("%d", word.indexes[i].i);
        printf("%s", word.indexes[i].head ? "-" : "+");
    }
    printf("\' ");
};
char* word_to_string(Word word){
    char *str = malloc(2*word.length * sizeof(char));
    if (str == NULL){
        printf("Error allocating memory\n");
        return NULL;
    }
    if (word.length == 0){
        sprintf(str,"%s", " ");
    }
    for(int i = 0; i<word.length; i++){
        sprintf(str + 2*i,"%d", word.indexes[i].i);
        sprintf(str + 2*i + 1,"%s", word.indexes[i].head ? "-" : "+");
    }
    return str;
}

void add_index(Word *word,Word *new_word, Index index){ // Creates new word from indexes from previous word
    if (word == NULL){
        new_word->length = 0;
        return ;
    }
    new_word->length = word->length + 1;

    new_word->indexes = malloc((new_word->length) * sizeof(Index ));
    
    memcpy(new_word->indexes,word->indexes,sizeof(Index)*word->length); // first n indexes are the same
    //new_word->indexes[word->length] = malloc(sizeof(Index*));
    new_word->indexes[word->length] = index; 

   new_word->num_times = (int) word->num_times + 0;
    
    new_word->value = malloc(new_word->num_times * sizeof(double)); // allocate memory for n values
    new_word->is_calculated = malloc(new_word->num_times * sizeof(bool)); // allocate memory for n booleans
    //reset_is_calculated(new_word);
   }
