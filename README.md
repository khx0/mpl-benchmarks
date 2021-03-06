# mpl-benchmarks
Useful matplotlib snippets, plotting routines and template scripts.
The examples herein illustrate many advanced matplotlib features by using them in a
concrete context. This repository collects such examples,
to provide them for easy reusability and as interesting showcases with the hope
that they might prove to be useful for other interested parties.
This repository consist of many examples which can also be understood as
template plot scripts for different plotting scenarios.
In particular, many of these are meant to illustrate how much potential matplotlib
has if one goes beyond the defaults.

For some cases both a full and minimal version of the same plotting example is provided.
The full versions are often heavily customized, whilst the minimal
versions are meant to be minimal requirement python scripts that focus on
a single issue, without further ado.

### Example: 2d correlation plot with marginal densities

![Demo3](/mpl_correlation2d_with_marginals/demo_composition.png)

The python scripts which produce the above example are placed in
```
/mpl_correlation2d_with_marginals
```

### Example: pseudo color plot (mpl's pcolormesh)

![Demo2](/mpl_heatmap_log_xy-scale/demo/out/pcolor_showcase_figure_composition.png)

The python script which produces the above two figures can be found under
```
/mpl_heatmap_log_xy-scale/demo
```

### Example: pcolormesh pseudo color plot

For visualizing small 2d matrices, this pcolormesh assay illustrates a nice way how to create fixed size figures with constant relative margins between data and figure borders. In this way the created panels can be nicely integrated into larger arrays and appear all homogeneously in terms of figure size, margins, borders and figure labels. This approach seems suitable for rather small matrices (around n < 64). For full image viewing matplotlib's imshow command seems more appropriate and up to the task.

![Demo1](/mpl_pcolormesh_with_fixed_size_and_relative_border_margins/demonstration/pcolormesh_array_composition_2019-12-16.png)

The script which produces the shown panels is located in 
```
/mpl_pcolormesh_with_fixed_size_and_relative_border_margins
```

### Example: scatter plot with data labels

The example below shows how to create a scatter plot with data lables using nice power of ten string formatting both for the data labels and for the scientific y-axis scaling.

![Demo4](/mpl_scatter_plot_with_data_labels/demo/composition_per_2021-02-22.png)

The script which produces the above figure is located in
```
/mpl_scatter_plot_with_data_labels
```

## Python and matplotlib versions
All shown examples have been tested with Python 3 (version 3.7.6)
and matplotlib version 3.4.1. Update to matplotlib 3.4.2 in progress.
Support for Python 2 is dropped.
However copying some snippets from the scripts will
most likely also (still) work with Python 2.7, as they were originally
developed using Python 2.7 starting with matplotlib 2.2.3.

### Testing
For some modules unit tests are provided in the
```
/unit-tests
```
directory which can be run using the unittest module or via pytest.
All tests were done using pytest version 6.1.2.

### Changes
For changes made to this repository see the provided `changelog.md` file in root.
