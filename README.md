# sure-trans
[![pytest](https://github.com/ffreemt/sure-trans/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/sure-trans/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/sure_trans.svg)](https://badge.fury.io/py/sure_trans)

Wrap translators with tenacity, auto-adapt

## Install it

```shell
pip install sure-trans

# pip install git+https://github.com/ffreemt/sure-trans
# poetry add git+https://github.com/ffreemt/sure-trans
# git clone https://github.com/ffreemt/sure-trans && cd sure-trans
```

## Use it
```python
from sure_trans import sure_trans

print(sure_trans("书山有路勤为径", from_language="zh", to_language="en"))
# api used: iciba_api, took 4.57s
# only the diligent will be rewarded by God in their pursuit for knowledge

print(sure_trans("书中自有黄金屋", from_language="zh", to_language="en"))
# api used: caiyun_api, took 1.32s
# The book has its own house of gold

```
