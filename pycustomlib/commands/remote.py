"""
    Module docstring
"""
from logging import getLogger, ERROR
from socket import timeout as socket_timeout

from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import AuthenticationException, NoValidConnectionsError

from .base import Base

logger = getLogger(__package__)
getLogger("paramiko").setLevel(ERROR)

class Remote(Base):
    """
        Handle remote SSH commands and SFTP file transfers
    """

    def __init__(self, ip_addr):
        super().__init__()
        self._ip = ip_addr
        self._ssh = None
        self._sftp = None

    def exec_command(self, command):
        """
            Runs remotelly some given command
        """

        logger.info("Running the remote command: %s at %s", command, self._ip)
        _, stdout, _ = self._ssh.exec_command(command)
        stdout = stdout.read().decode('utf-8').strip()
        return stdout

    def connect(self, username=None, password=None, key=None, port=22, timeout=1):
        """
            Creates the SSH connection to the server
        """
        if self._check_connection():
            logger.warning('You already have an active SSH connection')
            return False
        else:
            self._ssh, self._system = self._connect(username=username, password=password, key=key,
                                      timeout=timeout, port=port)

            logger.info("Working at %s", self._system)

            self._sftp = self._ssh.open_sftp()

            return True

    def disconnect(self):
        """
            Closes the SSH connection to the server
        """
        if not self._check_connection():
            logger.warning('You do not have an active SSH connection')
            return False
        else:
            self._ssh.close()
            self._ssh = None
            self._system = None
            self._sftp = None
            return True

     # ******************************* PRIVATE METHODS *****************************************
    def _check_connection(self):
        """
            Checks if there is an active SSH connection
        """
        if self._ssh is None:
            return False
        else:
            return self._ssh.get_transport().is_active()

    def _connect(self, username, password, timeout, key, port):
        """
            Creates the SSH connection given the credentials or SSH key
        """

        if key is not None:
            # TODO: implement. Check if file exists (if not raise FileNotFound)
            raise NotImplementedError

        if username is None or password is None:
            logger.error('You must provide username and password')

        try:
            ssh = SSHClient()
            # ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(self._ip, port=port, username=username, password=password, timeout=timeout)

            _, stdout, _ = ssh.exec_command(
                "python -c 'from platform import system; print(system())'"
                )
            system = stdout.read().decode('utf-8').strip()
            logger.info("system is %s", system)
            logger.info("ssh is %s", ssh)
        except AuthenticationException:
            logger.error('Bad credentials of client with IP %s', self._ip)
        except NoValidConnectionsError:
            logger.error('Client with %s is not connected', self._ip)
        except (TimeoutError, socket_timeout):
            logger.error('Client with %s has no SSH enabled', self._ip)
        except Exception as ex:  # pylint: disable=W
            logger.exception(ex)
        else:
            return ssh, system
