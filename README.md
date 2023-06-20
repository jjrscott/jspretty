# jspretty

[jq](https://jqlang.github.io/jq/) does a great job of making JSON data readable. However for large and repetitive data some improvements can be made, eg inlining objects and arrays that only contain primitives and ordering keys by numeric value.

## Example

#### jspretty

![jspretty output](images/jspretty-dark.png#gh-dark-mode-only)
![jspretty output](images/jspretty-light.png#gh-light-mode-only)

#### jspretty (annotated)

![jspretty output](images/jspretty-annotate-dark.png#gh-dark-mode-only)
![jspretty output](images/jspretty-annotate-light.png#gh-light-mode-only)

#### jspretty (hiding quotes)

![jspretty output](images/jspretty-hide-quotes-dark.png#gh-dark-mode-only)
![jspretty output](images/jspretty-hide-quotes-light.png#gh-light-mode-only)


## Usage

```
usage: jspretty [-h] [--max-inline-length MAX_INLINE_LENGTH] [--annotate] [--hide-quotes] [--color | --monochrome]

Format JSON for improved ledgability

options:
  -h, --help            show this help message and exit
  --max-inline-length MAX_INLINE_LENGTH
                        Maximum length of inlined objects and arrays
  --annotate            Annotate the output
  --hide-quotes         Show strings without quotes
  --color               colorise JSON
  --monochrome          monochrome (don't colorise JSON)
```
