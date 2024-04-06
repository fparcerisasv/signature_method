#ifndef SIGNATURE_H
#define SIGNATURE_H

#include "data.h"
#include "words.h"
#include <stdbool.h>
#include <stdlib.h>

typedef struct {
    int k,d,num_combinations;
    Index *possible_indexes;
    Data *data;
    double mu;
    double *delta_mu;
    Word *words;

} Signature;
/* Constructors */
Signature *create_signature(int k, Data *data);
double* calculate_signature(Signature *signature, int m, int n);
void create_words(Signature *signature);
void destroy_words(Signature *signature);
void generate_combinations(Signature *signature);

double signature_helper(Signature *signature, int n,int m,Word *word);

/*Getters and setters*/

void set_delta_mu(Signature *signature);

void set_mu(Signature *signature, double mu) {
    signature->mu = mu;
}

#endif
