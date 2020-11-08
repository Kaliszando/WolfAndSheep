from wolf import Wolf
from sheep import Sheep

# params init
init_pos_limit = 10.0
epochs = 70
sheep_count = 15
sheep_move_dist = 0.5
wolf_move_dist = 1.0

# animals init
wolf = Wolf(wolf_move_dist)

flock = []
for i in range(sheep_count):
    flock.append(Sheep(sheep_move_dist, i, init_pos_limit))

log = '[{}] WOLF: {:.3f}, {:.3f}, FLOCK: {}'

while len(flock) > 0 and epochs > 0:
    epochs -= 1

    for sheep in flock:
        sheep.move()
        sheep.update(wolf.get_pos())

    closest_sheep = flock[0]
    for sheep in flock:
        if sheep.wolf_dist < closest_sheep.wolf_dist:
            closest_sheep = sheep

    print(log.format(epochs, wolf.get_pos()[0], wolf.get_pos()[1], len(flock)))
    if closest_sheep.wolf_dist < wolf.move_dist:
        flock.remove(closest_sheep)

    else:
        wolf.move(closest_sheep.get_pos())

