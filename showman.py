#!/usr/bin/env python3


import time
import threading


CLEAR_LINE = "\033[K"
MOVE_UP = "\033[F"

def wiper():

    print('\r' + '  ' * 30 , end='')


def liner():

    print()


def mv_clr():
    print(f'\r{MOVE_UP}{CLEAR_LINE}', end='')


def count(line, num, wipe_space=False, next_line=False):

    if type(num) is not int:
        raise TypeError('First parameter should be an integer!')

    if type(wipe_space) is not bool or type(next_line) is not bool:
        raise TypeError('Second and third argument only accept boolean values!')

    for x in range(num, 0, -1):
        print(f'\r{line} Count: {x} seconds', end='')
        time.sleep(1)
        print(f'\r{CLEAR_LINE}', end='')

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


def carriage_dotprint(line, wipe_space=False, next_line=False):

    if type(line) is not str:
        raise TypeError('Argument: only strings are expected!')

    for x in ['.', '..', '...']:

        print(f'\r{line}{x}', end='', flush=True)
        time.sleep(0.5)
    
    wiper()

    for x in ['.', '..', '...']:

        print(f'\r{line}{x}', end='', flush=True)
        time.sleep(0.5)

    if wipe_space:
        print(f'\r{CLEAR_LINE}', end='')

    if next_line:
        liner()


def carriage_dict(data_dict, timeout=1):

    for x, y in data_dict.items():
        print(f'{x}: {y}')

    time.sleep(timeout)
    num = len(data_dict)
    var = f'\r{MOVE_UP}{CLEAR_LINE}' * num

    print(var, end='')

iteration_time = None


def carriage_ldict(data_ldict, timeout=1, wait=0):

    time.sleep(wait)

    for dictionary in data_ldict:

        global iteration_time

        start = time.perf_counter()
        x = '\n'.join(f'{k}: {v}' for k, v in dictionary.items())
        dict_num = len(dictionary)
        print(x)
        time.sleep(timeout)
        var = f'\r{MOVE_UP}{CLEAR_LINE}' * dict_num
        print(var, end='')
        end = time.perf_counter()
        iteration_time = end - start


dic_1 = [{'Name': 'Ichinose', 'Class': '1B', 'Gender': 'Female'}, {'Name': 'Ryuen', 'Class': '1C', 'Gender': 'Male'}, {'Name': 'Sakayanagi', 'Class': '1A', 'Gender': 'Female'}, {'Name': 'Horikita', 'Class': '1D', 'Gender': 'Female'}]
