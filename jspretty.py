import json
import re
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Format JSON for improved ledgability")
    parser.add_argument('--max-inline-length', default=120, type=int, help="Maximum length of inlined objects and arrays")

    args = parser.parse_args()

    root = json.loads(sys.stdin.read())
    print(encode(root, maxInlineLength=args.max_inline_length))

def encode(node, *nodes, maxInlineLength):
    if isinstance(node, list):
        allPrimitaves = True
        for element in node:
            if isinstance(element, list) or isinstance(element, dict):
                allPrimitaves = False
        if allPrimitaves:
            text = '[ ' + ', '.join(map(lambda element: encode(element, node, *nodes, maxInlineLength=maxInlineLength), node))+ ' ]'
            if len(text) < maxInlineLength:
                return text

        return '[\n' + ',\n'.join(map(lambda element: indent(element, node, *nodes)+encode(element, node, *nodes, maxInlineLength=maxInlineLength), node))+ '\n'+indent(node, *nodes) + ']'
    elif isinstance(node, dict):
        allPrimitaves = True
        for value in node.values():
            if isinstance(value, list) or isinstance(value, dict):
                allPrimitaves = False
        if allPrimitaves:
            text = '{ ' + ', '.join(map(lambda item: encode(item[0], node, *nodes, maxInlineLength=maxInlineLength)+': '+encode(item[1], node, *nodes, maxInlineLength=maxInlineLength), sorted(node.items(), key=objectKey)))  + ' }'
            if len(text) < maxInlineLength:
                return text

        return '{\n' + ',\n'.join(map(lambda item: encodeItem(item[0], item[1], node, *nodes, maxInlineLength=maxInlineLength), sorted(node.items(), key=objectKey)))  + '\n'+indent(node, *nodes) +'}'
    elif isinstance(node, str):
        return '"'+node+'"'
    elif isinstance(node, bool):
        return 'true' if node else 'false'
    elif node is None:
        return 'null'
    else:
        # exit(type(node))
        return str(node)

def encodeItem(key, value, node, *nodes, maxInlineLength):
    return indent(key, node, *nodes)+encode(key, node, *nodes, maxInlineLength=maxInlineLength)+': '+encode(value, node, *nodes, maxInlineLength=maxInlineLength)

def indent(node, *nodes):
    return "  " * len(nodes)

def objectKey(item):
    return list(filter(lambda element: len(element) > 0, re.split('(\\d+)', item[0].lower())))

if __name__ == "__main__":
    main()
