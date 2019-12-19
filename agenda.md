# Agenda

* create a imshow template, that is fast to use (good defaults)
	* for image viewing (not quantitative axes)
	* either plane, or with dimension labels
	* optional color bar (with zmin, zmax values, or window leveled)

* create a 2d image matrix class which has the following members
	* xVals (centerd pixel coordinate)
    * yVals (Centered pixel coordinate)

* Update code base using type hints. I do not see a reason to provide python < 3.5 compatibility.

* Provide mpl and python env settings for reproducability (e.g. set up a corresponding *.yml file)

* implement a nice bee scatter algorithm for the data points in 
boxplots

* fast auto-parsing boxplot scripts (plug'n play and robust data loading)

* automated mpl update testing routines

* automated pixel level output image comparison

* automated pdf vector graphic level output image comparison

* Add a markdown guide on how to install custom fonts for matplotlib using macOS and Windows 10. Make this guide for all relevant OS.

* Refactor those parts from the examples that are generic and put them in a deployable lib.

* Add license information for this repository.

* Window / Level plugin for mpl's imshow command

* generic imshow routines

* add adaptive colorbar and autowindow-colorbar functionality

* medical gray scale image using imshow with appropriate colorbar

* Window / Level labels for mpl's colorbars

* Write font guide to use custom fonts within matplotlib.

to pcolor exampels:
* add absolute padding scaling functionality

* specify relative paddingFraction, but w.r.t to the absolute figure size, this makes
more sense
