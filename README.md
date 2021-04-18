# XpsToTable Converter

Transform Xps data to an easily readable table in xlsx format (Excel).

## How to use it
 - Run the python scrypt with python 3
 - Parameters
    -  -i or --input add your XPS file path
    -  -o or --output add your desired output file path with its name and with .xlsx extension
    -  -r or --replicates add a file with plates informations (describe below)

## Replicates file
- Each line represents a plate
- Each line is compound of:

start_position end_position nb_replicates

## Dependencies
This software uses different python modules:
```
  sys
  getopt
  re
  fitz
    if not loaded use 'pip3 install PyMuPDF'
  numpy
    if not loaded use 'pip3 install numpy'
  xlsxwriter
    if not loaded use 'pip3 install XlsxWriter'
```
