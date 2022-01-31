#!/usr/bin/python3

import logging
from logging.handlers import RotatingFileHandler
from os import makedirs, path
import glob
import csv
from datetime import datetime


class CsvFormatter(logging.Formatter):
    def format_msg(self, msg):
        '''Format the msg to csv string'''
        if isinstance(msg, list):
            msg = ','.join(map(str, msg))
        return msg

    def format(self, record):
        record.msg = self.format_msg(record.msg)
        return logging.Formatter.format(self, record)


class CsvRotatingFileHandler(RotatingFileHandler):
    def __init__(self,
                 fmt,
                 datefmt,
                 filename,
                 max_size,
                 max_files,
                 header=None):
        # Format header string if needed
        self._header = header and CsvFormatter(fmt, datefmt).format_msg(header)
        # check if file exists
        self.file_pre_exists = path.exists(filename)
        # call parent file handler __init__
        RotatingFileHandler.__init__(self,
                                     filename,
                                     maxBytes=max_size,
                                     backupCount=max_files)
        self.formatter = CsvFormatter(fmt, datefmt)
        # Write the header if delay is False and a file stream was created.
        if self.stream is not None and not self.file_pre_exists:
            self.stream.write('%s\n' % self._header)

    def rotation_filename(self, default_name):
        '''Make log files counter before the .csv extension'''
        s = default_name.rsplit('.', 2)
        return '{}_{:0{}d}.csv'.format(s[0], int(s[-1]),
                                       self.backupCount // 10 + 1)

    def doRollover(self):
        ''' Prepend header string to each log file'''
        RotatingFileHandler.doRollover(self)
        if self._header is None:
            return
        f = self.formatter.format
        self.formatter.format = lambda x: x
        self.handle(self._header)
        self.formatter.format = f


class CsvLogger(logging.Logger):
    def __init__(self,
                 filename: str,
                 level=logging.INFO,
                 fmt: str = '%(asctime)s,%(message)s',
                 datefmt: str = '%Y/%m/%d %H:%M:%S',
                 max_size: int = 10485760,
                 max_files: int = 10,
                 header=None):
        """logger class to perform the csv logging

        Args:
            filename (string): main log file name or path. if path, will create subfolders as needed
            level (logging level | str | int, optional): logging level for logs. Defaults to logging.INFO.
            fmt (str, optional): output format, accepts parameters accepts 'asctime' 'message' 'levelname'. Defaults to '%(asctime)s,%(message)s'.
            datefmt (str, optional): date format for first column of logs. Defaults to '%Y/%m/%d %H:%M:%S'.
            max_size (int, optional): max size of each log file in bytes. Defaults to 10485760.
            max_files (int, optional): max file count. Defaults to 10.
            header (list[str], optional): header to prepend to csv files. Defaults to None
        """
        self.filename = filename
        self.datefmt = datefmt
        if header and isinstance(header, str):
            header = header.split(',')
        self.header = header

        # make log file directories
        if path.dirname(filename):
            makedirs(path.dirname(filename), exist_ok=True)
        # init logger and add handler
        logging.Logger.__init__(self, filename.rsplit('.', 1)[0], level)
        handler = CsvRotatingFileHandler(fmt, datefmt, filename, max_size,
                                         max_files, header)
        self.addHandler(handler)

    def get_logs(self, evaluate=False):
        """ read all logs from file and return them as a list of lists
        Args:
            evaluate (bool, optional): attempt to evaluate string values using python eval()
        """
        all_logs = []
        # get all files matching filename pattern with or without enumerations
        name = self.filename.rsplit('.', 1)[0]
        extension = self.filename.rsplit('.', 1)[1]
        logfiles = glob.glob(f'{name}*.{extension}')
        logfiles.sort(reverse=True)
        # read each log file and create list of csv logs
        for logfile in logfiles:
            with open(logfile, newline='') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in csvreader:
                    if row != self.header:
                        if evaluate:
                            new_row = []
                            for x in row:
                                try:
                                    # try to eval numerics
                                    new_row.append(eval(x))
                                except:
                                    try:
                                        new_row.append(
                                            datetime.strptime(x, self.datefmt))
                                    except:
                                        new_row.append(x)
                            row = new_row
                        all_logs.append(row)
        return all_logs
