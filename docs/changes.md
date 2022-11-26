# Changelog

## 2022.11.26

* Added translation table processing for YAML (new default)
* Reduced supported python versions to 3.10 and 3.11 (or higher)

## 2022.10.24

* Migrated to pyproject.toml for packaging and logging for, well, logging

## 2021.10.28

* Happy linter, happy winter

## 2021.10.22

* Resolved feedback from friendly users
* Added new command `template` to ease use of augmented translation table syntax
* Simplified internal operation and reduced warning noise
* Documented new features and data structures
* Outer test line coverage again complete
* New: Contra indicators - when given exempting a line from translation
* New: Pro indicators - when given marking a line for translation
* New: Flip-Flop indicators - providing either stop-start (default) or start-stop state switching
* Refactored tests to use pytest tmp_path fixture to stabilize the tests
* Removed prototype data and tests from table implemenbtation

## 2021.10.21

* Resolved feedback from friendly users
* Created initial documentation set covering API and examples of use
* Fixed python version dependency to be consistently 3.8, 3.9, and 3.10

## 2021.10.20

* Initial release to pypi
