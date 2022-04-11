import dataclasses
import itertools
import os
import pathlib
import subprocess
import time
import typing


@dataclasses.dataclass(frozen=True)
class Parameter:
    name: str
    flag: str
    value: int
    common: bool

    def render(self) -> typing.List[str]:
        return [self.flag, str(self.value)]


thread_parameters = [
    Parameter(name="threads", flag="-t", value=value, common=True)
    for value in [15, *range(26, 33, 2)]
]
b_parameters = [
    Parameter(name="b", flag="-b", value=value, common=False)
    for value in [512]
]
fx_parameters = [
    Parameter(name="fx", flag="--fx", value=value, common=False)
    for value in ["128MB", "256MB"]
]
f1_parameters = [
    Parameter(name="f1", flag="--f1", value=value, common=False)
    for value in ["128MB", "256MB"]
]


parameter_sets = [
    thread_parameters,
    b_parameters,
    fx_parameters,
    f1_parameters,
]


base_command = ["/farm/bladebit/build/bladebit"]
target_path = pathlib.Path("/farm/yards/907/testing")
summary_path = target_path.joinpath("summary.log")


def print_both(*args, file, **kwargs):
    print(*args, **kwargs, flush=True)
    print(*args, **kwargs, file=file, flush=True)


def main():
    this_path = pathlib.Path(__file__)
    target_path.joinpath(this_path.name).write_bytes(this_path.read_bytes())

    # bladebit -f ade0cc43610ce7540ab96a524d0ab17f5df7866ef13d1221a7203e5d10ad2a4ae37f7b73f6cdfd6ddf4122e8a1c2f8ef -p 80a836a74b077cabaca7a76d1c3c9f269f7f3a8f2fa196a65ee8953eb81274eb8b7328d474982617af5a0fe71b47e9b8 -t 24 -w -i c6b84729c23dc6d60c92f22c17083f47845c1179227c5509f07a5d2804a7b835 --memo 80a836a74b077cabaca7a76d1c3c9f269f7f3a8f2fa196a65ee8953eb81274eb8b7328d474982617af5a0fe71b47e9b8ade0cc43610ce7540ab96a524d0ab17f5df7866ef13d1221a7203e5d10ad2a4ae37f7b73f6cdfd6ddf4122e8a1c2f8ef01b7bf8a22a9ac82a003e07b551c851ea683839f3e1beb8ac9ede57d2c020669 --show-memo diskplot -t /mnt/p5510a/disk_tmp --f1 256MB --fx 256MB -b 64 /mnt/p5510a/disk_tmp

    with summary_path.open("w", encoding="utf-8") as summary_file:
        for parameters in itertools.product(*parameter_sets):
            common_options = [
                token
                for parameter in parameters
                for token in parameter.render()
                if parameter.common
            ]

            disk_options = [
                token
                for parameter in parameters
                for token in parameter.render()
                if not parameter.common
            ]

            file_flags = [f"{parameter.name}-{parameter.value}" for parameter in parameters]
            file_flags_string = "_".join(file_flags)
            log_path = target_path.joinpath(f"bladebit-disk_{file_flags_string}.log")

            command = [
                *base_command,
                "-f",
                "ade0cc43610ce7540ab96a524d0ab17f5df7866ef13d1221a7203e5d10ad2a4ae37f7b73f6cdfd6ddf4122e8a1c2f8ef",
                "-p",
                "80a836a74b077cabaca7a76d1c3c9f269f7f3a8f2fa196a65ee8953eb81274eb8b7328d474982617af5a0fe71b47e9b8",
                "-w",
                "-i",
                "c6b84729c23dc6d60c92f22c17083f47845c1179227c5509f07a5d2804a7b835",
                "--memo",
                "80a836a74b077cabaca7a76d1c3c9f269f7f3a8f2fa196a65ee8953eb81274eb8b7328d474982617af5a0fe71b47e9b8ade0cc43610ce7540ab96a524d0ab17f5df7866ef13d1221a7203e5d10ad2a4ae37f7b73f6cdfd6ddf4122e8a1c2f8ef01b7bf8a22a9ac82a003e07b551c851ea683839f3e1beb8ac9ede57d2c020669",
                "--show-memo",
                *common_options,
                "diskplot",
                *disk_options,
                "-t",
                os.fspath(target_path),
                "/dev/null",
            ]
            print_both(f"log: {log_path}", file=summary_file)
            print_both(f"    command: {command}", file=summary_file)
            for parameter in parameters:
                print_both(f"    {parameter.name}: {parameter.value}", file=summary_file)
            with log_path.open(mode="wb") as log_file:
                start = time.monotonic()
                completed_process = subprocess.run(command, check=True, stdout=log_file)
                end = time.monotonic()
            duration = end - start
            print_both(f"    duration: {duration:.0f} seconds, {duration / 60:.1f} minutes", file=summary_file)


main()
