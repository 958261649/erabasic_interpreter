import regex
from parsers import *


block_start = [
    r'[ \t]*IF',
    r'REPEAT',
    r'FOR',
    r'WHILE'
]

block_end = [
    r'[ \t]*ENDIF',
    r'REND',
    r'NEXT',
    r'WEND'
]

elses = [
    r'[ \t]*ELSE',
    r'[ \t]*ELSEIF',
]


class FindError(Exception):
    pass

#查找调用的函数在哪一行，但实际上erabasic的函数是可能在别的文件里的
def find_func(re, code, pos=0, reverse=False):
    for i in range(len(code))[pos::(-2*reverse+1)]:
        if regex.match(re, get_line(code, i)):
            return i + 1

    raise FindError('Cannot find that function')

# 这个应该是模仿basic语言在遇到 GOTO 等语句时全文查找标签在哪一行的操作
def find(re, code, pos, reverse=False):
    """
    this function will give you the searched position + 1 (past that instruction)
    """
    block_height = 0

    for r in elses:
        if regex.match(r, get_line(code, pos)):
            block_height = 1
            break

    direction = -2*reverse + 1

    for i in range(len(code))[pos::direction]:
        if regex.match(re, get_line(code, i)) and block_height == direction:
            return i + 1

        for s in block_start:
            if regex.match(s, get_line(code, i)):
                block_height += 1
                break

        for e in block_end:
            if regex.match(e, get_line(code, i)):
                block_height -= 1
                break

    raise FindError('Cannot find matching token')
