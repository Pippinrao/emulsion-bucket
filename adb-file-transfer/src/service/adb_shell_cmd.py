import subprocess
import re
from typing import List, Tuple

adb = "adb"


class File:
    def __init__(self, name, time, mode, size, own, own_group, path):
        self.name = name
        self.time = time
        self.mode: str = mode
        self.size = size
        self.own = own
        self.own_group = own_group
        self.path = path

    def is_dir(self):
        return self.mode[0] == "d"

    def is_link(self):
        return self.mode[0] == "l"


class Path:
    @classmethod
    def dir_name(cls, path: str):
        return "/" + "/".join(([s for s in path.split("/") if len(s) > 0])[:-1])

    @classmethod
    def _call(cls, cmd: str) -> str:
        try:
            ret: str = subprocess.check_output(cmd).decode("utf-8", 'ignore') + '\n'
            return ret
        except subprocess.CalledProcessError:
            print("error for call {}".format(cmd))

    @classmethod
    def list_dir(cls, path: str):
        cmd = "{} shell \"{}\"".format(adb, "ls -al {}".format(path))
        files = []
        file_list = cls._call(cmd)
        if file_list:
            pattern = r"([dlrwx-]*)\s+(\d*)\s+(\w+)\s*(\w+)\s+(\d+)\s+([\d\-\s]+:[\d]{2})\s+([^\n\r]*).*\n"
            ptn = re.compile(pattern)
            result: List[Tuple] = ptn.findall(file_list)
            for item in result:
                file_name: str = item[6]
                file_path = path + '/' + file_name
                mode = item[0]
                if mode and mode[0] == 'l':
                    file_path = file_name.split("->")[1].strip()
                    if file_path.strip()[0] != '/':
                        file_path = path + '/' + file_path
                if file_name.strip() == '..':
                    file_path = cls.dir_name(path)
                file = File(item[6], item[5], item[0], item[4], item[3], item[2], file_path)
                files.append(file)
        return files

    @classmethod
    def is_dir(cls, path: str):
        cmd = '{} shell "{}"'.format(adb, "if test -d {}; then echo 1;fi".format(path))
        return cls._call(cmd).strip() == "1"

    @classmethod
    def pull(cls, device, local):
        cmd = '{} pull {} {}'.format(adb, device, local)
        cls._call(cmd)

    @classmethod
    def push(cls, local, device):
        cmd = '{} push {} {}'.format(adb, local, device)
        cls._call(cmd)
