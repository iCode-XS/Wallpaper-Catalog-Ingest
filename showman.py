#!/usr/bin/env python3


import time
import threading


def wiper():

    print('\033[K', end='')


def liner():

    print()


def count(num, wipe_space=False, next_line=False):

    if type(num) is not int:
        raise TypeError('First parameter should be an integer!')

    if type(wipe_space) is not bool or type(next_line) is not bool:
        raise TypeError('Second and third argument only accept boolean values!')

    for x in range(num, 0, -1):
        print(f'\rCount: {x} seconds', end='')
        time.sleep(1)

    if wipe_space:
        wiper()

    if next_line:
        liner()


def carriage_print(line, timeout=0, wipe_space=False, next_line=False):

    if type(line) is not str:
        raise TypeError('First argument: Only strings are expected!')

    if type(timeout) is not int:
        raise TypeError('Second argument should be num!')

    if type(wipe_space) is not bool or type(next_line) is not bool:
        raise TypeError('Third and forth argument only accept boolean values!')

    print(f'\r{line}', end='')
    time.sleep(timeout)

    if wipe_space:
        wiper()

    if next_line:
        liner()


def carriage_dotprint(line):

    if type(line) is not str:
        raise TypeError('Argument: only strings are expected!')

    for x in ['.', '..', '...']:

        print(f'\r{line}{x}', end='', flush=True)
        time.sleep(0.5)

    wiper()

    for x in ['.', '..', '...']:

        print(f'\r{line}{x}', end='', flush=True)
        time.sleep(0.5)

    wiper()
    liner()


CLEAR_LINE = "\033[K"
MOVE_UP = "\033[F"


def carriage_loopp(data_list):
    for dictionary in data_list:
        x = '\n'.join(f'{k}: {v}' for k, v in dictionary.items())
        dict_num = len(dictionary)
        print(x)
        time.sleep(1)
        var = f'\r{MOVE_UP}{CLEAR_LINE}' * dict_num
        print(var, end='')
