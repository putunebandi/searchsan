# searchsan

[![made-with-Python](https://img.shields.io/badge/made%20with-Python-blue.svg)](https://www.python.org/)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![issues](https://img.shields.io/github/issues/putunebandi/searchsan?color=blue)](https://github.com/putunebandi/searchsan/issues)

<p align="center">
  <img src="banner.png" alt="Searchsan Logo" width="60%">
</p>

Efficient Python tool crafted for conducting bulk Google searches seamlessly, powered by the serper.dev API.

---

## Resources

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```bash
git clone https://github.com/putunebandi/searchsan && cd searchsan
python -m pip install PyYAML
```

## Usage
```text
python searchsan.py -h
```
This will display all the options that can be used.
```text
usage: searchsan.py [-h] -ql QUERYLIST -t NUMTHREAD [-o SAVEOUTPUT] [-exdom] [-maxpage MAXPAGE] [-perpage PERPAGE]
                    [-country COUNTRY] [-language LANGUAGE] [-show]

options:
  -h, --help            show this help message and exit
  -ql QUERYLIST, --query-list QUERYLIST
                        Input file with a list of query
  -t NUMTHREAD, --threads NUMTHREAD
                        Number of threads
  -o SAVEOUTPUT, --output SAVEOUTPUT
                        Output file to write found links
  -exdom, --extract-domain
                        Extract and filter unique domains
  -maxpage MAXPAGE, --maxpage MAXPAGE
                        Set the maximum page number (default: max of the page or 20 pages)
  -perpage PERPAGE, --perpage PERPAGE
                        Set result urls per page (default: 100)
  -country COUNTRY, --country COUNTRY
                        Set search by country (default: us)
  -language LANGUAGE, --language LANGUAGE
                        Set search by language (default: en)
  -show, --show         Print text results
```

## License

Please see the [LICENSE file](LICENSE) for more information.
