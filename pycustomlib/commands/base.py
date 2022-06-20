"""
    Docstring to prevent pylint info msg
"""

class Base:
    """
        A base class for running common commands, even those over the FS
        that may require an SFTP client
    """

    def __init__(self):
        self._system = None

    def exec_command(self, command):
        """
            Runs a command. Must be implemented in subclases
        """

        raise NotImplementedError


    def free(self):
        """
            Some random docstring.
        """

        if "linux" in self._system.lower():
            return self.exec_command('free')
        elif "windows" in self._system.lower():
            return self.exec_command('wmic OS get TotalVisibleMemorySize /Value')

        return None
