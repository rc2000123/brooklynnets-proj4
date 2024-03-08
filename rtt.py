import socket
import time
import subprocess


def get_rtt(host, port):
    try:
        command = f"sh -c \"time echo -e '\x1dclose\x0d' | telnet {host} {port}\""
        result = str(subprocess.run(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout)
        # print(result)
        rtt = result.split("real\\t")[1][2:7]
        # print(rtt)
        return float(rtt)

            
    except subprocess.CalledProcessError as e:
        print("process error, could not get rtt")
        return None


print(get_rtt("144.214.26.111", 80))
