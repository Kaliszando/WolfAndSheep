import csv
import json

from wolf import Wolf
from sheep import Sheep

# params init
init_pos_limit = 10.0
epochs = 50
sheep_count = 15
sheep_move_dist = 0.5
wolf_move_dist = 1.0

# sheep list
flock = []

# sheep positions
sheep_pos = []

# animals init
wolf = Wolf(wolf_move_dist)
for i in range(sheep_count):
    flock.append(Sheep(sheep_move_dist, i, init_pos_limit))
    sheep_pos.append(flock[i].get_pos())

# log formatter
epoch_log = '[{:2}]\twolf: ({: >7.3f}, {: >7.3f})\tno. sheep: {:2}'
eaten_log = '  •———— sheep [{:2}] is dead'
print(epoch_log.format(0, wolf.get_pos()[0], wolf.get_pos()[1], len(flock)))

# files var init
json_str = ''

# init alive.csv file
with open('alive.csv', mode='w', newline="") as csv_file:
    fieldnames = ['epoch_no', 'living_sheep']
    writer = csv.writer(csv_file)
    writer.writerow(fieldnames)

# init pos.json file
with open('pos.json', mode='w', newline='') as json_file:
    pass

# main loop
for i in range(1, epochs+1):

    # move and update sheep
    for sheep in flock:
        sheep.move()
        sheep.update(wolf.get_pos())
        sheep_pos[sheep.id] = sheep.get_pos()

    # find closest sheep to wolf
    closest_sheep = flock[0]
    for sheep in flock:
        if sheep.wolf_dist < closest_sheep.wolf_dist:
            closest_sheep = sheep

    # eat or chase sheep
    if closest_sheep.wolf_dist < wolf.move_dist:
        print(eaten_log.format(closest_sheep.id))
        flock.remove(closest_sheep)
        sheep_pos[closest_sheep.id] = None
    else:
        wolf.move(closest_sheep.get_pos())

    # print epoch summary
    print(epoch_log.format(i,
                           wolf.get_pos()[0],
                           wolf.get_pos()[1],
                           len(flock))
          )

    # append data to csv file
    with open('alive.csv', mode='a', newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([i, len(flock)])

    # append data to json file
    with open('pos.json', mode='a', newline='') as json_file:
        json_row = {
            'round_no': i,
            'wolf_pos': wolf.get_pos(),
            'sheep_pos': sheep_pos
        }
        json_file.write(json.dumps(json_row, indent=4))

    # end loop if no sheep in flock
    if len(flock) < 1:
        break
