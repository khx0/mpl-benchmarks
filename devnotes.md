# Development notes

## Python 2 deprecation

As of 2018-03-24 Python 2 support is dropped.
Below I collect parts which do not work with python 2 any longer.

I started using
```
os.makedirs(DIRNAME, exist_ok = True)
```

to replace the custom function
```
def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
```
The exist_ok keyword argument of os.makedirs is not supported by Python 2.7.x. To make the scripts run with Python 2.7.x again you can revert back to the custom ensure_dir function. Most of the core parts of these examples
should continue to work with Python 2.7.x. However I will increasingly neglect this, since I stopped using Python 2.7.x a while ago.