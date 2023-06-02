import json
import re
import sys


def main():
    root = json.loads(sys.stdin.read())

    print(encode(root))

def encode(node, *nodes):
    if isinstance(node, list):
        allPrimitaves = True
        for element in node:
            if isinstance(element, list) or isinstance(element, dict):
                allPrimitaves = False
        if allPrimitaves:
            return '[ ' + ', '.join(map(lambda element: encode(element, node, *nodes), node))+ ' ]'
        else:
            return '[\n' + ',\n'.join(map(lambda element: indent(element, node, *nodes)+encode(element, node, *nodes), node))+ '\n'+indent(node, *nodes) + ']'
    elif isinstance(node, dict):
        allPrimitaves = True
        for value in node.values():
            if isinstance(value, list) or isinstance(value, dict):
                allPrimitaves = False
        maxKeyLength = max(map(len, node))
        if allPrimitaves:
            return '{ ' + ', '.join(map(lambda item: encode(item[0], node, *nodes)+': '+encode(item[1], node, *nodes), sorted(node.items(), key=objectKey)))  + ' }'
        else:
            return '{\n' + ',\n'.join(map(lambda item: encodeItem(item[0], item[1], maxKeyLength, node, *nodes), sorted(node.items(), key=objectKey)))  + '\n'+indent(node, *nodes) +'}'
    elif isinstance(node, str):
        return '"'+node+'"'
    elif isinstance(node, bool):
        return 'true' if node else 'false'
    elif node is None:
        return 'null'
    else:
        # exit(type(node))
        return str(node)

def encodeItem(key, value, maxKeyLength, node, *nodes):
    return indent(key, node, *nodes)+encode(key, node, *nodes)+': '+encode(value, node, *nodes)

def indent(node, *nodes):
    return "  " * len(nodes)

def objectKey(item):
    foo = re.split('\\d+', item[0].upper())
    # print(foo)
    return foo

if __name__ == "__main__":
    main()
