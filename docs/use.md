# Use

<!-- MarkdownTOC -->

- Examples
  - Version
  - General Help
  - Translate Help
  - Translate Dryrun
  - Translate
  - Example Translation Table

<!-- /MarkdownTOC -->

## Examples

### Version

```console
$ afasi version
Fuzz a language by mixing up only few words. version 2021.10.21
```

### General Help

```console
$ afasi
Usage: afasi [OPTIONS] COMMAND [ARGS]...

  Fuzz a language by mixing up only few words.

  The translation table entries are applied in order per line of input. So,
  with large translation tables the performance will obviously degrade with
  a power of two. The latter should be taken as a hint to maintain both
  language files in separate entities not as a patch task.

  The translation table is an array or two element arrays provided as JSON
  and thus shall be in a shape like:

    [
      ["repl", "ace"],
      ["als", "othis"]
    ]

  Default for input source is standard in and out per default is sent to
  standard out.

Options:
  -V, --version  Display the afasi version and exit  [default: False]
  -h, --help     Show this message and exit.

Commands:
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
                                  standard in)  [default: ]

  -o, --output <targetpath>       Path to non-existing output file (default is
                                  writing to standard out)  [default: ]

  -t, --table <translation table path>
                                  Path to translation table file in JSON
                                  format. Structure of table data is [["repl",
                                  "ace"], ["als", "othis"]]  [default: ]

  -n, --dryrun                    Flag to execute without writing the
                                  translation but a diff instead (default is
                                  False)  [default: False]

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

### Example Translation Table

```json
[
  [">Rock", ">Lounge"],
  [">Track", ">Rock"]
]
```
