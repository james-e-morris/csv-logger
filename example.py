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