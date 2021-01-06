# parse-prc-reports
Parse and merge reports from Philippines Red Cross local chapters into one table, to be used for 3W reporting. 

Reports must follow [this format](https://drive.google.com/file/d/1uUliURyV0wn8Y1aq6pBpuxHm8pxeHTWH/view?usp=sharing). Output follows [this other format](https://drive.google.com/file/d/1F77-PW-NRdgfuCuAw095YQUpCQwCSHzw/view?usp=sharing).

## Requirements
* Python > 3.7
* [pandas](https://pypi.org/project/pandas/)
* [click](https://pypi.org/project/click/)

## Usage
Add the reports into one directory named e.g. "input-reports". Then from terminal execute
```
$ python parse_reports --input path/to/input-reports --output final-table.xlsx
```
Documentation
```
Usage: parse_reports.py [OPTIONS]

  merge PRC chapter reports into one table and save it

Options:
  --input TEXT   input directory with chapter reports
  --output TEXT  output (xlsx)
  --help         Show this message and exit.
```
