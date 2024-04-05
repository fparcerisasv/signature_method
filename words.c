// words.c

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "words.h"
#include <stdio.h>

Words *create_words(int k, int d) {
    Words *words = malloc(sizeof(Words)); // Allocate memory for the struct
    if (words == NULL) {
        return NULL;
    }
    words->k = k;
    words->d = d;
    words->num_combinations = (int)combinatory(d*2+k+1, k); // Calculate the number of combinations
    words->combinations = malloc(words->num_combinations * sizeof(Word*)); // Allocate memory for the combinations
    if (words->combinations == NULL) {
        free(words);
        return NULL;
    }
    for (int i = 0; i < words->num_combinations; i++) {
        words->combinations[i] = (Word *)malloc(sizeof(Word)); // Allocate memory for each combination
    }
    words->possible_indexes = malloc(d * 2 * sizeof(Index)); // Allocate memory for the possible indexes
    for (int i = 0; i < d; i++) {
        words->possible_indexes[2*i].i = i;
        words->possible_indexes[2*i].head = true;
        words->possible_indexes[2*i + 1].i = i;
        words->possible_indexes[2*i + 1].head = false;
    }
    if (words->combinations == NULL) {
        free(words);
        return NULL;
    }
    return words;
}

void destroy_words(Words *words) {
    for (int i = 0; i < words->num_combinations; i++) {
        destroy_word(words->combinations[i]);
    }
    free(words->combinations);
    free (words->possible_indexes);
    free(words);

}

void destroy_word(Word *word){
    free(word->indexes);
}
Word create_word(int length){
    Word word;
    word.indexes = malloc(length * sizeof(Index *));// allocate memory for n pointers to indexes
    //word.prevWord = NULL;
    word.length = length;
    //word.prev_word_index = -1;
    return word;
}





void generate_combinations(Words *words) {
    Word word = create_word(0); 
    int first=0,last=1; // First and last indexes of words of previous length
    int index = 1;
    words->combinations[0] = &word;
    for (int length = 0; length < words->k; length++) {
        for (int i=first;i<last;i++){
            for (int j = 0;j<2*words->d;j++){
                words->combinations[index] = add_index(words->combinations[i], &words->possible_indexes[j]);
                words->combinations[index]->prev_word_index = i;
                index++;
            }
        }
        first = last;
        last = index;
    }
    printf("Generated %d combinations\n", index);
    //Print all combinations
    for (int i = 0; i < words->num_combinations; i++) {
        print_word(*words->combinations[i]);
    }

printf("So long everything is fine if any errors from here on not our fault\n");
    
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
    for(int i = 0; i<word.length; i++){
        //printf(" **This index is on address %p**", word.indexes[i] );
        printf("%d", word.indexes[i]->i);
        printf("%s", word.indexes[i]->head ? "+" : "-");
    }
    printf("\n");
};
Word* add_index(Word *word, Index *index){ // Creates new word from indexes from previous word
    Word *new_word = malloc(sizeof(Word *)); //create new word with length + 1
    
    new_word->length = word->length + 1;

    new_word->indexes = malloc((new_word->length) * sizeof(Index *));
    
    *new_word->indexes = *word->indexes; // first n indexes are the same
    new_word->indexes[word->length] = malloc(sizeof(Index*));
    new_word->indexes[word->length] = index; 
    //new_word->prevWord = word;
   /* new_word->indexes[word->length]->i = i;
    new_word->indexes[word->length]->head = head;
    */
   
    return new_word;
}
