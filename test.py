sm = 0
with open("data/100000000.txt", 'r') as file: # 100000000
    for line in file.readlines():
        sm += int(line)
print(sm)