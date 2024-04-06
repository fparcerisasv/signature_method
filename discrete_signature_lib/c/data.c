// data.c

#include "data.h"


#include <stdlib.h>
#include <stdio.h>

Data *create_data(int num_times, int d) {
    Data *data = malloc(sizeof(Data));
    if (data == NULL) {
        return NULL;
    }
    data->num_times = num_times;
    data->d = d;
    data->times = malloc(num_times * sizeof(double));
    if (data->times == NULL) {
        free(data);
        return NULL;
    }
    data->values = malloc(num_times * sizeof(double *));
    if (data->values == NULL) {
        free(data->times);
        free(data);
        return NULL;
    }
    for (int i = 0; i < num_times; i++) {
        data->values[i] = malloc(d * sizeof(double));
        if (data->values[i] == NULL) {
            for (int j = 0; j < i; j++) {
                free(data->values[j]);
            }
            free(data->values);
            free(data->times);
            free(data);
            return NULL;
        }
    }
    return data;
}

void destroy_data(Data *data) {
    for (int i = 0; i < data->num_times; i++) {
        free(data->values[i]);
    }
    free(data->values);
    free(data->times);
    free(data);
}

void set_times(Data *data, double *times) {
    for (int i = 0; i < data->num_times; i++) {
        data->times[i] = times[i];
    }
}

void set_values(Data *data, double **values) {
    for (int i = 0; i < data->num_times; i++) {
        for (int j = 0; j < data->d; j++) {
            data->values[i][j] = values[i][j];
        }
    }
}

void calculate_delta_X(Data *data) {
    double **delta_X = malloc((data->num_times - 1) * sizeof(double *));
    if (delta_X == NULL) {
        data->delta_X = NULL;
    }
    for (int i = 0; i < data->num_times - 1; i++) {
        delta_X[i] = malloc(data->d * sizeof(double));
        if (delta_X[i] == NULL) {
            for (int j = 0; j < i; j++) {
                free(delta_X[j]);
            }
            free(delta_X);
            data->delta_X = NULL;
        }
        for (int j = 0; j < data->d; j++) {
            delta_X[i][j] = data->values[i + 1][j] - data->values[i][j];
        }
    }
    data->delta_X = delta_X;

}
void print_data(Data *data) {
    printf("Data\n");
    for (int i = 0; i < data->num_times; i++) {
        printf("%f: ", data->times[i]);
        for (int j = 0; j < data->d; j++) {
            printf("%f ", data->values[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}
