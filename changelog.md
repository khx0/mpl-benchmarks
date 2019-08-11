# mpl-benchmarks changelog

### 2019-08-11
I replaced my old datetime strings in the form of
```
import datetime
now = datetime.datetime.now()
now = "{}-{}-{}".format(str(now.year), str(now.month).zfill(2), str(now.day).zfill(2)) 
```
by the way more simple
```
today = datetime.datetime.now().strftime("%Y-%m-%d")
```
.