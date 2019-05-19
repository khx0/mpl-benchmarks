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
All shown examples have been tested with python 3 (version 3.7.2)
and matplotlib version 3.0.3.
The update to matplotlib version 3.1.0 is ongoing.
Support for Python 2 is dropped.
However copying some snippets from the scripts will
most likely also work with Python 2.7, as they were originally
developed using python 2.7 and matplotlib 2.2.3.

### Example pseudo color plot

![Demo](/mpl_heatmap_log_xy-scale/demo/out/pcolor_showcase_figure_composition.png)

The python script which produces the above two figures can be found under
```
/mpl_heatmap_log_xy-scale/demo/
```

### Example 2d correlation plot with marginal densities

![Demo2](/mpl_correlation2d_with_marginals/out/demo_composition.png)

The python scripts which produce the above example are placed in
```
/mpl_correlation2d_with_marginals/
```

### Testing
For some modules unit tests are provided in the
```
/unit-tests/
```
directory which can be run using the unittest module or via pytest.
All tests were done using pytest version 4.3.1.
