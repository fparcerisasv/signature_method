#ifndef SIGNATURE_H
#define SIGNATURE_H

#include "data.h"
#include "words.h"
#include <stdbool.h>

typedef struct {
    Word *word;
    double **value;
    bool **is_calculated;
    int num_times;
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
double signature_helper(Signature *signature, int m, int n,SignatureElement *element);
SignatureElement * create_signature_element( int lenght,Signature *signature){
    SignatureElement *element =  malloc(sizeof(SignatureElement*));
    element->num_times = signature->data->num_times; 
    
    element->value = (double **) malloc(signature->data->num_times * sizeof(double *));
    for (int i = 0; i < signature->data->num_times; i++) {
        element->value[i] = (double *) malloc(signature->data->num_times * sizeof(double));

    } 
    element->is_calculated = (bool **) malloc(signature->data->num_times * sizeof(bool *)); 
    if (element->is_calculated == NULL) {
    printf("Memory allocation failed for is_calculated\n");
}
    for (int i = 0; i < signature->data->num_times; i++) {
        element->is_calculated[i] = (bool *)malloc(signature->data->num_times * sizeof(bool));
        if (element->is_calculated[i] == NULL) {
            printf("Memory allocation failed for is_calculated[%d]\n", i);
        }
        printf("Address %p\n", element->is_calculated[i]);
        for (int j = 0; j < signature->data->num_times; j++) {
            element->is_calculated[i][j] = false;
            printf("Position %d %d\n", i, j);
            printf("Address %p\n", &element->is_calculated[i][j]);
        }
    }
    return element;

}
void init_all_signature_elements(Signature *signature){
    signature->elements = malloc(signature->words->num_combinations * sizeof(SignatureElement*));

    for (int i = 0; i < signature->words->num_combinations; i++) {
        signature->elements[i]=create_signature_element(signature->words->combinations[i]->length,signature);

        signature->elements[i]->word = malloc(sizeof(Word));
        *signature->elements[i]->word = *signature->words->combinations[i];
        printf("Element %d\n", i);
        print_word(*signature->elements[i]->word);
    }
}
/*
void print_signature(Signature *signature){
    printf("Signature for %d and %d\n", 0, 0);
    for (int k = 0; k < signature->words->num_combinations; k++) {
        for (int i = 0; i < signature->data->num_times; i++) {
            for (int j = 0; j < signature->data->num_times; j++) {
                printf("%f ", signature->sig[k][i][j]);
            }
            printf("\n");
        }
        printf("\n");
    }
}
*/

/*Getters and setters*/

void set_delta_mu(Signature *signature);
/*double ***get_signature(Signature *signature){
    print_signature(signature);
    return signature->sig;;*/
void set_mu(Signature *signature, double mu) {
    signature->mu = mu;
}
Words *get_words(Signature *signature){return signature->words;};
void set_words(Signature *signature, Words *words){signature->words = words;};  


/*Destructors*/

void destroy_signature_element(SignatureElement *element, int num_times){
    for (int i = 0; i < num_times; i++) {
        free(element->value[i]);
    }
    free(element->value);
    for (int i = 0; i < num_times; i++) {
        free(element->is_calculated[i]);
    }
    free(element->is_calculated);
}



#endif
