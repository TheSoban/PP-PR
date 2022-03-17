#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
  int c;
  char *filename = "./data/100.txt";
  char bufor[1000];
  int L = 0;
  int v = 0;
  if (argc > 1)
  {
    filename = argv[1];
  };

  fprintf(stderr, "File: %s\n", filename);
  FILE *f = fopen(filename, "r");
  if (f != NULL)
  {
    while ((c = fscanf(f, "%s", bufor)) > 0)
    {
      v = atoi(bufor);
      L += v;
    }
  }
  fclose(f);
  printf("{Sum: %d}\n", L);
  return EXIT_SUCCESS;
}