# mpl-benchmarks
Useful matplotlib snippets, plotting routines and template scripts.
The examples herein illustrate many advanced matplotlib features by using them in a
concrete context. This repository is used to collect such examples,
to provide them for easy reusability and as interesting showcases with the hope
that they might prove to be useful for interested other parties.
This repository consist of many examples which can also be understood as
template plot scripts for different plotting scenarios.
In particular, many of these are meant to illustrate how much potential matplotlib 
has if one goes beyond the defaults.

For some cases both a full and minimal version of the same plotting example is provided.
The full versions are often heavily customized, whilst the minimal
versions are meant to be minimal requirement python scripts that focus on
a single issue, without further ado.

## Python and matplotlib versions
All shown examples have been tested both with python 3 (version 3.7.2)
and python 2 (version 2.7.15).
* Python 2.7.15, Matplotlib 2.2.3
* Python 3.7.2,  Matplotlib 3.0.3

### Example pseudo color plot

![Demo](/mpl_heatmap_log_xy-scale/demo/out/pcolor_showcase_figure_composition.png)

The python script which produces the above two figures can be found under
```
/mpl_heatmap_log_xy-scale/demo/
```

<<<<<<< HEAD
### Testing
=======
### Testting
>>>>>>> 5de7217d2dded24616ed069e8714c08532ca7e02
For some modules unit tests are provided in the
```
/unit-tests/
```
directory which can be run using the unittest module or via pytest.
All tests were done using pytest version 4.3.1.