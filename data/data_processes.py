from fnmatch import fnmatch
from psutil import process_iter, Process, AccessDenied


class Processes:
    def __init__(self):
        self.output = ''
        self.founded = ''
        self.killed = ''

    def GetProcesses(self):
        """
        getting processes list
        :return: str <processes>
        """
        for process in process_iter():
            try:
                process_name = process.name().lower()
                processes_id = process.pid
                self.output += f'{process_name} {processes_id}\n'
            except AccessDenied:
                pass

        return self.output

    def KillProcess(self, target):
        """
        Killing process by name[.exe]
        :param target: str
        :return: str (killed)
        """
        for process in Processes.GetProcesses(self).splitlines():
            try:
                process_name = process.split(" ")[0]
                process_id = int(process.split(" ")[1])
                if target.lower() == process_name:
                    Process(process_id).kill()
                    self.killed += f'{process}\n'
            except Exception as e:
                print(e)

        return self.killed

    def FindProcess(self, pattern):
        """
        Using fnmatch [pattern]

        :param pattern:
        :return: str (founded)
        """
        for process in Processes.GetProcesses(self).splitlines():
            try:
                process_name = process.split(" ")[0]
                if fnmatch(process_name, pattern.lower()):
                    self.founded += f'{process}\n'
            except ValueError and IndexError:
                pass

        return self.founded

