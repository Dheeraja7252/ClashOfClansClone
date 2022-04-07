from time import clock

from src.constants import SCREEN_HEIGHT, TIME_BW_FRAMES, RESET_CURSOR
from src.utils import filename_by_id

# TODO: save game frames for replay

def show_frame(frame):
    print(RESET_CURSOR)
    for line in frame:
        for ch in line:
            print(ch, end='')
        print("")


id = input("Enter game id:")
filename = "replay/" + filename_by_id(id)
lines = []
try:
    with open(filename) as f:
        lines = f.readlines()
except IOError:
    print("Invalid id, could not load file")
    raise SystemExit

frame_len = SCREEN_HEIGHT + 3
frames = [lines[i:i + frame_len] for i in range(0, len(lines), frame_len)]

prev_time = clock()
for frame in frames:
    while clock() - prev_time < TIME_BW_FRAMES:
        pass

