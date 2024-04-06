#ifndef DATA_H
#define DATA_H

typedef struct {
    double *times;
    double **values;
    int d;
    int num_times;
    double **delta_X;
} Data;

Data *create_data(int num_times, int d);
void destroy_data(Data *data);
void set_times(Data *data, double *times);
void set_values(Data *data, double **values);
void calculate_delta_X(Data *data);
void print_data(Data *data);
#endif
