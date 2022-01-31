# csv-logger

[![Publish to PyPI](https://github.com/morrious/csv-logger/actions/workflows/python-publish.yml/badge.svg)](https://pypi.org/project/csv-logger/) [![Downloads](https://pepy.tech/badge/csv-logger)](https://pepy.tech/project/csv-logger)

Simple class to log to csv using the logging rotating handler, output is a rolling csv log

![csv-logger](https://github.com/Morrious/csv-logger/blob/prod/csv-logger.png?raw=true)

Description
-----------
This library allows you to easily log information to CSV file format, in the same fashion as the logging package. This allows you to generate a rolling set of csv logs with a maximum  file size and file count.

Inputs:

* filename
    * main log file name or path. if path, will create subfolders as needed
* level
	* logging level for logs, below which the logs will not be written to file. default `INFO`
* add_level_names
    * list fo strings, adds additional logging levels for custom log tagging. default: `[]`
* add_level_nums
    * assigns specific nums to `add_level_names`. default if None provided: `[100,99,98,..]`
* fmt
	* output format. default `%(asctime)s,%(message)s`. accepts:
        - `%(name)s`            Name of the logger (logging channel)
        - `%(levelno)s`         Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        - `%(levelname)s`       Text logging level for the message ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
        - `%(pathname)s`        Full pathname of the source file where the logging call was issued (if available)
        - `%(filename)s`        Filename portion of pathname
        - `%(module)s`          Module (name portion of filename)
        - `%(lineno)d`          Source line number where the logging call was issued (if available)
        - `%(funcName)s`        Function name
        - `%(created)f`         Time when the LogRecord was created (time.time() return value)
        - `%(asctime)s`         Textual time when the LogRecord was created
        - `%(msecs)d`           Millisecond portion of the creation time
        - `%(relativeCreated)d` Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded (typically at application startup time)
        - `%(thread)d`          Thread ID (if available)
        - `%(threadName)s`      Thread name (if available)
        - `%(process)d`         Process ID (if available)
        - `%(message)s`         The result of record.getMessage(), computed just as the record is emitted
* datefmt
	* date format for first column of logs. default `%Y/%m/%d %H:%M:%S`
* max_size
	* max size of each log file in bytes. default `10MB` (10,485,760)
* max_files
	* max file count. default `10`
* header
	* header to prepend to csv files. default `None`

Getting started
---------------

Install with ```pip3 install csv_logger```

Basic usage example below.

Since the example is set to only 1kB of data per file, the code results in 2 log files. `log.csv` will always contain the most recent data, and the subsequent files (`log_1.csv` and so on) will have older data.

```python
#!/usr/bin/python3

from csv_logger import CsvLogger
import logging
from time import sleep

filename = 'logs/log.csv'
level = logging.INFO
custom_additional_levels = ['logs_a', 'logs_b', 'logs_c']
fmt = '%(asctime)s,%(levelname)s,%(message)s'
datefmt = '%Y/%m/%d %H:%M:%S'
max_size = 1024  # 1 kilobyte
max_files = 4  # 4 rotating files
header = ['date', 'level', 'value_1', 'value_2']

# Creat logger with csv rotating handler
csvlogger = CsvLogger(filename=filename,
                      level=level,
                      add_level_names=custom_additional_levels,
                      add_level_nums=None,
                      fmt=fmt,
                      datefmt=datefmt,
                      max_size=max_size,
                      max_files=max_files,
                      header=header)

# Log some records
for i in range(10):
    csvlogger.logs_a([i, i * 2])
    sleep(0.1)

# You can log list or string
csvlogger.logs_b([1000.1, 2000.2])
csvlogger.critical('3000,4000')

# Log some more records to trigger rollover
for i in range(50):
    csvlogger.logs_c([i * 2, float(i**2)])
    sleep(0.1)

# Read and print all of the logs from file after logging
all_logs = csvlogger.get_logs(evaluate=False)
for log in all_logs:
    print(log)
```

`log_2.csv`:
```csv
date,level,value_1,value_2
2022/01/31 15:49:53,logs_a,0,0
2022/01/31 15:49:53,logs_a,1,2
2022/01/31 15:49:53,logs_a,2,4
2022/01/31 15:49:53,logs_a,3,6
2022/01/31 15:49:53,logs_a,4,8
2022/01/31 15:49:53,logs_a,5,10
2022/01/31 15:49:53,logs_a,6,12
2022/01/31 15:49:53,logs_a,7,14
2022/01/31 15:49:53,logs_a,8,16
2022/01/31 15:49:54,logs_a,9,18
2022/01/31 15:49:54,logs_b,1000.1,2000.2
2022/01/31 15:49:54,CRITICAL,3000,4000
2022/01/31 15:49:54,logs_c,0,0.0
2022/01/31 15:49:54,logs_c,2,1.0
2022/01/31 15:49:54,logs_c,4,4.0
2022/01/31 15:49:54,logs_c,6,9.0
2022/01/31 15:49:54,logs_c,8,16.0
2022/01/31 15:49:54,logs_c,10,25.0
2022/01/31 15:49:54,logs_c,12,36.0
2022/01/31 15:49:54,logs_c,14,49.0
2022/01/31 15:49:54,logs_c,16,64.0
2022/01/31 15:49:55,logs_c,18,81.0
2022/01/31 15:49:55,logs_c,20,100.0
2022/01/31 15:49:55,logs_c,22,121.0
2022/01/31 15:49:55,logs_c,24,144.0
2022/01/31 15:49:55,logs_c,26,169.0
2022/01/31 15:49:55,logs_c,28,196.0
2022/01/31 15:49:55,logs_c,30,225.0
2022/01/31 15:49:55,logs_c,32,256.0
```

`log_1.csv`:
```csv
date,level,value_1,value_2
2022/01/31 15:49:55,logs_c,34,289.0
2022/01/31 15:49:55,logs_c,36,324.0
2022/01/31 15:49:56,logs_c,38,361.0
2022/01/31 15:49:56,logs_c,40,400.0
2022/01/31 15:49:56,logs_c,42,441.0
2022/01/31 15:49:56,logs_c,44,484.0
2022/01/31 15:49:56,logs_c,46,529.0
2022/01/31 15:49:56,logs_c,48,576.0
2022/01/31 15:49:56,logs_c,50,625.0
2022/01/31 15:49:56,logs_c,52,676.0
2022/01/31 15:49:56,logs_c,54,729.0
2022/01/31 15:49:57,logs_c,56,784.0
2022/01/31 15:49:57,logs_c,58,841.0
2022/01/31 15:49:57,logs_c,60,900.0
2022/01/31 15:49:57,logs_c,62,961.0
2022/01/31 15:49:57,logs_c,64,1024.0
2022/01/31 15:49:57,logs_c,66,1089.0
2022/01/31 15:49:57,logs_c,68,1156.0
2022/01/31 15:49:57,logs_c,70,1225.0
2022/01/31 15:49:57,logs_c,72,1296.0
2022/01/31 15:49:57,logs_c,74,1369.0
2022/01/31 15:49:58,logs_c,76,1444.0
2022/01/31 15:49:58,logs_c,78,1521.0
2022/01/31 15:49:58,logs_c,80,1600.0
2022/01/31 15:49:58,logs_c,82,1681.0
2022/01/31 15:49:58,logs_c,84,1764.0
2022/01/31 15:49:58,logs_c,86,1849.0
```
`log.csv`:
```csv
date,level,value_1,value_2
2022/01/31 15:49:58,logs_c,88,1936.0
2022/01/31 15:49:58,logs_c,90,2025.0
2022/01/31 15:49:58,logs_c,92,2116.0
2022/01/31 15:49:58,logs_c,94,2209.0
2022/01/31 15:49:59,logs_c,96,2304.0
2022/01/31 15:49:59,logs_c,98,2401.0
```
Author
-------
* James Morris (https://james.pizza)

License
-------
* Free software: MIT license

Credits
---------
* [Python CSV Rotating Logger gist](https://gist.github.com/arduino12/144c346c9f3ecc8175be45a2f6bda599) as starting point