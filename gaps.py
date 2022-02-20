import dataclasses
import datetime
import itertools
import string
import sys
import time


@dataclasses.dataclass
class Line:
    timestamp: datetime.datetime
    line: str
    rest: str


# https://docs.python.org/3.10/library/itertools.html#itertools.pairwise
def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def split(lines):
    for line in sys.stdin:
        if len(line) == 0:
            first = None
        else:
            first = line[0]

        if first not in string.digits:
            continue

        time_text, maybe_space, rest = line.strip().partition(' ')
        timestamp = datetime.datetime.fromisoformat(time_text)

        yield Line(timestamp=timestamp, line=line, rest=rest)


def main():
    for before, after in pairwise(split(sys.stdin)):
        gap = after.timestamp - before.timestamp
        is_big_gap = gap > datetime.timedelta(seconds=20)
        if is_big_gap:
            print(f" ==== gap: {gap}")
            print(after.line.rstrip())

main()
