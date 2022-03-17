#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main(int argc, char *argv[])
{
  int c;
  char *filename = "./data/100.txt";
  char bufor[1000];
  int L = 0;
  int v = 0;
  int counter = 0;
  int end = 1;
  if (argc > 1)
  {
    filename = argv[1];
  };

  fprintf(stderr, "File: %s\n", filename);
  FILE *f = fopen(filename, "r");
  if (f != NULL)
  {
    #pragma omp parallel num_threads(2) 
    {
      if (omp_get_thread_num() == 0) c = fscanf(f, "%s", bufor);
      #pragma omp barrier

      while (c > 0)
      {
        if (omp_get_thread_num() != 0) {
          v = atoi(bufor);
          L+=v;
        }
        #pragma omp barrier

        if (omp_get_thread_num() == 0) c = fscanf(f, "%s", bufor);
      #pragma omp barrier
      }
      fclose(f);
    }
  }

  printf("{Sum: %d}\n", L);
  return EXIT_SUCCESS;
}