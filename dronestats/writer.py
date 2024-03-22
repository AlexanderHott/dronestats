import os
import datetime


def write_to_csv(data: list[float], filename: str) -> None:
    """Write data to a CSV file."""

    if len(data) != 3:
        raise ValueError("Data must contain 3 lap times")

    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write("time,lap1,lap2,lap3,total,fastest\n")

    with open(filename, 'a') as file:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{now},{data[0]},{data[1]},{data[2]},{sum(data)},{min(data)}\n")
