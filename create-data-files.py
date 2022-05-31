from random import randint
import os

DATA_FILES_DIRECTORY = './data'
MIN_NUMBER_VALUE = 1
MAX_NUMBER_VALUE = 999

# create files with sizes ranging from 10 to 100000000
file_sizes_to_create = [10 ** exponent for exponent in range(1, 9)]

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
            if file_size <= 10 ** 6:
                numbers = [randint(MIN_NUMBER_VALUE, MAX_NUMBER_VALUE)
                        for _ in range(file_size)]
                f.write('\n'.join(map(str, numbers)))
                s.write(f'{file_name} - {sum(numbers)}\n')
                print(f'{file_name} created')
            else:
                # sth wrong with sum

                sm = 0
                for _ in range(file_size // 10**6):
                    numbers = [randint(MIN_NUMBER_VALUE, MAX_NUMBER_VALUE)
                        for _ in range(10**6)]
                    sm += sum(numbers)
                    f.write('\n'.join(map(str, numbers)))

                s.write(f'{file_name} - {sm}\n')
                print(f'{file_name} created')