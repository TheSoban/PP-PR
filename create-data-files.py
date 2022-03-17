from random import randint
import os

DATA_FILES_DIRECTORY = './data'
MIN_NUMBER_VALUE = 1
MAX_NUMBER_VALUE = 999

# create files with sizes ranging from 100 to 10000000
file_sizes_to_create = [10 ** exponent for exponent in range(2, 8)]

# create data directory
if not os.path.exists(DATA_FILES_DIRECTORY):
    os.makedirs(DATA_FILES_DIRECTORY)

# delete old data files
for file in os.listdir(DATA_FILES_DIRECTORY):
    os.remove(os.path.join(DATA_FILES_DIRECTORY, file))

# create new data files and save solutions to solutions.txt
with open(f'{DATA_FILES_DIRECTORY}/solutions.txt', 'w') as s:
    for file_size in file_sizes_to_create:
        file_name = f'{file_size}.txt'
        with open(f'{DATA_FILES_DIRECTORY}/{file_name}', 'w') as f:
            numbers = [randint(MIN_NUMBER_VALUE, MAX_NUMBER_VALUE)
                       for _ in range(file_size)]
            f.write('\n'.join(map(str, numbers)))
            s.write(f'{file_name} - {sum(numbers)}\n')
            print(f'{file_name} created')
