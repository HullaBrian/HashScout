# HashScout
Application to recursively hash every file in a directory or .zip

HashScout works best on Windows with 7zip already installed!

# Contents
- [Usage](#usage)
  - [Help Menu](#help-menu)
  - [From Zip](#from-zip)
  - [From Directory](#from-directory)
- [Output](#output)

# Usage
## Help Menu
```
> python hscout --help
usage: HashScout [-h] [-a ALGORITHM] [-p PASSWORD] input

A tool to get hashes of all files in a directory or .zip

positional arguments:
  input                 input zip file or directory

options:
  -h, --help            show this help message and exit
  -a ALGORITHM, --algorithm ALGORITHM
                        hashing algorithm to use [SHA256|MD5]
  -p PASSWORD, --password PASSWORD
                        password to use for unlocking a zip

Project repository: https://github.com/HullaBrian/HashScout
```
## From Zip
To extract files from a zip file, use the following:
```commandline
python hscout INPUT -p PASSWORD
```
Ensure that you replace `INPUT` with the zip file you want to use, and `PASSWORD`
with the password you'd like to use, although it is optional

## From Directory
```commandline
python hscout INPUT
```
Ensure that you replace `INPUT` with the directory that you'd like to traverse

# Output
HashScout will output the resulting file path(s) and their respective hashes
into a `.csv` file in the same parent directory in which they were extracted.