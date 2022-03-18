#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main(int argc, char *argv[])
{
  clock_t start, end;
  start = clock();
  
  char filename[100];
  char buffer[1000];
  int rc, sum = 0;
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

  while ((rc = fscanf(f, "%s", buffer)) > 0) sum += atoi(buffer);
  fclose(f);

  end = clock();
  double time_taken = (double)(end - start) / (double)CLOCKS_PER_SEC;
  printf("sum: %d, t: %f\n", sum, time_taken);
  return EXIT_SUCCESS;
}