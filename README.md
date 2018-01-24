# README.md

## Description
Package to operate the Scanse Sweep scanner, and a Maxbotix sonic ranger with python from a raspberrypi.

Written by S. Filhol, August 2017

## Installation
See Zim notes



## Usage

```bash
# perform 20 scans with Sweep
python sweep_collect.py -nbscans 20

# perform 30 measurement from the maxbotix
python maxbotix_collect.py -nbm 30

```





## Idea, TODOs

- TODO: problem with the database initialization function
- Add module to convert data from cylindrical to cartesian coordinate, add colum to table
- currently, the path to database is hardcoded, see how to pass it as an argument
- redesign code to avoid using the Pandas library
- ...
