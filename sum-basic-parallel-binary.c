#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main(int argc, char *argv[])
{
  double start = omp_get_wtime();

  char filename[100];
  short buffer;

  int rc = 0;
  long long sum = 0;
  
  if (argc > 1) sprintf(filename, "./data/%s.txt", argv[1]);
  else {
    fprintf(stderr, "Argument \"input_file_number\" is missing\n");
    return EXIT_FAILURE;
  }

  FILE *f = fopen(filename, "r");
  if (f == NULL)
  {
    fprintf(stderr, "Cannot open file \"%s\"\n", filename);
    return EXIT_FAILURE;
  }
  
  #pragma omp parallel num_threads(2) 
  {
    if (omp_get_thread_num() == 0) rc = fread(&buffer, sizeof(buffer), 1, f);
    #pragma omp barrier

    while (rc > 0)
    {
      if (omp_get_thread_num() != 0) sum += buffer;
      #pragma omp barrier

      if (omp_get_thread_num() == 0) rc = fread(&buffer, sizeof(buffer), 1, f);
      #pragma omp barrier
    }
  }
  fclose(f);

  double end = omp_get_wtime();

  double time_taken = end - start;

  printf("sum: %lld, t: %f\n", sum, time_taken);
  return EXIT_SUCCESS;
}