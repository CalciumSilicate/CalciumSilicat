import subprocess
import threading
import queue
import time
import sys
import os

# 设置TCPing的路径（需要提前安装并配置环境变量）
TCPING_PATH = 'tcping.exe'

# 设置要查找的ip段
IP_BASE = '*.*.'
IP_START = 200
IP_END = 255

# 设置要查找的端口
PORT = 26802

# 设置同时运行的线程数
MAX_THREADS = 512

# 初始化队列和结果列表
queue = queue.Queue()
result = []

# 初始化进度条
def print_progress(progress):
    bar_length = 30
    status = ""
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(bar_length*progress))
    text = "\rProgress: [{0}] {1}% {2}".format( "#"*block + "-"*(bar_length-block), round(progress*100, 2), status)
    sys.stdout.write(text)
    sys.stdout.flush()

# 检查ip的端口是否开放
def check_ip(ip):
    try:
        output = subprocess.check_output([TCPING_PATH, ip, str(PORT), '-T', '500ms', '-c', '1'])
        if b'Connected' in output:
            result.append(ip)
    except subprocess.CalledProcessError:
        pass

# 每个线程的工作
def worker():
    while True:
        ip = queue.get()
        check_ip(ip)
        queue.task_done()

# 初始化线程池
for i in range(MAX_THREADS):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

# 添加要检查的ip到队列
for i in range(IP_START, IP_END+1):
    for j in range(256):
        ip = IP_BASE + str(i) + '.' + str(j)
        queue.put(ip)

# 开始检查
start_time = time.time()
total_ips = queue.qsize()
processed_ips = 0
while not queue.empty():
    time.sleep(0.1)
    processed_ips = total_ips - queue.qsize()
    progress = processed_ips / total_ips
    print_progress(progress)

# 等待所有线程结束
queue.join()

# 输出结果
if len(result) == 0:
    print('没有IP符合要求')
else:
    print('\n符合要求的IP列表：')
    for ip in result:
        print(ip)

# 输出用时
end_time = time.time()
print('用时：', round(end_time-start_time, 2), '秒')
