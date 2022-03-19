#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main(int argc, char *argv[])
{
  double start, end;
  start = omp_get_wtime();

  char filename[100];
  short buffer;
  int rc;
  long sum = 0;
  if (argc > 1) sprintf(filename, "./data-bin/%s.bin", argv[1]);
  else {
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

  end = omp_get_wtime();
  printf("sum: %ld, time: %g\n", sum, end - start);
  return EXIT_SUCCESS;
}