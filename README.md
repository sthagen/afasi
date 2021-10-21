# afasi

[![license](https://img.shields.io/github/license/sthagen/afasi.svg?style=flat)](https://github.com/sthagen/afasi/blob/default/LICENSE)
[![version](https://img.shields.io/pypi/v/afasi.svg?style=flat)](https://pypi.python.org/pypi/afasi/)
[![downloads](https://img.shields.io/pypi/dm/afasi.svg?style=flat)](https://pypi.python.org/pypi/afasi/)
[![wheel](https://img.shields.io/pypi/wheel/afasi.svg?style=flat)](https://pypi.python.org/pypi/afasi/)
[![supported-versions](https://img.shields.io/pypi/pyversions/afasi.svg?style=flat)](https://pypi.python.org/pypi/afasi/)
[![supported-implementations](https://img.shields.io/pypi/implementation/afasi.svg?style=flat)](https://pypi.python.org/pypi/afasi/)

Fuzz a language by mixing up only few words.


## Status

Beta.

**Note**: The default branch is `default`.

# Use

<!-- MarkdownTOC -->

- Examples
  - Version
  - General Help
  - Translate Help
  - Translate Dryrun
  - Translate
  - Example Translation Tables
- Command Line API
- `afasi`
  - `afasi template`
  - `afasi translate`
  - `afasi version`

<!-- /MarkdownTOC -->

## Examples

### Version

```console
$ afasi version
Fuzz a language by mixing up only few words. version 2021.10.22
```

### General Help

```console
$ afasi
Usage: afasi [OPTIONS] COMMAND [ARGS]...

  Fuzz a language by mixing up only few words.

  The translation table entries are applied in order per line of input. So,
  with large translation tables the performance will obviously degrade with a
  power of two. The latter should be taken as a hint to maintain both language
  files in separate entities not as a patch task.

  The translation table is either an array of two element arrays provided as
  JSON and thus shall be in a shape like:

    [
      ["repl", "ace"],
      ["als", "othis"]
    ]

  Or the table is given as an object providing more detailed instructions
  constraining the translation rules like:

  * contra indicators - when given exempting a line from translation
  * pro indicators - when given marking a line for translation
  * flip_flop indicators - providing either stop-start (default) or start-stop state switching

  The JSON object format is best understood when executing the template
  command and adapting the resulting JSON object written to standard out.

  Default for input source is standard in and out per default is sent to
  standard out.

Options:
  -V, --version  Display the afasi version and exit
  -h, --help     Show this message and exit.

Commands:
  template   Write a template of a translation table JSON structure to...
  translate  Translate from a language to a 'langauge'.
  version    Display the afasi version and exit
```

### Translate Help

```console
$ afasi translate -h
Usage: afasi translate [OPTIONS] [SOURCE] [TARGET]

  Translate from a language to a 'langauge'.

Arguments:
  [SOURCE]  [default: STDIN]
  [TARGET]  [default: STDOUT]

Options:
  -i, --input <sourcepath>        Path to input file (default is reading from
                                  standard in)
  -o, --output <targetpath>       Path to non-existing output file (default is
                                  writing to standard out)
  -t, --table <translation table path>
                                  Path to translation table file in JSON
                                  format. Structure of table data is [["repl",
                                  "ace"], ["als", "othis"]]
  -n, --dryrun                    Flag to execute without writing the
                                  translation but a diff instead (default is
                                  False)
  -h, --help                      Show this message and exit.
```

### Translate Dryrun

```console
$ afasi translate minimal-in.xml --table minimal.json --dryrun
dryrun requested
# ---
* resources used:
  - input from:       "minimal-in.xml"
  - output to:        STDOUT
  - translation from: "minimal.json"
* translations (in order):
  1. '>Rock' -> '>Lounge'
  2. '>Track' -> '>Rock'
* diff of source to target:
--- SOURCE
+++ TARGET
@@ -6,12 +6,12 @@
         <message id="SOME_TRACK">
             <source>Some Track</source>
             <extracomment>Does not matter.</extracomment>
-            <translation>Track</translation>
+            <translation>Rock</translation>
         </message>
         <message id="SOME_ROCK">
             <source>Some Rock</source>
             <extracomment>Does not matter.</extracomment>
-            <translation>Rock</translation>
+            <translation>Lounge</translation>
         </message>
     </context>
 </TS>
# ---
```

### Translate

```console
$ afasi translate --input minimal-in.xml --output minimal-out.xml --table minimal.json
$ afasi % diff -u minimal-*.xml
--- minimal-in.xml  2021-10-20 20:12:54.000000000 +0200
+++ minimal-out.xml 2021-10-20 20:14:45.000000000 +0200
@@ -6,12 +6,12 @@
         <message id="SOME_TRACK">
             <source>Some Track</source>
             <extracomment>Does not matter.</extracomment>
-            <translation>Track</translation>
+            <translation>Rock</translation>
         </message>
         <message id="SOME_ROCK">
             <source>Some Rock</source>
             <extracomment>Does not matter.</extracomment>
-            <translation>Rock</translation>
+            <translation>Lounge</translation>
         </message>
     </context>
 </TS>
```

### Example Translation Tables

Simple version (parallel arrays):

```json
[
  [">Rock", ">Lounge"],
  [">Track", ">Rock"]
]
```

Augmented version (object):

```json
{
  "table": {
    "description": "table level default constraints, row attributes do replace those if present.",
    "contra": [
      "extracomment",
      "source"
    ],
    "count": 0,
    "flip_is_stop": true,
    "flip_flop": [
      "<message id=\"SOME_TRACK\">",
      "</message>"
    ],
    "pro": [
      "translation"
    ]
  },
  "foo": "bar",
  "translations": [
    {
      "repl": ">Lock",
      "ace": ">Launch"
    },
    {
      "repl": ">Track",
      "ace": ">Lock"
    },
    {
      "repl": ">Autotrack",
      "ace": ">Autolock"
    },
    {
      "repl": "lock r",
      "ace": "launch r"
    },
    {
      "repl": "track r",
      "ace": "lock r"
    }
  ]
}
```

# Command Line API

<!-- MarkdownTOC -->

- `afasi`
  - `afasi template`
  - `afasi translate`
  - `afasi version`

<!-- /MarkdownTOC -->

## `afasi`

Fuzz a language by mixing up only few words.

The translation table entries are applied in order per line of input.
So, with large translation tables the performance will obviously degrade with a power of two.
The latter should be taken as a hint to maintain both language files in separate entities not as a patch task.

The translation table is either an array of two element arrays provided as JSON and thus shall be in a shape like:

```json
  [
    ["repl", "ace"],
    ["als", "othis"]
  ]
```

Or the table is given as an object providing more detailed instructions constraining the translation rules like:

* contra indicators - when given exempting a line from translation
* pro indicators - when given marking a line for translation
* flip_flop indicators - providing either stop-start (default) or start-stop state switching

The JSON object format is best understood when executing the template command and adapting the resulting JSON
object written to standard out.

Default for input source is standard in and out per default is sent to standard out.

**Usage**:

```console
$ afasi [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-V, --version`: Display the afasi version and exit  [default: False]
* `-h, --help`: Show this message and exit.

**Commands**:

* `template`: Write a template of a translation table JSON...
* `translate`: Translate from a language to a 'langauge'.
* `version`: Display the afasi version and exit

### `afasi template`

Write a template of a translation table JSON structure to standard out and exit

**Usage**:

```console
$ afasi template [OPTIONS]
```

**Options**:

* `-h, --help`: Show this message and exit.

### `afasi translate`

Translate from a language to a 'langauge'.

**Usage**:

```console
$ afasi translate [OPTIONS] [SOURCE] [TARGET]
```

**Arguments**:

* `[SOURCE]`: [default: STDIN]
* `[TARGET]`: [default: STDOUT]

**Options**:

* `-i, --input <sourcepath>`: Path to input file (default is reading from standard in)  [default: ]
* `-o, --output <targetpath>`: Path to non-existing output file (default is writing to standard out)  [default: ]
* `-t, --table <translation table path>`: Path to translation table file in JSON format.
Structure of table data is [["repl", "ace"], ["als", "othis"]]  [default: ]
* `-n, --dryrun`: Flag to execute without writing the translation but a diff instead (default is False)  [default: False]
* `-h, --help`: Show this message and exit.

### `afasi version`

Display the afasi version and exit

**Usage**:

```console
$ afasi version [OPTIONS]
```

**Options**:

* `-h, --help`: Show this message and exit.
