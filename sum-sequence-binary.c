#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[])
{
  clock_t start = clock();

  char filename[100];
  short buffer;

  long long sum = 0;

  if (argc > 1)
    sprintf(filename, "./data-bin/%s.bin", argv[1]);
  else
  {
    fprintf(stderr, "Argument \"input_file_number\" is missing\n");
    return EXIT_FAILURE;
  }

  FILE *f = fopen(filename, "rb");
  if (f == NULL)
  {
    fprintf(stderr, "Cannot open file \"%s\"\n", filename);
    return EXIT_FAILURE;
  }

  while (fread(&buffer, sizeof(buffer), 1, f) > 0)
    sum += buffer;

  fclose(f);

  clock_t end = clock();

  double time_taken = (double)(end - start) / (double)CLOCKS_PER_SEC;

  printf("sum: %lld, t: %f\n", sum, time_taken);
  return EXIT_SUCCESS;
}