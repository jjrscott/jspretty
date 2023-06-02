# jspretty

[jq](https://jqlang.github.io/jq/) does a great job of making JSON data readable. However for large and repetitive data some improvements can be made, eg inlining objects and arrays that only contain primitives and ordering keys by numeric value.

### Example

#### Compact

```JSON
{"en5":["Hello","World"],"en10":["Hello","World"],"fr":["Bonjour","Monde"]}
```

#### jq -S

```json
{
  "en10": [
    "Hello",
    "World"
  ],
  "en5": [
    "Hello",
    "World"
  ],
  "fr": [
    "Bonjour",
    "Monde"
  ]
}
```

#### python3 jspretty.py

```json
{
  "en5": [ "Hello", "World" ],
  "en10": [ "Hello", "World" ],
  "fr": [ "Bonjour", "Monde" ]
}
```
