# Usage
## Examples

### Version

```console
❯ afasi version
Fuzz a language by mixing up only few words. version 2022.10.24+parent.a72a019a
```

### General Help

```console
❯ afasi -h

 Usage: afasi [OPTIONS] COMMAND [ARGS]...

 Fuzz a language by mixing up only few words.
 The translation table entries are applied in order per line of input. So, with large translation tables the
 performance will obviously degrade with a power of two. The latter should be taken as a hint to maintain both
 language files in separate entities not as a patch task.
 The translation table is either an array of two element arrays provided as YAML or JSON and thus shall be in a
 shape like either:
   [
     ["repl", "ace"],
     ["als", "othis"]
   ]

 or:
 ---
 - - repl
   - ace
 - - als
   - othis

 Or the table is given as an object providing more detailed instructions constraining the translation rules
 like:
 * contra indicators - when given exempting a line from translation
 * pro indicators - when given marking a line for translation
 * flip_flop indicators - providing either stop-start (default) or start-stop state switching

 The JSON object format is best understood when executing the template command and adapting the resulting JSON
 object written to standard out.
 Default for input source is standard in and out per default is sent to standard out.

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version  -V        Display the afasi version and exit                                                      │
│ --help     -h        Show this message and exit.                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ template     Write a template of a translation table YAML or JSON structure to standard out and exit         │
│ translate    Translate from a language to a 'langauge'.                                                      │
│ version      Display the afasi version and exit                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

### Translate Help

```console
❯ afasi translate -h

 Usage: afasi translate [OPTIONS] [SOURCE] [TARGET]

 Translate from a language to a 'langauge'.

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│   source      [SOURCE]  [default: STDIN]                                                                     │
│   target      [TARGET]  [default: STDOUT]                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --input   -i      <sourcepath>              Path to input file (default is reading from standard in)         │
│ --output  -o      <targetpath>              Path to non-existing output file (default is writing to standard │
│                                             out)                                                             │
│ --table   -t      <translation table path>  Path to translation table file in YAML or JSON format. Structure │
│                                             of table data is [["repl", "ace"], ["als", "othis"]]             │
│ --dryrun  -n      bool                      Flag to execute without writing the translation but a diff       │
│                                             instead (default is False)                                       │
│ --help    -h                                Show this message and exit.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

### Translate Dryrun

Using files from `test/fixtures/basic/`:

```console
❯ afasi translate minimal-in.xml --table minimal.json --dryrun
2022-10-24T18:28:25.225303+00:00 INFO [AFASI]: dryrun requested
# ---
2022-10-24T18:28:25.226082+00:00 INFO [AFASI]: * resources used:
2022-10-24T18:28:25.226101+00:00 INFO [AFASI]:   - input from:       "test/fixtures/basic/minimal-in.xml"
2022-10-24T18:28:25.226114+00:00 INFO [AFASI]:   - output to:        STDOUT
2022-10-24T18:28:25.226125+00:00 INFO [AFASI]:   - translation from: "test/fixtures/basic/minimal.json"
2022-10-24T18:28:25.226144+00:00 INFO [AFASI]: * translations (in order):
  1. '>Rock' -> '>Lounge'
  2. '>Track' -> '>Rock'

2022-10-24T18:28:25.226560+00:00 INFO [AFASI]: * diff of source to target:
2022-10-24T18:28:25.226625+00:00 INFO [AFASI]: --- SOURCE
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
2022-10-24T18:28:25.226643+00:00 INFO [AFASI]: # ---
```

### Translate

```console
❯ afasi translate minimal-in.xml --table minimal.json --output minimal-out.xml
❯ diff -u minimal-in.xml minimal-out.xml
--- minimal-in.xml	2021-10-20 17:38:28.000000000 +0200
+++ minimal-out.xml	2022-10-24 20:31:30.000000000 +0200
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
Augmented version (object) in YAML format:

```yaml
---
table:
  description: table level default constraints, row attributes do replace those if
    present.
  contra:
  - extracomment
  - source
  count: 0
  flip_is_stop: true
  flip_flop:
  - <message id="SOME_TRACK">
  - </message>
  pro:
  - translation
foo: bar
translations:
- repl: ">Lock"
  ace: ">Launch"
- repl: ">Track"
  ace: ">Lock"
- repl: ">Autotrack"
  ace: ">Autolock"
- repl: lock r
  ace: launch r
- repl: track r
  ace: lock r

```

Same augmented version (object) in JSON format:

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
