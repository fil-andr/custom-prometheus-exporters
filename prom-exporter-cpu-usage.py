from prometheus_client import start_http_server, Gauge
import time
import paramiko

metric_dict = {}
cpu_var = 0

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

##host creds
ip = '192.168.1.10'
user = 'user'
pswd = 'password'

client.connect(hostname=ip, username=user, password=pswd, look_for_keys=False, allow_agent=False,timeout=3)

##cjnfigire metric
metric_name = 'cpu_usage'
metric_dict[metric_name] = Gauge(metric_name, f"cpu usage  on {ip}")


##function for parsing cpu usage on remote host
def cpu_usage():
    stdin, stdout, stderr = client.exec_command("top -bn1 | grep %Cpu")
    cpu_lst = ''.join(stdout.readlines()).split()
    global cpu_var
    cpu_var = cpu_lst[1]
    return cpu_var

def main():
    start_http_server(9000)                                  ### port
    metric_dict[metric_name].set(cpu_usage())



if __name__ == "__main__":
     while True:
        main()
        time.sleep(5)