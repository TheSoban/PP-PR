import json
import numpy as np
from subprocess import PIPE, Popen
from math import floor, log10


class Config:
    def __init__(self):
        with open("config.json", "r") as file:
            self.data = json.load(file)
            self.input_files = [int(tmp) for tmp in self.data["inputFiles"]]
            self.samples = self.data["samples"]


config: Config


class Color:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def compile(program):
    proc_comm = Popen(
        ["gcc", "-fopenmp", f"{program}.c", "-o", f"{program}.out"], stdout=PIPE, stderr=PIPE, encoding="UTF-8"
    ).communicate()
    if proc_comm[1] != "":
        print(f"{Color.WARNING}{proc_comm[1]}{Color.END}")
        return False
    return True


def progress_message(percent, mode, input_file, thread_count):
    full = "=" * floor(percent * config.data["progressBarLen"])
    empty = " " * (config.data["progressBarLen"] - len(full))
    thread_count = " " if thread_count == -1 else thread_count
    print(
        f"\rRunning for ({mode}:10e{round(log10(input_file))}:{thread_count: >3}) "
        f"[{Color.OKGREEN}{full}{empty}{Color.END}] {round(percent * 100): >4}%",
        end="",
    )


def check_if_no_errors(output_line, input_file):
    if "Argument" in output_line or "Cannot" in output_line:
        return f"\n{Color.FAIL}Error occured in C for ({input_file}): {Color.BOLD}{output_line[:-1]}{Color.END}"
    return None


def process_output(output_line):
    sm, t = [tmp.split(":")[1] for tmp in output_line.split(",")]
    return int(sm), float(t)


def run(mode, input_file, samples, thread_count=-1):
    output = []
    if mode == "s":
        program = config.data["sequence.program"]
        program_params = [str(input_file)]
    elif mode == "d":
        program = config.data["dynamic.program"]
        program_params = [str(input_file)]
    else:
        program = config.data["parallel.program"]
        program_params = [str(input_file), str(thread_count)]
    progress_message(0, mode, input_file, thread_count)
    for i in range(samples):
        proc = Popen([f"./{program}.out", *program_params], stdout=PIPE, stderr=PIPE, encoding="UTF-8")
        check = check_if_no_errors(proc.communicate()[1], input_file)
        if check is not None:
            print(check)
            exit(-1)
        output.append(proc.communicate()[0])
        progress_message((i + 1) / samples, mode, input_file, thread_count)
    print()
    sums = set()
    times = []
    for line in output:
        sm, t = process_output(line)
        sums.add(sm)
        times.append(t)

    if len(sums) != 1:
        print(f"{Color.FAIL}Sums don't much: {sums}!{Color.END}")
        exit(-1)

    comp_sum = sums.pop()

    with open("./data-bin/solutions.txt", "r") as file:
        for line in file.readlines():
            if str(input_file) == line.split(".")[0]:
                if int(line.split("-")[-1]) != comp_sum:
                    sol_sum = int(line.split("-")[-1])
                    print(f"{Color.FAIL}Computed sum ({comp_sum}) doesn't much the solution ({sol_sum})!{Color.END}")
                    exit(-1)

    if config.data["outliers"]:
        times = np.array(times)
        mean = np.mean(times)
        std_dev = np.std(times)
        zero_based = abs(times - mean)
        max_deviations = 2
        no_outliers = times[zero_based < max_deviations * std_dev]
        avg_t = round(sum(no_outliers) / len(no_outliers), 6)
    else:
        avg_t = round(sum(times) / len(times), 6)

    if config.data["showIntermediateResults"]:
        print(f"Results from {samples} samples for ({input_file}): avg={avg_t}")
    return avg_t


def main():
    try:
        if config.data["compileBeforeRunning"]:
            if config.data["sequence.run"] and not compile(config.data["sequence.program"]):
                return
            if config.data["parallel.run"] and not compile(config.data["parallel.program"]):
                return
            if config.data["dynamic.run"] and not compile(config.data["dynamic.program"]):
                return

        sequence = dict()
        parallel = dict()
        dynamic = dict()
        for input_file, samples in zip(config.input_files, config.samples):
            if config.data["sequence.run"]:
                sequence[f"{input_file}"] = run("s", input_file, samples)
            if config.data["parallel.run"]:
                if config.data["parallel.runForEveryThreadCount"]:
                    parallel[f"{input_file}"] = {}
                    for thread_count in config.data["parallel.threadCount"]:
                        parallel[f"{input_file}"][f"{thread_count}"] = run("p", input_file, samples, thread_count)
                else:
                    parallel[f"{input_file}"] = run("p", input_file, samples)
            if config.data["dynamic.run"]:
                dynamic[f"{input_file}"] = run("d", input_file, samples)

    except KeyboardInterrupt:
        print("\nUser exited")
    finally:
        if config.data["sequence.run"]:
            print("Sequence:\n", json.dumps(json.loads(str(sequence).replace("'", '"')), indent=4))
        if config.data["parallel.run"]:
            print("Parallel:\n", json.dumps(json.loads(str(parallel).replace("'", '"')), indent=4))
        if config.data["dynamic.run"]:
            print("Dynamic:\n", json.dumps(json.loads(str(dynamic).replace("'", '"')), indent=4))


if __name__ == "__main__":
    config = Config()
    main()
