#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main(int argc, char *argv[])
{
  double start = omp_get_wtime();

  char filename[100];
  short buffer;

  int thread_id, i, N;

  long long sum = 0;

  FILE *f = NULL;

  if (argc > 1) sprintf(filename, "./data-bin/%s.bin", argv[1]);
  else {
    fprintf(stderr, "Argument \"input_file_number\" is missing\n");
    return EXIT_FAILURE;
  }
  
  int num = atoi(argv[1]);

  if (num <= 10000)
  {
    f = fopen(filename, "rb");
    if (f == NULL)
    {
        fprintf(stderr, "Cannot open file \"%s\"\n", filename);
        return EXIT_FAILURE;
    }
    while (fread(&buffer, sizeof(buffer), 1, f) > 0)
        sum += buffer;
    fclose(f);
  }
  else
  {
    if (num <= 100000) N = 4;
    else if (num <= 1000000) N = 6;
    else N = 50;

    const int cycles = num / N;

    #pragma omp parallel num_threads(N) reduction(+: sum) private(f, buffer, thread_id, i)
    {
      thread_id = omp_get_thread_num();
      f = fopen(filename, "rb");
      if (f == NULL)
      {
        fprintf(stderr, "Cannot open file \"%s\"\n", filename);
        #pragma omp cancel parallel
      }
      fseek(f, sizeof(buffer) * cycles * thread_id, SEEK_SET);
      #pragma omp parallel for
      for (i = 0; i < cycles; i++)
      {
        if (fread(&buffer, sizeof(buffer), 1, f) <= 0)
          i = cycles;
        else
          sum += buffer;
      }
      #pragma omp single
      {
        if (num != cycles * N) {
          fseek(f, sizeof(buffer) * cycles * N, SEEK_SET);
          while (fread(&buffer, sizeof(buffer), 1, f) > 0)
            sum += buffer;
        }
      }
      fclose(f);
    }
  }
  
  double end = omp_get_wtime();

  double time_taken = end - start;

  printf("sum: %lld, t: %f\n", sum, time_taken);
  return EXIT_SUCCESS;
}