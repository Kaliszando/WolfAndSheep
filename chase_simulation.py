import csv
import json
import argparse
import os
import configparser
import logging
import functions as fun

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


def main():

    # default params init
    init_pos_limit = 10.0
    epochs = 50
    sheep_count = 15
    sheep_move_dist = 0.5
    wolf_move_dist = 1.0

    log_lvl = None

    # sheep list
    flock = []

    # sheep positions
    sheep_pos = []

    # file data
    json_data = []
    csv_data = []

    # path to pos.json and alive.csv files
    data_dir = os.getcwd()

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        type=file_type,
                        metavar='FILE',
                        help='specify config file with initial values',
                        dest='conf_file'
                        )
    parser.add_argument('-d', '--dir',
                        type=dir_type,
                        metavar='DIR',
                        help='specify path to catalog that holds generated files',
                        dest='data_dir'
                        )
    parser.add_argument('-l', '--log',
                        type=int,
                        metavar='LEVEL',
                        help='choose level of logs saved in chase.log file: 10: DEBUG, 20: INFO, '
                             '30: WARNING, 40: ERROR, 50: CRITICAL',
                        dest='log_lvl'
                        )
    parser.add_argument('-r', '--rounds',
                        type=int,
                        metavar='NUM',
                        help='specify max number of iterations',
                        dest='rounds_no'
                        )
    parser.add_argument('-s', '--sheep',
                        type=int,
                        metavar='NUM',
                        dest='sheep_no',
                        help='specify number of sheep in flock'
                        )
    parser.add_argument('-w', '--wait',
                        action='store_true',
                        dest='wait_flag',
                        help='wait for user at the end of each round to continue'
                        )
    parser.add_argument('-q', '--quiet',
                        action='store_false',
                        dest='quiet_flag',
                        help='do not print info in terminal'
                        )
    args = parser.parse_args()

    # check optional args
    wait_flag = args.wait_flag
    print_flag = args.quiet_flag

    if args.data_dir:
        data_dir = os.path.join(data_dir, args.data_dir)

    if args.log_lvl:
        for lvl in [10, 20, 30, 40, 50]:
            if args.log_lvl == lvl:
                log_lvl = lvl

        if log_lvl is None:
            raise ValueError('no such level: ' + str(args.log_lvl))

        print(os.path.join(data_dir, 'chase.log'))

        logging.basicConfig(filename=os.path.join(data_dir, 'chase.log'),
                            filemode='w',
                            level=log_lvl
                            )

    if args.conf_file:
        config = configparser.ConfigParser()
        config.read(args.conf_file)

        terrain = config['Terrain']
        movement = config['Movement']

        if float(terrain['InitPosLimit']) < 0:
            logging.critical('ValueError raised: incorrect value in InitPosLimit config file')
            raise ValueError('negative value in config file: InitPosLimit')

        if float(movement['SheepMoveDist']) < 0:
            logging.critical('ValueError raised: incorrect value in SheepMoveDist config file')
            raise ValueError('negative value in config file: SheepMoveDist')

        if float(movement['WolfMoveDist']) < 0:
            logging.critical('ValueError raised: incorrect value in WolfMoveDist config file')
            raise ValueError('negative value in config file: WolfMoveDist')

        init_pos_limit = float(terrain['InitPosLimit'])
        sheep_move_dist = float(movement['SheepMoveDist'])
        wolf_move_dist = float(movement['WolfMoveDist'])

    if args.rounds_no:
        if args.rounds_no > 0:
            epochs = args.rounds_no
        elif log_lvl is not None:
            logging.warning('value passed by -r/--rounds is incorrect, continuing with default values')

    if args.sheep_no:
        if args.sheep_no > 0:
            sheep_count = args.sheep_no
        elif log_lvl is not None:
            logging.warning('value passed by -s/--sheep is incorrect, continuing with default values')

    # animals init
    wolf = Wolf(wolf_move_dist)
    for round_no in range(sheep_count):
        flock.append(Sheep(sheep_move_dist, round_no, init_pos_limit))
        sheep_pos.append(flock[round_no].position)

    # log formatter
    epoch_log = '[{:2}]\twolf pos.: ({: >7.3f}, {: >7.3f})\tnumber of sheep: {:2}'
    eaten_log = '  •———— sheep [{:2}] is dead'
    tmp_str = epoch_log.format(0, wolf.position[0], wolf.position[1], len(flock))
    if print_flag:
        print(tmp_str)
    logging.info(tmp_str)

    # wait for user input
    if wait_flag:
        input('Press enter to continue: ')

    # main loop
    for round_no in range(1, epochs + 1):

        # move and update sheep
        for sheep in flock:
            sheep.move()
            sheep_pos[sheep.id] = sheep.position

        # find closest sheep to wolf
        closest_sheep = flock[0]
        for sheep in flock:
            x = fun.calc_euclid_dist(wolf.position, sheep.position)
            if x < fun.calc_euclid_dist(wolf.position, closest_sheep.position):
                closest_sheep = sheep
        wolf.closest_sheep_pos = closest_sheep.position
        logging.info('sheep closest to wolf found ({})'.format(closest_sheep.position))

        # eat or chase sheep
        if fun.calc_euclid_dist(wolf.position, closest_sheep.position) < wolf.move_dist:
            tmp_str = eaten_log.format(closest_sheep.id)
            if print_flag:
                print(tmp_str)
            logging.info(tmp_str)

            flock.remove(closest_sheep)
            sheep_pos[closest_sheep.id] = None
        else:
            wolf.move()
            logging.info('Wolf is chasing closest sheep')

        # print epoch summary
        tmp_str = epoch_log.format(round_no,
                                   wolf.position[0],
                                   wolf.position[1],
                                   len(flock))
        if print_flag:
            print(tmp_str)
        logging.info(tmp_str)

        # append data to csv file
        csv_data.append([round_no, len(flock)])

        # append data to json file
        cloned_sheep_pos_list = sheep_pos[:]
        json_data.append({
                'round_no': round_no,
                'wolf_pos': wolf.position,
                'sheep_pos': cloned_sheep_pos_list
            }
        )

        # end loop if no sheep in flock
        if len(flock) < 1:
            logging.info('simulation ended: all sheep were eaten')
            break

        # wait for user input
        if wait_flag and input('Press enter to continue: ') == 'exit':
            logging.info('simulation ended: user stopped the simulation')
            break

    # write to json file
    with open(os.path.join(data_dir, 'pos.json'), mode='w', newline='') as json_file:
        json_file.write(json.dumps(json_data, indent=4))
        logging.info('data written to pos.json')

    # write to csv file
    with open(os.path.join(data_dir, 'alive.csv'), mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['epoch_no', 'living_sheep'])
        writer.writerows(csv_data)
        logging.info('data written to alive.csv')


if __name__ == '__main__':
    main()
