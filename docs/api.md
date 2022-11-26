# Command Line API

## `afasi`

Fuzz a language by mixing up only few words.

The translation table entries are applied in order per line of input.
So, with large translation tables the performance will obviously degrade with a power of two.
The latter should be taken as a hint to maintain both language files in separate entities not as a patch task.

The translation table is either an array of two element arrays provided as YAML or JSON
and thus shall be in a shape like either:

```json
  [
    ["repl", "ace"],
    ["als", "othis"]
  ]
```

or:

```yaml
---
- - repl
  - ace
- - als
  - othis
```

Or the table is given as an object providing more detailed instructions constraining the translation rules like:

* contra indicators - when given exempting a line from translation
* pro indicators - when given marking a line for translation
* flip_flop indicators - providing either stop-start (default) or start-stop state switching

The YAML or JSON object format is best understood when executing the template command and adapting the resulting
respective YAML document or JSON object written to standard out.

Default for input source is standard in and out per default is sent to standard out.

**Usage**:

```console
❯ afasi [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-V, --version`: Display the afasi version and exit  [default: False]
* `-h, --help`: Show this message and exit.

**Commands**:

* `template`: Write a template of a translation table YAML or JSON...
* `translate`: Translate from a language to a 'langauge'.
* `version`: Display the afasi version and exit

### `afasi template`

Write a template of a translation table JSON structure to standard out and exit

**Usage**:

```console
❯ afasi template [OPTIONS]
```

**Options**:

* `-h, --help`: Show this message and exit.

### `afasi translate`

Translate from a language to a 'langauge'.

**Usage**:

```console
❯ afasi translate [OPTIONS] [SOURCE] [TARGET]
```

**Arguments**:

* `[SOURCE]`: [default: STDIN]
* `[TARGET]`: [default: STDOUT]

**Options**:

* `-i, --input <sourcepath>`: Path to input file (default is reading from standard in)  [default: ]
* `-o, --output <targetpath>`: Path to non-existing output file (default is writing to standard out)  [default: ]
* `-t, --table <translation table path>`: Path to translation table file in YAML or JSON format.
Structure of table data is [["repl", "ace"], ["als", "othis"]]  [default: ]
* `-n, --dryrun`: Flag to execute without writing the translation but a diff instead (default is False)  [default: False]
* `-h, --help`: Show this message and exit.

### `afasi version`

Display the afasi version and exit

**Usage**:

```console
❯ afasi version [OPTIONS]
```

**Options**:

* `-h, --help`: Show this message and exit.

