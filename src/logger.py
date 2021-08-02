import logging
import os


class Logger:
    _verbose_logging: bool = False
    _path: str = '.'

    def __init__(self, verbose_logging: bool = False, path: str = '.'):
        Logger._verbose_logging = verbose_logging
        Logger._path = path
        self.__prepare_logger()

    @property
    def verbose_logging(self):
        return type(self)._verbose_logging

    @property
    def path(self) -> str:
        return type(self)._path

    @staticmethod
    def __prepare_logger():
        level = logging.DEBUG if Logger.verbose_logging else logging.CRITICAL
        path = os.path.join(Logger._path, 'web_gallery.log')

        handler = logging.FileHandler(path, encoding="utf-8")
        handler.setFormatter(logging.Formatter(u"[%(asctime)s %(module)s - %(funcName)s()] %(message)s", "%Y-%m-%d %H:%M:%S"))
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(level)
