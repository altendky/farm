# while true; do sleep 600; (date --iso-8601=seconds; date '+%s'; chia show --state; echo) | tee --append /farm/progress; done

seconds = None
delta_seconds = None
height = None
delta_height = None

with open("/farm/progress") as f:
    for line in f:
        line = line.strip()
        if line.isdigit():
            new_seconds = int(line)
            if seconds is not None:
                delta_seconds = new_seconds - seconds
            seconds = new_seconds
        elif line.startswith("Time:") and "Height:" in line:
            new_height = int(line.split("Height:")[-1].strip())
            if height is not None:
                delta_height = new_height - height
            height = new_height

            if delta_seconds is not None and delta_height is not None:
                per_second = delta_height / delta_seconds
                per_hour = per_second * 60 * 60
                print(f"{height},{int(per_hour)}")
