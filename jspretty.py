import json
import re
import sys
import argparse
import os
from collections import namedtuple

class Colors:
    KEY = '\033[38;5;31m'
    COMMENT = '\032[38;5;28m'
    STRING = '\033[38;5;160m'
    PLAIN = '\033[0m'
    KEYWORD = '\033[38;5;198m'
    NUMBER = '\033[38;5;221m'

Options = namedtuple('Options', ['maxInlineLength', 'showColors'])

def main():
    parser = argparse.ArgumentParser(description="Format JSON for improved ledgability")
    parser.add_argument('--max-inline-length', default=120, type=int, help="Maximum length of inlined objects and arrays")
    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument('--color', dest='should_colorise', default=sys.stdout.isatty(), action='store_true', help="colorise JSON")
    command_group.add_argument('--monochrome', dest='should_colorise', default=sys.stdout.isatty(), action='store_false', help="monochrome (don't colorise JSON)")

    args = parser.parse_args()

    root = json.loads(sys.stdin.read())
    print(encode(root, options=Options(args.max_inline_length, args.should_colorise)))

def encode(node, *nodes, options, isKey=False):
    if isinstance(node, list):
        allPrimitaves = True
        for element in node:
            if isinstance(element, list) or isinstance(element, dict):
                allPrimitaves = False
        if allPrimitaves:
            text = '[ ' + ', '.join(map(lambda element: encode(element, node, *nodes, options=options), node))+ ' ]'
            if len(text) < options.maxInlineLength:
                return text

        return '[\n' + ',\n'.join(map(lambda element: indent(element, node, *nodes)+encode(element, node, *nodes, options=options), node))+ '\n'+indent(node, *nodes) + ']'
    elif isinstance(node, dict):
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
        return colorise((Colors.KEY if isKey else Colors.STRING), '"'+node.replace('\n','\\n')+'"', options)
    elif isinstance(node, bool):
        return colorise(Colors.KEYWORD, ('true' if node else 'false'), options)
    elif node is None:
        return colorise(Colors.KEYWORD, 'null', options)
    else:
        return colorise(Colors.NUMBER, str(node), options)

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
