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

def handle_json(j):
    base_port = 1081
    ret = []
    for conf in j["configs"]:
        p = start_sslocal(conf["server"],
                      conf["server_port"],
                      conf["password"],
                      str(base_port))
        base_port += 1
        ret.append(p)
    return ret

def read_config(path="./gui-config.json"):
    with open(path) as f:
        j = json.load(f)
        return handle_json(j)

if __name__=="__main__":
    ps = read_config()
    [i.wait() for i in ps]
    #start_sslocal("sg01-80.ssv7.net", "62089", "Zzk5etEUYYUj", "1081")
