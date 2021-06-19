#!/usr/bin/python3

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