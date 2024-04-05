#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include "signature.h"

Signature *create_signature(int k, Data *data) {
    Signature *signature = malloc(sizeof(Signature));
    if (signature == NULL) {
        return NULL;
    }
    signature->k = k;
    signature->data = data;
    signature->mu = 0;
    signature->delta_mu = NULL;
    signature->words = NULL;

    // Init words
    signature->words = create_words(k, data->d);
    if (signature->words == NULL) {
        printf("Error: Unable to create Words.\n");
        return NULL;
    }
    generate_combinations(signature->words); // Generate all possible combinations
    printf("Number of combinations: %d\n", signature->words->num_combinations);
    signature->elements = (SignatureElement **) malloc(signature->words->num_combinations * sizeof(SignatureElement *));

    init_all_signature_elements(signature); // Initialize all signature elements
    calculate_signature(signature, 0, 4); // Calculate signature for m = 0 and n = 0
    return signature;
}

Signature *create_signature_with_words(int k, Data *data, Words *words) { //initiate signature with words
    Signature *signature = malloc(sizeof(Signature));
    if (signature == NULL) {
        return NULL;
    }
    signature->k = k;
    signature->data = data;
    signature->mu = 0;
    signature->delta_mu = NULL;
    signature->words = words;
    //signature->sig = NULL;
    signature->elements = malloc(words->num_combinations * sizeof(SignatureElement *));
    init_all_signature_elements(signature); // Initialize all signature elements

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

    printf("Delta mu set\n");

    for (int i = 0; i < num_times - 1; i++) {
        printf("%f ", signature->delta_mu[i]);
    }
}

double* calculate_signature(Signature *signature, int m, int n) {
    double *sig = malloc(signature->words->num_combinations * sizeof(double));
    printf("\nSignature for %d and %d\n", m, n);
    printf("Number of combinations: %d\n", signature->words->num_combinations);
   for(int i = 0; i<signature->words->num_combinations;i++){
        printf("Element %d ", i);
        print_word(*signature->elements[i]->word); printf("-popopopop");
        sig[i] = signature_helper(signature,m,n,signature->elements[i]);
        printf(" %f\t", sig[i]);   printf("\n");
   }
   printf("\n");
    return sig;

}

double signature_helper(Signature *signature, int m, int n,SignatureElement *element)
{   if(element->word->length == 0){
        return 1;
    }
    if(element->is_calculated[m][n]){
        return element->value[m][n];
    }
    
    if (m == n) {
        element->value[m][n] = 1;
        element->is_calculated[m][n] = true;
        return 1;
    }
    Word *word = element->word;
    SignatureElement * prev_element = signature->elements[word->prev_word_index];
    if (word->indexes[word->length - 1]->head) { // If the last index is a head
        element->value[m][n] = signature->delta_mu[n-1] * (signature_helper(signature,m,n-1,element) + 
                                signature->data->delta_X[n-1][word->indexes[word->length - 1]->i] * signature_helper(signature,m,n-1,prev_element));
        element->is_calculated[m][n] = true;
        return element->value[m][n];
    } else {
        element->value[m][n] = signature->delta_mu[n-1] * signature_helper(signature,m,n-1,element) + signature->data->delta_X[n-1][word->indexes[word->length - 1]->i] * signature_helper(signature,m,n,prev_element);
        element->is_calculated[m][n] = true;
        return element->value[m][n];

    }

}
