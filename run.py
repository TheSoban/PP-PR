from subprocess import PIPE, Popen
from math import floor

SAMPLES = 200
INPUT_FILE_NUMBER = 10000
PROGRESS_BAR_LEN = 20

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def progress_message(percent):
    full = "=" * floor(percent * PROGRESS_BAR_LEN)
    empty = " " * (PROGRESS_BAR_LEN - len(full))
    print(f"\rRunning for ({INPUT_FILE_NUMBER}) [{Color.OKGREEN}{full}{empty}{Color.END}] {round(percent * 100): >4}%", end="")


def check_if_no_errors(output_line):
    if "Argument" in output_line or "Cannot" in output_line:
        return f"\n{Color.FAIL}Error occured in C for ({INPUT_FILE_NUMBER}): {Color.BOLD}{output_line[:-1]}{Color.END}"
    return None


def process_output(output_line):
    sm, t  = [tmp.split(":")[1] for tmp in output_line.split(",")]
    return int(sm), float(t)


def main():
    output = []
    progress_message(0)
    for i in range(SAMPLES):
        proc = Popen(["./sum-basic.out", str(INPUT_FILE_NUMBER)], stdout=PIPE, stderr=PIPE, encoding="UTF-8")
        check = check_if_no_errors(proc.communicate()[1])
        if check is not None:
            print(check)
            return
        output.append(proc.communicate()[0])
        progress_message((i+1) / SAMPLES)
    
    print("\nProcessing results")
    sums = set()
    times = []
    for line in output:
        sm, t = process_output(line)
        sums.add(sm)
        times.append(t)
    
    if len(sums) != 1:
        print(f"{Color.FAIL}Sums don't much!{Color.END}")
        return

    computed_sum = sums.pop()

    with open("./data/solutions.txt", "r") as file:
        for line in file.readlines():
            if str(INPUT_FILE_NUMBER) == line.split(".")[0]:
                if int(line.split("-")[-1]) != computed_sum:
                    solution_sum = int(line.split("-")[-1])
                    print(f"{Color.FAIL}Computed sum ({computed_sum}) doesn't much the solution ({solution_sum})!{Color.END}")
                    return
    
    print(f"Results from {SAMPLES} samples: avg={round(sum(times)/len(times), 6)}, min={round(min(times), 6)}, max={round(max(times), 6)}")

if __name__ == "__main__":
    main()
