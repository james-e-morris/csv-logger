# csv-logger

Simple class to log to csv using the logging rotating handler, output is a rolling csv log

![csv-logger](https://github.com/Morrious/csv-logger/blob/prod/csv-logger.png?raw=true)

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
#!/usr/bin/python3

from csv_logger import CsvLogger
import logging
from time import sleep

filename = 'logs/log.csv'
level = logging.INFO
fmt = '%(asctime)s,%(message)s'
datefmt = '%Y/%m/%d %H:%M:%S'
max_size = 1024  # 1 kilobyte
max_files = 4  # 4 rotating files
header = ['date', 'value_1', 'value_2']

# Creat logger with csv rotating handler
csvlogger = CsvLogger(filename=filename,
                      level=level,
                      fmt=fmt,
                      datefmt=datefmt,
                      max_size=max_size,
                      max_files=max_files,
                      header=header)

# Log some records
for i in range(10):
    csvlogger.info([i, i * 2])
    sleep(0.1)

# You can log list or string
csvlogger.info([1000.1, 2000.2])
csvlogger.critical('3000,4000')

# Log some more records to trigger rollover
for i in range(50):
    csvlogger.info([i * 2, float(i**2)])
    sleep(0.1)

# Read and print all of the logs from file after logging
all_logs = csvlogger.get_logs(evaluate=True)
for log in all_logs:
    print(log)
```
`log_1.csv`:
```csv
date,value_1,value_2
2021/10/25 12:32:57,0,0
2021/10/25 12:32:57,1,2
2021/10/25 12:32:57,2,4
2021/10/25 12:32:57,3,6
2021/10/25 12:32:57,4,8
2021/10/25 12:32:57,5,10
2021/10/25 12:32:57,6,12
2021/10/25 12:32:57,7,14
2021/10/25 12:32:58,8,16
2021/10/25 12:32:58,9,18
2021/10/25 12:32:58,1000.1,2000.2
2021/10/25 12:32:58,3000,4000
2021/10/25 12:32:58,0,0.0
2021/10/25 12:32:58,2,1.0
2021/10/25 12:32:58,4,4.0
2021/10/25 12:32:58,6,9.0
2021/10/25 12:32:58,8,16.0
2021/10/25 12:32:58,10,25.0
2021/10/25 12:32:58,12,36.0
2021/10/25 12:32:58,14,49.0
2021/10/25 12:32:59,16,64.0
2021/10/25 12:32:59,18,81.0
2021/10/25 12:32:59,20,100.0
2021/10/25 12:32:59,22,121.0
2021/10/25 12:32:59,24,144.0
2021/10/25 12:32:59,26,169.0
2021/10/25 12:32:59,28,196.0
2021/10/25 12:32:59,30,225.0
2021/10/25 12:32:59,32,256.0
2021/10/25 12:32:59,34,289.0
2021/10/25 12:33:00,36,324.0
2021/10/25 12:33:00,38,361.0
2021/10/25 12:33:00,40,400.0
2021/10/25 12:33:00,42,441.0
2021/10/25 12:33:00,44,484.0
2021/10/25 12:33:00,46,529.0
```
`log.csv`:
```csv
date,value_1,value_2
2021/10/25 12:33:00,48,576.0
2021/10/25 12:33:00,50,625.0
2021/10/25 12:33:00,52,676.0
2021/10/25 12:33:00,54,729.0
2021/10/25 12:33:01,56,784.0
2021/10/25 12:33:01,58,841.0
2021/10/25 12:33:01,60,900.0
2021/10/25 12:33:01,62,961.0
2021/10/25 12:33:01,64,1024.0
2021/10/25 12:33:01,66,1089.0
2021/10/25 12:33:01,68,1156.0
2021/10/25 12:33:01,70,1225.0
2021/10/25 12:33:01,72,1296.0
2021/10/25 12:33:01,74,1369.0
2021/10/25 12:33:02,76,1444.0
2021/10/25 12:33:02,78,1521.0
2021/10/25 12:33:02,80,1600.0
2021/10/25 12:33:02,82,1681.0
2021/10/25 12:33:02,84,1764.0
2021/10/25 12:33:02,86,1849.0
2021/10/25 12:33:02,88,1936.0
2021/10/25 12:33:02,90,2025.0
2021/10/25 12:33:02,92,2116.0
2021/10/25 12:33:02,94,2209.0
2021/10/25 12:33:03,96,2304.0
2021/10/25 12:33:03,98,2401.0
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