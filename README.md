[![Build Status](https://travis-ci.org/carlmatt/personal-data-anonymizer.svg?branch=master)](https://travis-ci.org/carlmatt/personal-data-anonymizer)
[![codecov](https://codecov.io/gh/carlmatt/personal-data-anonymizer/branch/master/graph/badge.svg)](https://codecov.io/gh/carlmatt/personal-data-anonymizer)

# Personal Data Anonymizer

Application for anonymizing personal data. Currently covers:

- General
  - Email addresses

- Finland
  - First and last names
  - Social security numbers
  - Phone numbers (experimental)

## Requirements

The following versions of Python are supported:

- 3.7
- 3.8
- 3.9

## Source data

### Names, Finland

The first and last names in Finland have been obtained from
[here](https://www.avoindata.fi/data/en_GB/dataset/none "Avoindata.fi Finnish names").
The list has been updated on 2020-08-19.

## References

Conjugation of Finnish names based on [this code](http://www.nic.funet.fi/~magi/ohjelmointi/python/hyphen/kieli.py)
by Marko Grönroos (with some modifications).
