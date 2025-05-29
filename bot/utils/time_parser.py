import re

def parse_duration(arg: str) -> int:
    # Парсить '1h30m' -> 1.5 години
    hours = re.search(r"(\d+)h", arg)
    mins = re.search(r"(\d+)m", arg)
    total = 0
    if hours:
        total += int(hours.group(1))
    if mins:
        total += int(mins.group(1)) / 60
    return total 