# jspretty

[jq](https://jqlang.github.io/jq/) does a great job of making JSON data readable. However for large and repetitive data some improvements can be made, eg inlining objects and arrays that only contain primitives and ordering keys by numeric value.

## Example

#### jspretty

![jspretty output](images/jspretty-dark.png#gh-dark-mode-only)
![jspretty output](images/jspretty-light.png#gh-light-mode-only)

#### jq (compact)

![jq -cS output](images/jq-cS-dark.png#gh-dark-mode-only)
![jq -cS output](images/jq-cS-light.png#gh-light-mode-only)

#### jq (pretty-printed)

![jq -S output](images/jq-S-dark.png#gh-dark-mode-only)
![jq -S output](images/jq-S-light.png#gh-light-mode-only)

## Usage

```
usage: jspretty.py [-h] [--max-inline-length MAX_INLINE_LENGTH] [--color | --monochrome]

Format JSON for improved ledgability

options:
  -h, --help            show this help message and exit
  --max-inline-length MAX_INLINE_LENGTH
                        Maximum length of inlined objects and arrays
  --color               colorise JSON
  --monochrome          monochrome (don't colorise JSON)
```
