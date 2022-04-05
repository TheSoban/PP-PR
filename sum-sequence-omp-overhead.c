#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

int main(int argc, char *argv[])
{
  clock_t start = clock();
  
  char filename[100];
  char buffer[1000];

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

  while (fscanf(f, "%s", buffer) > 0) 
    sum += atoi(buffer);

  fclose(f);

  clock_t end = clock();

  double time_taken = (double)(end - start) / (double)CLOCKS_PER_SEC;
  
  printf("sum: %lld, t: %f\n", sum, time_taken);
  return EXIT_SUCCESS;
}