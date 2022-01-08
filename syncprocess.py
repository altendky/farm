import dataclasses
import datetime
import json
import pathlib
import sys


# {"query_time":"2022-01-06T02:24:10Z","height":939108,"timestamp":"2021-10-02T01:46:48Z","sync":{"sync_mode":true,"sync_progress_height":939108,"sync_tip_height":1373334,"synced":false}}
# {"query_time":"2022-01-06T02:25:10Z","height":939226,"timestamp":null,"sync":{"sync_mode":true,"sync_progress_height":939226,"sync_tip_height":1373334,"synced":false}}

iso_format = "%Y-%m-%dT%H:%M:%SZ"

@dataclasses.dataclass(frozen=True)
class Record:
    query_time: datetime.datetime
    height: int

    @classmethod
    def from_json(cls, json_string):
        record = json.loads(json_string)
        height = record["height"]
        if height is None:
            height = 0
        
        return cls(
            query_time=datetime.datetime.strptime(record["query_time"], iso_format),
            height=height,
        )


def main(path):
    with path.open() as file:
        records = [Record.from_json(json_string=line) for line in file]

    old_iter = iter(records)
    new_iter = iter(records)
    for _ in range(60):
        next(new_iter)

    for old, new in zip(old_iter, new_iter):
        delta = (new.query_time - old.query_time).total_seconds()
        progress = new.height - old.height
        height = new.height
        rate = progress / delta
        bph = rate * 60 * 60
        print(",".join(str(x) for x in [new.query_time, height, progress, bph]))



sys.exit(main(pathlib.Path(sys.argv[-1])))
