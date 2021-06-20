#!/usr/bin/python3

import logging
from logging.handlers import RotatingFileHandler
from os import makedirs, path

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

    def __init__(self, fmt, datefmt, filename, max_size, max_files, header=None):
        RotatingFileHandler.__init__(self, filename, maxBytes=max_size, backupCount=max_files)
        self.formatter = CsvFormatter(fmt, datefmt)
        # Format header string if needed
        self._header = header and self.formatter.format_msg(header)

    def rotation_filename(self, default_name):
        '''Make log files counter before the .csv extension'''
        s = default_name.rsplit('.', 2)
        return '{}_{:0{}d}.csv'.format(s[0], int(s[-1]), self.backupCount // 10 + 1)

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
                level           = logging.INFO,
                fmt: str        = '%(asctime)s,%(message)s',
                datefmt: str    = '%Y/%m/%d %H:%M:%S',
                max_size: int   = 10485760,
                max_files: int  = 10,
                header          = None
                ):
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
        if path.dirname(filename):
            makedirs(path.dirname(filename), exist_ok=True)
        logging.Logger.__init__(self, filename.rsplit('.', 1)[0], level)
        handler = CsvRotatingFileHandler(fmt, datefmt, filename, max_size, max_files, header)
        self.addHandler(handler)
