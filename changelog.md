# mpl-benchmarks' changelog

### 2020-07-25 latex preamble
Changes introduced when updating to mpl 3.3.0.

I used to set a latex preamble in python mpl scripts by writing
```python
mpl.rcParams['text.usetex'] = False
mpl.rcParams['mathtext.fontset'] = 'cm'

fontparams = {'text.latex.preamble': [r'\usepackage{cmbright}',
                                      r'\usepackage{amsmath}']}
mpl.rcParams.update(fontparams)
```
Which I now switched to
```python
mpl.rcParams['text.usetex'] = False
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['text.latex.preamble'] = \
    r'\usepackage{cmbright}' + \
    r'\usepackage{amsmath}'
```

### 2019-11-08 using type hints
As of python 3.5, type hints are supported to allow for function annotations.
Below I exemplary show how the function syntax changes when using type hints using the
ticker.py module of this repository. This module contains a function `getLogTicksBase10`,
which has the conventional function signature
```python
def getLogTicksBase10(min, max, comb = np.arange(1, 10)):
    # function body
    return ...
```
This changes to the following below with type hints:
```python
def getLogTicksBase10(min: float, max: float, comb: np.ndarray = np.arange(1, 10)) -> np.ndarray:
    # function body
    return ...
```

### 2019-08-11 date str using datetime
I replaced my old datetime strings in the form of
```python
import datetime
now = datetime.datetime.now()
now = "{}-{}-{}".format(str(now.year), str(now.month).zfill(2), str(now.day).zfill(2)) 
```
by the way more simple
```python
import datetime
today = datetime.datetime.now().strftime("%Y-%m-%d")
```
to get a string variable of today's date in the military format YYYY-MM-DD.
