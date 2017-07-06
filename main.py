import re
import sys
import json
import subprocess

def start_sslocal(server_addr, server_port, password, local_port):
    return subprocess.Popen(['sslocal',
                    '-s', server_addr,
                    '-p', server_port,
                    '-k', password,
                    '-l', local_port
    ])

def ping_test(addr):
    try:
        out = subprocess.check_output(
            ['ping', '-c', '10', '-i', '0.21', addr]
        ).decode('utf8')
        total_time_r = re.search('packet loss, time (\d+)ms', out)
        total_time = int(total_time_r.group(1))
        print('[info]: ping test:', addr, total_time)
        return total_time < 2200
    except:
        return False

def handle_json(j):
    base_port = 1081
    ret = []
    export_configs = []
    for conf in j["configs"]:
        if not ping_test(conf["server"]):
            continue
        p = start_sslocal(conf["server"],
                      conf["server_port"],
                      conf["password"],
                      str(base_port))
        export_configs.append(' '.join(['socks5', '127.0.0.1', str(base_port)]))
        base_port += 1
        ret.append(p)

    exp_beg = ['############proxychain.conf############']
    exp_end = ['##################end##################']
    print('\n'.join(exp_beg+export_configs+exp_end))
    return ret

def read_config(path="./gui-config.json"):
    with open(path) as f:
        j = json.load(f)
        return handle_json(j)

if __name__=="__main__":
    ps = read_config()
    try:
        [i.wait() for i in ps]
    except:
        [i.kill() for i in ps]

