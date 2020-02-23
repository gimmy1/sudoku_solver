from itertools import chain
from collections import defaultdict
import functools
import operator
ROWS = "ABCDEFGHI"
COLS = "123456789"
SUDOKU_STRING = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."



def helper_cross(rows, cols):
    return [r+c for r in rows for c in cols]

def row_units(rows, cols):
    return [helper_cross(r, cols) for r in rows]

def col_units(rows, cols):
    return [helper_cross(rows, c) for c in cols]

def square_units(rows, cols):
    return [helper_cross(sr, sc) for sr in (rows[:3], rows[3:6], rows[6:]) for sc in (cols[:3], cols[3:6], cols[6:])]

def get_row_units(unit):
    return [r+c for r in ROWS for c in unit[1] if r+c != unit]

def get_col_units(unit):
    return [r+c for r in unit[0] for c in COLS if r+c != unit]

def get_square_units(unit):
    row = next(v for _, v in enumerate([("ABC"), ("DEF"), ("GHI")]) if unit[0] in v)
    col = next(v for _, v in enumerate([("123"), ("456"), ("789")]) if unit[1] in v)
    return [r+c for r in row for c in col if r+c != unit]


def grid_values(ssudoku):
    # Convert string representation of board into a dictionary
    # IF "." in place, then add "123456789" instead
    # '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    values = "123456789"
    sudoku_dictionary = defaultdict(str)
    unit_list = functools.reduce(operator.iconcat, row_units(ROWS, COLS) + col_units(ROWS, COLS) + square_units(ROWS, COLS), [])
    for (u, s) in zip(unit_list, ssudoku):
        sudoku_dictionary[u] = s if s != "." else values
    return sudoku_dictionary

def eliminate_helper(unit, sdict):
    unique_units = set(get_row_units(unit) + get_col_units(unit) + get_square_units(unit))
    for unique in unique_units:
        if len(sdict[unique]) == 1 and sdict[unique] in sdict[unit]:
            replace = sdict[unit].replace(sdict[unique], "")
            sdict[unit] = replace
    return sdict[unit]

def eliminate(sdict):
    # NOW HOW DO WE ELIMINATE?
    for k, v in sdict.items():
        eliminate_value = eliminate_helper(k, sdict)
        sdict[k] = eliminate_value
    return sdict


def only_choice(sdict):
    for key, val in sdict.items():
        if len(val) > 1:
            units = set(get_row_units(key) + get_col_units(key) + get_square_units(key))
            for v in val:
                exists = False
                for unit in units:
                    if v in sdict[unit]:
                        exists = True
                if not exists:
                    sdict[key] = v
    return sdict

def reduce_puzzle(sdict):
    """ Naive constraint propogation"""
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([(key, val) for key, val in sdict.items() if len(val) == 1])
        edict = eliminate(sdict)
        odict = only_choice(edict)
        solved_values_after = len([(key, val) for key, val in odict.items() if len(val) == 1])
        stalled = solved_values_before == solved_values_after
        if len([(key, val) for key, val in odict.items() if len(val) == 0]): return False
    return sdict
        
if __name__ == "__main__":
    sdict = grid_values(SUDOKU_STRING)
    eliminated_dict = eliminate(sdict)
    only_dict = only_choice(eliminated_dict)
    reduce_puzzle(only_dict)
# def display(sudoku_dictionary, unit_list):
#     """ MAKE IT LOOK LIKE THIS
#         . . 3 |. 2 . |6 . . 
#         9 . . |3 . 5 |. . 1 
#         . . 1 |8 . 6 |4 . . 
#         ------+------+------
#         . . 8 |1 . 2 |9 . . 
#         7 . . |. . . |. . 8 
#         . . 6 |7 . 8 |2 . . 
#         ------+------+------
#         . . 2 |6 . 9 |5 . . 
#         8 . . |2 . 3 |. . 9 
#         . . 5 |. 1 . |3 . . 
#     """
#     pass





