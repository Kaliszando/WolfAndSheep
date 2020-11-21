import csv
import json
import argparse
import os

from wolf import Wolf
from sheep import Sheep


def file_type(path):
    if not os.path.isfile(path):
        msg = '%r is not a file' % path
        raise argparse.ArgumentTypeError(msg)
    if not os.path.exists(path):
        msg = 'file %r does not exists' % path
        raise argparse.ArgumentTypeError(msg)
    return path


def dir_type(path):
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.isdir(path):
        msg = '%r is not a directory' % path
        raise argparse.ArgumentTypeError(msg)
    return path


# default params init
init_pos_limit = 10.0
epochs = 50
sheep_count = 15
sheep_move_dist = 0.5
wolf_move_dist = 1.0

log_dir = os.getcwd()

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', type=file_type, metavar='FILE',
                    help='specify config file with initial values', dest='conf_file')
parser.add_argument('-d', '--dir', type=dir_type, metavar='DIR',
                    help='specify path to catalog that holds generated files', dest='log_dir')
parser.add_argument('-l', '--log', type=int, metavar='LEVEL', dest='log_lvl',
                    help='choose level of logs saved in chase.log file')
parser.add_argument('-r', '--rounds', type=int, metavar='NUM', dest='rounds_no',
                    help='specify max number of iterations')
parser.add_argument('-s', '--sheep', type=int, metavar='NUM', dest='sheep_no',
                    help='specify number of sheep in flock: 10: DEBUG, 20: INFO, '
                         '30: WARNING, 40: ERROR, 50: CRITICAL')
parser.add_argument('-w', '--wait', action='store_true', dest='wait_flag',
                    help='wait for user at the end of each round to continue')
parser.add_argument('-q', '--quiet', action='store_false', dest='quiet_flag',
                    help='do not print info in terminal')
args = parser.parse_args()

# check optional args
wait_flag = args.wait_flag
print_flag = args.quiet_flag

if args.conf_file:
    # TODO
    print(args.conf_file)

if args.log_dir:
    log_dir = os.path.join(log_dir, args.log_dir)

if args.log_lvl:
    # TODO
    pass

if args.rounds_no and args.rounds_no >= 0:
    epochs = args.rounds_no

if args.sheep_no and args.sheep_no > 0:
    sheep_count = args.sheep_no


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
epoch_log = '[{:2}]\twolf pos.: ({: >7.3f}, {: >7.3f})\tnumber of sheep: {:2}'
eaten_log = '  •———— sheep [{:2}] is dead'
if print_flag:
    print(epoch_log.format(0, wolf.get_pos()[0], wolf.get_pos()[1], len(flock)))

# init alive.csv file
with open(os.path.join(log_dir, 'alive.csv'), mode='w', newline="") as csv_file:
    fieldnames = ['epoch_no', 'living_sheep']
    writer = csv.writer(csv_file)
    writer.writerow(fieldnames)

# init pos.json file
with open('pos.json', mode='w', newline='') as json_file:
    pass

# wait for user input
if wait_flag:
    input('Press enter to continue ')

# main loop
for i in range(1, epochs + 1):

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
        if print_flag:
            print(eaten_log.format(closest_sheep.id))
        flock.remove(closest_sheep)
        sheep_pos[closest_sheep.id] = None
    else:
        wolf.move(closest_sheep.get_pos())

    # print epoch summary
    if print_flag:
        print(epoch_log.format(i,
                               wolf.get_pos()[0],
                               wolf.get_pos()[1],
                               len(flock))
              )

    # append data to csv file
    with open(os.path.join(log_dir, 'alive.csv'), mode='a', newline="") as csv_file:
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

    # wait for user input
    if wait_flag and input('Press enter to continue ') == 'exit':
        break
