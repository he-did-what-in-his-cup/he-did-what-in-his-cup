from robomation import *
import time

NO_DATA = 65535

beagle = Beagle(0)
t0 = time.perf_counter()
beagle.lidar_power(True)

t_first = None
t_full = None

while True:
    arr = beagle.read(Beagle.LIDAR_ARRAY)
    now = time.perf_counter() - t0
    valid = sum(1 for d in arr if d != NO_DATA)

    if t_first is None and valid > 0:
        t_first = now
        print(f"first valid reading after {t_first:.2f} s")
    if t_full is None and valid >= 300:
        t_full = now
        print(f"~full scan (300+ valid) after {t_full:.2f} s")

    cone = list(arr[0:46]) + list(arr[314:360])
    cone_valid = [d for d in cone if d != NO_DATA]
    nearest = min(cone_valid) if cone_valid else None
    print(f"{now:6.2f}s  valid={valid:3d}  front nearest={nearest}")

    time.sleep(0.1)