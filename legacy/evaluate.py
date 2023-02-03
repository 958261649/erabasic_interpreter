#regex疑似是某个正则表达式库，尝试用re模块取代
import regex
from typing import *
from collections.abc import Iterable
from tokens import *


def evaluate_code(code: str):
    pos = 0
    context = Context()

    code = code.split('\n')
    while pos < len(code):
        matched = False
        line = get_line(code, pos)

        #让当前行和 tokens.line[] 中的所有行类型逐个匹配
        for line_type in lines:
            if regex.match(regex.compile(line_type.re, regex.MULTILINE), line):
                pos = line_type(line).eval(context, pos, code)
                matched = True
                break
        #所有行类型都不能匹配的话报错
        if not matched:
            raise SyntaxError('Unexpected line type')
    #一行打印一下
    print(context)


if __name__ == '__main__':
    with open('../Frontend/test.erb', 'r') as f:
        evaluate_code(f.read(-1))
