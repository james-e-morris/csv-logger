#!/usr/bin/python3

import logging
from logging.handlers import RotatingFileHandler
from os import makedirs, path
import glob
import csv
from datetime import datetime


class CsvFormatter(logging.Formatter):

    def __init__(self, fmt, datefmt, delimiter=','):
        super().__init__(fmt, datefmt)
        self._delimiter = delimiter

    def format_msg(self, msg):
        ''' format the msg to csv string from list if list '''
        if isinstance(msg, list):
            msg = self._delimiter.join(map(str, msg))
        return msg

    def format(self, record):
        ''' run format_msg on record to get string before passing to Formatter '''
        record.msg = self.format_msg(record.msg)
        return logging.Formatter.format(self, record)


class CsvRotatingFileHandler(RotatingFileHandler):

    def __init__(
            self,  #
            fmt,
            datefmt,
            filename,
            max_size,
            max_files,
            header=None,
            delimiter=','):
        # Format header string if needed
        self._header = header and CsvFormatter(fmt, datefmt, delimiter).format_msg(header)
        # check if file exists
        self.file_pre_exists = path.exists(filename)
        # call parent file handler __init__
        RotatingFileHandler.__init__(self, filename, maxBytes=max_size, backupCount=max_files)
        self.formatter = CsvFormatter(fmt, datefmt, delimiter)
        # Write the header if delay is False and a file stream was created.
        if self.stream is not None and not self.file_pre_exists:
            self.stream.write('%s\n' % self._header)

    def rotation_filename(self, default_name):
        ''' make log files counter before the .csv extension '''
        s = default_name.rsplit('.', 2)
        return '{}_{:0{}d}.csv'.format(s[0], int(s[-1]), self.backupCount // 10 + 1)

    def doRollover(self):
        ''' prepend header string to each log file '''
        RotatingFileHandler.doRollover(self)
        if self._header is None:
            return
        # temporarily overwrite format function with a straight pass-through lambda function
        # handle header without formatting, then reset format function to what it was
        f = self.formatter.format
        self.formatter.format = lambda x: x
        self.handle(self._header)
        self.formatter.format = f


class CsvLogger(logging.Logger):

    def __init__(self,
                 filename: str,
                 delimiter=',',
                 level=logging.INFO,
                 add_level_names=[],
                 add_level_nums=None,
                 fmt: str = '%(asctime)s,%(message)s',
                 datefmt: str = '%Y/%m/%d %H:%M:%S',
                 max_size: int = 10485760,
                 max_files: int = 10,
                 header=None):
        """logger class to perform the csv logging

        Args:
            filename (string): main log file name or path. if path, will create subfolders as needed
            delimiter (str, optional): delimiter to use in the files. Defaults to ','.
            level (logging level | str | int, optional): logging level for logs. Defaults to logging.INFO.
            add_level_names (list[str], optional): adds additional logging levels at the highest level for custom log tagging
            add_level_nums (list[int], optional): assigns specific nums to add_level_names (default nums if not provided: 100,99,98..)
            fmt (str, optional): output format, accepts parameters 'asctime' 'message' 'levelname'. Defaults to '%(asctime)s,%(message)s'.
            datefmt (str, optional): date format for first column of logs. Defaults to '%Y/%m/%d %H:%M:%S'.
            max_size (int, optional): max size of each log file in bytes. Defaults to 10485760.
            max_files (int, optional): max file count. Defaults to 10.
            header (list[str], optional): header to prepend to csv files. Defaults to None
        """
        self.filename = filename
        self.delimiter = delimiter
        # if default fmt is still set but delimiter is not comma, replace with delimiter
        if fmt == '%(asctime)s,%(message)s' and delimiter != ',':
            fmt = f'%(asctime)s{delimiter}%(message)s'
        self.datefmt = datefmt
        if header and isinstance(header, str):
            header = header.split(delimiter)
        self.header = header

        # make log file directories
        if path.dirname(filename):
            makedirs(path.dirname(filename), exist_ok=True)
        # init logger and add handler
        logging.Logger.__init__(self, filename.rsplit('.', 1)[0], level)
        add_level_nums = add_level_nums or [100 - i for i in range(len(add_level_names))]
        for level_num, level_name in zip(add_level_nums, add_level_names):
            self.addLoggingLevel(level_name, level_num, level_name)

        handler = CsvRotatingFileHandler(fmt, datefmt, filename, max_size, max_files, header, delimiter)
        self.addHandler(handler)

    def addLoggingLevel(self, levelName, levelNum, methodName=None):
        """
        https://stackoverflow.com/a/35804945/8605878
        
        Comprehensively adds a new logging level to the `logging` module and the
        currently configured logging class.

        `levelName` becomes an attribute of the `logging` module with the value
        `levelNum`. `methodName` becomes a convenience method for both `logging`
        itself and the class returned by `logging.getLoggerClass()` (usually just
        `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
        used.

        To avoid accidental clobberings of existing attributes, this method will
        raise an `AttributeError` if the level name is already an attribute of the
        `logging` module or if the method name is already present 

        Example
        -------
        >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
        >>> logging.getLogger(__name__).setLevel("TRACE")
        >>> logging.getLogger(__name__).trace('that worked')
        >>> logging.trace('so did this')
        >>> logging.TRACE
        5

        """
        if not methodName:
            methodName = levelName.lower()

        if hasattr(logging, levelName):
            raise AttributeError('{} already defined in logging module'.format(levelName))
        if hasattr(logging, methodName):
            raise AttributeError('{} already defined in logging module'.format(methodName))
        if hasattr(logging.getLoggerClass(), methodName):
            raise AttributeError('{} already defined in logger class'.format(methodName))

        # This method was inspired by the answers to Stack Overflow post
        # http://stackoverflow.com/q/2183233/2988730, especially
        # http://stackoverflow.com/a/13638084/2988730
        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(levelNum):
                self._log(levelNum, message, args, **kwargs)

        def logToRoot(message, *args, **kwargs):
            logging.log(levelNum, message, *args, **kwargs)

        logging.addLevelName(levelNum, levelName)
        setattr(logging, levelName, levelNum)
        setattr(logging.getLoggerClass(), methodName, logForLevel)
        setattr(logging, methodName, logToRoot)

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
                csvreader = csv.reader(csvfile, delimiter=self.delimiter, quotechar='|')
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
                                        new_row.append(datetime.strptime(x, self.datefmt))
                                    except:
                                        new_row.append(x)
                            row = new_row
                        all_logs.append(row)
        return all_logs
