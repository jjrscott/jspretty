import json
import re
import sys
import argparse
import os
from collections import namedtuple

def RGB(red, green, blue):
    value = red * 36 + green * 6 + blue + 16
    return '\033[38;5;'+str(value)+'m'

class Colors:
    KEY = RGB(0, 2, 3)
    COMMENT = RGB(0, 2, 0)
    STRING = RGB(4, 0, 0)
    PLAIN = '\033[0m'
    NULL = RGB(5, 0, 2)
    BOOLEAN = RGB(5, 0, 2)
    NUMBER = RGB(5, 4, 1)

Options = namedtuple('Options', ['maxInlineLength', 'showColors', 'shouldAnnotate', 'hideQuotes'])

def main():
    try:
        defaultMaxInlineLength = os.get_terminal_size().columns
    except:
        defaultMaxInlineLength = 120

    parser = argparse.ArgumentParser(prog='jspretty', description="Format JSON for improved ledgability")
    parser.add_argument('--max-inline-length', default=defaultMaxInlineLength, type=int, help="Maximum length of inlined objects and arrays")
    parser.add_argument('--annotate', dest='shouldAnnotate', default=False, action='store_true', help="Annotate the output")
    parser.add_argument('--hide-quotes', dest='hideQuotes', default=False, action='store_true', help="Show strings without quotes")
    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument('--color', dest='should_colorise', default=sys.stdout.isatty(), action='store_true', help="colorise JSON")
    command_group.add_argument('--monochrome', dest='should_colorise', default=sys.stdout.isatty(), action='store_false', help="monochrome (don't colorise JSON)")

    args = parser.parse_args()

    root = json.loads(sys.stdin.read())
    print(encode(root, options=Options(args.max_inline_length, args.should_colorise, args.shouldAnnotate, args.hideQuotes)))

def encode(node, *nodes, options, isKey=False):
    if isinstance(node, list):
        allPrimitaves = True
        if len(node) == 0:
            return '[ ]'

        for element in node:
            if isinstance(element, list) or isinstance(element, dict):
                allPrimitaves = False
        if allPrimitaves:
            text = '[ ' + ', '.join(map(lambda element: encode(element, node, *nodes, options=options), enumerate(node)))+ ' ]'
            if len(text) < options.maxInlineLength:
                return text

        return '[\n' + ',\n'.join(map(lambda element: indent(element, node, *nodes)+encode(element, node, *nodes, options=options), enumerate(node)))+ '\n'+indent(node, *nodes) + ']'
    elif isinstance(node, dict):
        if len(node) == 0:
            return '{ }'
        allPrimitaves = True
        for value in node.values():
            if isinstance(value, list) or isinstance(value, dict):
                allPrimitaves = False
        if allPrimitaves:
            text = '{ ' + ', '.join(map(lambda item: encode(item[0], node, *nodes, options=options, isKey=True)+': '+encode(item[1], node, *nodes, options=options), sorted(node.items(), key=objectKey)))  + ' }'
            if len(text) < options.maxInlineLength:
                return text

        return '{\n' + ',\n'.join(map(lambda item: encodeItem(item[0], item[1], node, *nodes, options=options), sorted(node.items(), key=objectKey)))  + '\n'+indent(node, *nodes) +'}'
    elif isinstance(node, str):
        return colorise((Colors.KEY if isKey else Colors.STRING), (node if options.hideQuotes else json.dumps(node)), options)
    elif isinstance(node, bool):
        return colorise(Colors.BOOLEAN, json.dumps(node), options)
    elif node is None:
        return colorise(Colors.NULL, json.dumps(node), options)
    elif isinstance(node, tuple):
        if options.shouldAnnotate:
            return colorise(Colors.COMMENT, f'/* {node[0]} */', options)+' '+encode(node[1], *nodes, options=options)
        else:
            return encode(node[1], *nodes, options=options)
    else:
        return colorise(Colors.NUMBER, json.dumps(node), options)

def colorise(color, value, options):
    if options.showColors:
        return color + value + Colors.PLAIN
    else:
        return value

def encodeItem(key, value, node, *nodes, options):
    return indent(key, node, *nodes)+encode(key, node, *nodes, options=options, isKey=True)+': '+encode(value, node, *nodes, options=options)

def indent(node, *nodes):
    return "  " * len(nodes)

def tryInt(value):
    try:
        return int(value)
    except:
        return value

def objectKey(item):
    return list(map(tryInt, filter(lambda element: len(element) > 0, re.split('(\\d+)', item[0].lower()))))

if __name__ == "__main__":
    main()
