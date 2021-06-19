# csv-logger

Simple class to log to csv using the logging rotating handler, output is a rolling csv log

Description
-----------
This library allows you to easily log information to CSV file format, in the same fashion as the logging package. This allows you to generate a rolling set of csv logs with a maximum  file size and file count.

Inputs:

* filename
    * main log file name or path. if path, will create subfolders as needed
* level
	* logging level for logs, default INFO
* fmt
	* output format, default '%(asctime)s,%(message)s', accepts 'asctime' 'message' 'levelname'
* datefmt
	* date format for first column of logs, default '%Y/%m/%d %H:%M:%S'
* max_size
	* max size of each log file in bytes, default 10MB (10485760)
* max_files
	* max file count, default 10
* header
	* header to prepend to csv files

Getting started
---------------

Install with ```pip3 install csv_logger```

Basic usage example below.

Since the example is set to only 1kB of data per file, the code results in 2 log files. `log.csv` will always contain the most recent data, and the subsequent files (`log_1.csv` and so on) will have older data.

```python
#!/usr/bin/env python3

from csv_logger import CsvLogger
import logging
from time import sleep
    
LOG_FILE_NAME = 'log.csv'
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s,%(message)s'
LOG_DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
LOG_MAX_SIZE = 1024 # 1 kilobyte
LOG_MAX_FILES = 4 # 4 rotating files
LOG_HEADER = ['date', 'value_1', 'value_2']

# Creat logger with csv rotating handler
csvlogger = CsvLogger(LOG_FILE_NAME, LOG_LEVEL, LOG_FORMAT, LOG_DATE_FORMAT,
    LOG_MAX_SIZE, LOG_MAX_FILES, LOG_HEADER)

# Log some records
for i in range(10):
    csvlogger.info([i, i * 2])
    sleep(0.1)

# You can log list or string
csvlogger.info([1000, 2000])
csvlogger.critical('3000,4000')

# Log some more records to trigger rollover
for i in range(50):
    csvlogger.info([i*2, i ** 2])
    sleep(0.1)
```
`log_1.csv`:
```csv
2021/06/19 09:52:56,0,0
2021/06/19 09:52:56,1,2
2021/06/19 09:52:56,2,4
2021/06/19 09:52:56,3,6
2021/06/19 09:52:56,4,8
2021/06/19 09:52:56,5,10
2021/06/19 09:52:56,6,12
2021/06/19 09:52:56,7,14
2021/06/19 09:52:57,8,16
2021/06/19 09:52:57,9,18
2021/06/19 09:52:57,1000,2000
2021/06/19 09:52:57,3000,4000
2021/06/19 09:52:57,0,0
2021/06/19 09:52:57,2,1
2021/06/19 09:52:57,4,4
2021/06/19 09:52:57,6,9
2021/06/19 09:52:57,8,16
2021/06/19 09:52:57,10,25
2021/06/19 09:52:57,12,36
2021/06/19 09:52:58,14,49
2021/06/19 09:52:58,16,64
2021/06/19 09:52:58,18,81
2021/06/19 09:52:58,20,100
2021/06/19 09:52:58,22,121
2021/06/19 09:52:58,24,144
2021/06/19 09:52:58,26,169
2021/06/19 09:52:58,28,196
2021/06/19 09:52:58,30,225
2021/06/19 09:52:59,32,256
2021/06/19 09:52:59,34,289
2021/06/19 09:52:59,36,324
2021/06/19 09:52:59,38,361
2021/06/19 09:52:59,40,400
2021/06/19 09:52:59,42,441
2021/06/19 09:52:59,44,484
2021/06/19 09:52:59,46,529
2021/06/19 09:52:59,48,576
```
`log.csv`:
```csv
date,value_1,value_2
2021/06/19 09:53:00,50,625
2021/06/19 09:53:00,52,676
2021/06/19 09:53:00,54,729
2021/06/19 09:53:00,56,784
2021/06/19 09:53:00,58,841
2021/06/19 09:53:00,60,900
2021/06/19 09:53:00,62,961
2021/06/19 09:53:00,64,1024
2021/06/19 09:53:00,66,1089
2021/06/19 09:53:00,68,1156
2021/06/19 09:53:01,70,1225
2021/06/19 09:53:01,72,1296
2021/06/19 09:53:01,74,1369
2021/06/19 09:53:01,76,1444
2021/06/19 09:53:01,78,1521
2021/06/19 09:53:01,80,1600
2021/06/19 09:53:01,82,1681
2021/06/19 09:53:01,84,1764
2021/06/19 09:53:01,86,1849
2021/06/19 09:53:02,88,1936
2021/06/19 09:53:02,90,2025
2021/06/19 09:53:02,92,2116
2021/06/19 09:53:02,94,2209
2021/06/19 09:53:02,96,2304
2021/06/19 09:53:02,98,2401
```
Author
-------
* [James Morris](https://morrisjam.es)

License
-------
* Free software: MIT license

Credits
---------
* [Python CSV Rotating Logger gist](https://gist.github.com/arduino12/144c346c9f3ecc8175be45a2f6bda599) as starting point