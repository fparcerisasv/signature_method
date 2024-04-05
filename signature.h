#ifndef SIGNATURE_H
#define SIGNATURE_H

#include "data.h"
#include "words.h"
#include <stdbool.h>
#include <stdlib.h>
typedef struct {
    Word *word;
    int num_times;
    double *value;
    bool *is_calculated;
    
}SignatureElement;
typedef struct {
    int k;
    Data *data;
    double mu;
    double *delta_mu;
    Words *words;
    SignatureElement **elements;
} Signature;
/* Constructors */
Signature *create_signature(int k, Data *data);
Signature *create_signature_with_words(int k, Data *data, Words *words);
double* calculate_signature(Signature *signature, int m, int n);
double signature_helper(Signature *signature, int n,SignatureElement *element);


/*

void reset_is_calculated(SignatureElement * element){
    for (int i = 0; i < element->num_times; i++) {
        *element->is_calculated[i] = false;
    }
}

*/
SignatureElement * create_signature_element( int lenght,Signature *signature){
    SignatureElement *element =  malloc(sizeof(SignatureElement*));
    element->num_times = signature->data->num_times; 
    
    
    element->is_calculated = (bool *) malloc(signature->data->num_times * sizeof(bool )); //allocate memory for is_calculated
     
     element->value = (double *) malloc(signature->data->num_times * sizeof(double *)); //allocate memory for the values
    if (element->value == NULL) {
        printf("Memory allocation failed for value\n");

    }
  
   if (element->is_calculated == NULL) {
    printf("Memory allocation failed for is_calculated\n");
    }
     for (int i = 0; i < signature->data->num_times; i++) {
       
        element->is_calculated[i] = false; //allocate memory for is_calculated
 
        //element->value[i] = (double *) malloc( sizeof(double));/* //allocate memory for the values*/
       /* if (element->value[i] == NULL) {
            printf("Memory allocation failed for value\n");

        }*/
       
      
    }

   // reset_is_calculated(element);
    
    return element;

}
void init_all_signature_elements(Signature *signature){
    signature->elements = malloc(signature->words->num_combinations * sizeof(SignatureElement*));
    
    for(int i=0;i<signature->words->num_combinations;i++){
       // print_word(* signature->words->combinations[i]);
        printf("Prev word index is in %p\n", & signature->words->combinations[i]->prev_word_index);
        //printf("word length is %d\n", signature->words->combinations[i]->length);
    }
    for (int i = 0; i < signature->words->num_combinations; i++) {
        signature->elements[i]=create_signature_element(signature->words->combinations[i]->length,signature);

        //signature->elements[i]->word = malloc(sizeof(Word));
        signature->elements[i]->word = signature->words->combinations[i];
      
        print_word(*signature->elements[i]->word);
        printf("Prev word index is %d\n", signature->elements[i]->word->prev_word_index);
        printf("Prev word index is in %p\n", & signature->words->combinations[i]->prev_word_index);

    }
}



/*Getters and setters*/

void set_delta_mu(Signature *signature);

void set_mu(Signature *signature, double mu) {
    signature->mu = mu;
}
Words *get_words(Signature *signature){return signature->words;};
void set_words(Signature *signature, Words *words){signature->words = words;};  


/*Destructors*/

void destroy_signature_element(SignatureElement *element, int num_times){

    free(element->value);
   
    free(element->is_calculated);
    free(element);
}



#endif
