"""
    Local module docstring
"""

import logging
from platform import system
from subprocess import PIPE, Popen

from .base import Base

logger = logging.getLogger(__package__)

class Local(Base):
    """
        Local class docstring
    """

    def __init__(self):
        super().__init__()
        self._system = system()

    def exec_command(self, command):
        """
            Runs a command in the local machine and returns the output
        """
        try:
            logger.info("running command %s", command)
            p = Popen(command, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
            p.stdin.flush()
            stdout = p.stdout
            stderr = p.stderr

            err = stderr.read().decode('utf-8').replace('\n', '')
        except Exception as ex:
            logger.exception(ex)
            raise
        else:
            if err != '':
                logger.error('ERROR: %s', err)
            else:
                out = stdout.read().decode('utf-8')
                # logger.info('out is: %s', out)

            return out
