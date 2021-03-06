import paramiko

def get_cpu_idle(host, username, password, port=22, type=None, isWindows=False ):
    connect = ssh_connect(host, port, username, password)
    cmd = "top -bi -n 2 -d 0.02"
    if type is not None:
        cmd += " | grep %s" % type
    stdin, stdout, stderr = connect.exec_command(cmd)
    info = stdout.readlines()

    if isWindows is False:
        list = info[1].split(",")
        for li in list:
            if "id" in li:
                if '%' in li:
                    cpuusage = li.strip().split("%")[0]
                else:
                    cpuusage = li.strip().split(" ")[0]
                return float(cpuusage)
        return 0
    else:
        num_cpu = len(info) / 2  # number of cpu cores
        cur_usage = 0
        for i in range(num_cpu, num_cpu * 2):
            line = info[i]
            if 'Cpu' in line:
                usage = float(line.split(':')[1].split('/')[0].strip())
                cur_usage += usage
        print cur_usage / num_cpu
        return int(cur_usage / num_cpu)


def release_memory(host, username, password, port=22):
    connect = ssh_connect(host, port, username, password)
    cmd = 'sudo sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"'
    stdin, stdout, stderr = connect.exec_command(cmd)
    info = stdout.readlines()


def check_network(host, username, password, port=22, type=None, isWindows=False ):
    connect = ssh_connect(host, port, username, password)
    pass


def ssh_connect(host, port, username, password):
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshClient.connect(host, port, username, password)
    return sshClient
    
'''
for h in host:
    machine = MachineFactory.generate(ip)
    Monitor().register(machine)

Monitor().get_cpu_usage(ip)


class VoidMachine(object):
    def get_cpu_usage(self):
        print 'error ip'

class Machine(object):
    def get_cpu_usage(self):
        print get_cpu_idle()

class MachineFactory(object):
    __metaclass__ = Singleton
    def __init__(self):
        self._all_machine = {}

    def generage(ip, name='root', cluster='sp1unk', port=22):
        machine = Machine(ip, name, cluster, port)
        slef._all_machine[ip] = machine
        return machine

class Monitor(object):
    __metaclass__ = Singleton
    def __init__(self):
        self._monitor_machine = {}

    def register(machine):
        self._monitor_machine[machine.ip] = machine

    def get_cpu_usage(ip):
        machine = self._monitor_machine.get(ip, VoidMachine())
        machine.get_cpu_usage() 

'''


