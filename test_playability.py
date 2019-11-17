import numpy as np
from playability import evaluate_playability

# file_name = "tloz1_2_room_5.txt"
file_name = "tloz2_1_room_15.txt"

room = []
with open(file_name, 'r') as fp:
    while True:
        line = fp.readline()
        if not line:
            break

        room_line = []
        for tile in line:
            if tile != "\n":
                room_line.append(tile)
            
        room.append(room_line)

room = np.asarray(room)
# print(room)
# print(room.shape)

rooms = np.reshape(room, (-1, room.shape[0], room.shape[1]))
# print(rooms.shape)

unplayable, playability = evaluate_playability(rooms)
print(unplayable)
print(playability)

