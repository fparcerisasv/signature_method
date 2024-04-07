#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include "signature.h"
#include <stdbool.h>    

Signature *create_signature(int k, Data *data) {
    Signature *signature = malloc(sizeof(Signature));
    if (signature == NULL) {
        return NULL;
    }
    signature->k = k;
    signature->data = data;
    signature->d = data->d;
    signature->mu = 0;
    signature->delta_mu = NULL;
    signature->words = NULL;

    // Init words
    create_words(signature); // Create words

    generate_combinations(signature); // Generate all possible combinations
    
    return signature;
}

void set_delta_mu(Signature *signature) {
    int num_times = signature->data->num_times;
    signature->delta_mu = malloc((num_times - 1) * sizeof(double));
    if (signature->delta_mu == NULL) {
        return;
    }
    for (int n = 1; n < num_times; n++) {
        signature->delta_mu[n - 1] = exp(-signature->mu * (signature->data->times[n] - signature->data->times[n - 1]));
    }
}
/***GET VALUE OF THE SIGNATURE  BETWEEN GIVEN m AND n***/
double* calculate_signature(Signature *signature, int m, int n) {
    for (int i = 0; i < signature->num_combinations; i++) {
        reset_is_calculated(&signature->words[i]);
    }
    double *sig = malloc(signature->num_combinations * sizeof(double));
    for(int i = 0; i<signature->num_combinations;i++){
        sig[i] = signature_helper(signature,n,m,&signature->words[i]);
    }

    return sig;

}
/***GET VALUE OF SIGNATURE FOR A GIVEN WORD AND POSITIION***/
double signature_helper(Signature *signature, int n,int m,Word *word)
{ 
    if(word->length == 0){
        return 1;
    }
    if(word->is_calculated[n]){

        return word->value[n];
    }
    if (n==m) {
        word->value[n] = 0;
        word->is_calculated[n] = true;
        return 0;
    }

    

    if (word->indexes[word->length - 1]->head) { // If the last index is a head
        word->value[n] = signature->delta_mu[n-1] * (signature_helper(signature,n-1,m,word) + 
                                signature->data->delta_X[n-1][word->indexes[word->length - 1]->i] * signature_helper(signature,n-1,m,&signature->words[word->prev_word_index]));
    } else {
        word->value[n] = signature->delta_mu[n-1] * signature_helper(signature,n-1,m,word) + signature->data->delta_X[n-1][word->indexes[word->length - 1]->i] * signature_helper(signature,n,m,&signature->words[word->prev_word_index]);
    }
         word->is_calculated[n] = true;
        return word->value[n];
}




/***INTIALIZE WORDS***/
void create_words(Signature *signature){

    signature->num_combinations = combinatory(2*signature->d + signature->k +1 ,signature->k); // calculate number of combinations
    signature->words = (Word *) malloc(signature->num_combinations * sizeof(Word )); // allocate memory for words
    signature->possible_indexes = malloc(2*signature->d * sizeof(Index)); // allocate memory for possible indexes
    for (int i = 0; i < signature->d; i++) { // set possible indexes
        signature->possible_indexes[2*i].i = i;
        signature->possible_indexes[2*i].head = false; // head goes first
        signature->possible_indexes[2*i + 1].i = i;
        signature->possible_indexes[2*i + 1].head = true;
    }

}
void destroy_words(Signature *signature) {
    destroy_word(signature->words);

    free(signature->words);
    free (signature->possible_indexes);
}


/***GENERATE COMBINATIONS OF WORDS***/
void generate_combinations(Signature *signature) {

    signature->words[0] = create_word_from_scratch(0,signature->data->num_times); 
    int first=0,last=1; // First and last indexes of words of previous length
    int index = 1;
    signature->words[0].prev_word_index = -1;
    for (int length =  0; length < signature->k; length++) {
        for (int i=first;i<last;i++){
            for (int j = 0;j<2*signature->d;j++){
                add_index(&signature->words[i], &signature->words[index], &signature->possible_indexes[j]);
                signature->words[index].prev_word_index = i;

                index++;
            }
        }
        first = last;
        last = index;
    }
    
}

char** get_words(Signature *signature){
    char **words = malloc(signature->num_combinations * sizeof(char *));
    for (int i = 0; i < signature->num_combinations; i++) {
        words[i] = word_to_string(signature->words[i]);
    }
    return words;
}