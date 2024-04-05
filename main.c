#include <stdio.h>
#include "signature.h"

#include <math.h>
#include "data.h"
#include "words.h"
#include <stdlib.h>

int main() {
    printf("Hello, World!\n");

    Data *data = create_data(5,2);

    double * times;
    times = malloc(5 * sizeof(double));
    if (times == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }
    times[0] = 0;
    times[1] = 1;
    times[2] = 1.5;
    times[3] = 2.5;
    times[4] = 3;
double **values = malloc(5 * sizeof(double *));
    if (values == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }

    // Allocate memory for each row
    for (int i = 0; i < 5; i++) {
        values[i] = malloc(2 * sizeof(double));
        if (values[i] == NULL) {
            printf("Memory allocation failed\n");
            return 1;
        }
    }

    // Assign values to each row
    values[0][0] = 1;
    values[0][1] = 1;
    values[1][0] = 3;
    values[1][1] = 4;
    values[2][0] = 3;
    values[2][1] = 2;
    values[3][0] = 5;
    values[3][1] = 2;
    values[4][0] = 8;
    values[4][1] = 6;
    set_times(data, times);
    set_values(data, values);

    Signature *signature = create_signature(2, data);
    printf("Signature created\n");
     double * sig = calculate_signature(signature, 0, 4);
    for (int i = 0; i < signature->words->num_combinations; i++) {
        printf("Signature element %d: %f\n", i, sig[i]);
    }



    return 0;
}