# coding: utf-8

from .runner import AdHocRunner, CommandRunner
from .inventory import Inventory


def TestAdHocRunner():
    """
     以yml的形式 执行多个命令
    :return:
    """
    host_data = [
        {"hostname": "10.144.132.6",
         "ip": "10.144.132.6",
         "port": 22,
         "username": "centos",
         "private_key": "/home/python/.ssh/id_rsa_1",
         },
    ]
    inventory = Inventory(host_data)
    runner = AdHocRunner(inventory)
    dest = "/opt/mysql/world.sh"

    tasks = [
        # {"action": {"module": "shell", "args": "whoami"}, "name": "run_whoami"},
        # {"action": {"module": "shell", "args": "free -m | awk 'NR\=\=2{printf \"%.2f\", $3*100/$2 }'"}, "name": "get_mem_usage"},
        # {"action": {"module": "shell", "args": "df -h | awk '$NF\=\=\"/\"{printf \"%s\", $5}'"}, "name": "get_disk_usage"},
        # {"action": {"module": "copy", "args": "src=/home/python/Desktop/3358.cnf dest=/opt/mysql/my3358.cnf mode=0777"}, "name": "send_file"},
        # {"action": {"module": "copy", "args": "src=/home/python/Desktop/deploy.sh dest=/opt/mysql/deploy.sh mode=0777"}, "name": "send_file"},
        # {"action": {"module": "command", "args": "sh /opt/mysql/hello.sh"}, "name": "execute_file"},
        # {"action": {"module": "shell", "args": "sudo sh /opt/mysql/deploy.sh"}, "name": "execute_file"},
        # {"action": {"module": "lineinfile", "args": "dest=/opt/mysql/hello.sh line=hello1 regexp=echo state=present"}, "name": "modify_file"},
        # {"action": {"module": "lineinfile", "args": "dest=/opt/mysql/world.sh line="" regexp=echo state=present"}, "name": "modify_file"},
        {"action": {"module": "lineinfile", "args": "dest=%s line=sun regexp=echo state=present" % dest}, "name": "modify_file"},
        # {"action": {"module": "shell", "args": "lineinfile dest=/opt/mysql/hello.sh regexp=hello insertafter=#echo line=hello world"}, "name": "modify_file"},

        # {"action": {"module": "shell", "args": "grep 'cpu ' /proc/stat | awk '{usage\=($2+$4)*100/($2+$4+$5)} END {print usage}'"}, "name": "get_cpu_usage"},
    ]
    ret = runner.run(tasks, "all")
    print(ret.results_summary)
    print(ret.results_raw)


def TestCommandRunner():
    """
    执行单个命令，返回结果
    :return:
    """

    host_data = [
        {
            "hostname": "10.144.132.6",
            "ip": "10.144.132.6",
            "port": 22,
            "username": "centos",
            "private_key": "/home/python/.ssh/id_rsa_1",
        },
    ]
    inventory = Inventory(host_data)
    runner = CommandRunner(inventory)

    res = runner.execute('pwd', 'all')
    print(res.results_command)
    print(res.results_raw)
    print(res.results_command['10.144.132.6']['stdout'])


if __name__ == "__main__":
    TestAdHocRunner()
    TestCommandRunner()
