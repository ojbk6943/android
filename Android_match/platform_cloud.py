import os
import threading
import socket
import subprocess
import time

from android_match import AndroidMatch
from simulator_phone import SimulatorPhone




class PlatformCloud:

    # 获得设备信息
    def get_devices(self):
        port = 8000
        bp_port = 10000
        # 全部设备(包括信息)
        devices = subprocess.check_output('adb devices').decode().strip().split('\r\n')
        device_infos = []
        # 设备信息
        for i in range(1, len(devices)):
            device_name = devices[i].split('\t')[0].strip()
            device_verison = subprocess.check_output(
                'adb -s %s shell getprop ro.build.version.release' %(device_name)
            ).decode().strip()
            # 端口号
            port = self.find_port(port)
            bp_port = self.find_port(bp_port)

            # 找到未占用端口，+1，防止重复选中
            port += 1
            bp_port += 1

            device_infos.append((port, bp_port, device_name, device_verison))

        return device_infos

    # 获得端口号(port:9000, bpport:10000)
    def find_port(self, port):
        while self.check_port(port):
            port += 1
        return port

    # 检查端口号是否占用
    def check_port(self, port):
        s = socket.socket()
        # 连接、断开
        try:
            s.connect(("127.0.0.1", port))
            s.shutdown(socket.SHUT_RDWR)
            return True
        except:
            return False

    # 启动appium
    def start_appium(self, port, bp_port, device_name, device_version):
        log_path = os.path.join(os.getcwd(), "log/error.log")
        cmd = 'appium -a 127.0.0.1 -p %d -bp %d --device-name %s ' \
              '--platform-version %s --log %s --log-level warn --log-timestamp'\
              %(port, bp_port, device_name, device_version, log_path)
        os.system(cmd)

    # 线程池
    def get_thread(self, device_infos):
        thread_group = []
        for i in range(len(device_infos)):
            # appium、脚本
            tmp = AndroidMatch(device_infos[i][-1], device_infos[i][0])
            service_thread = threading.Thread(target=pfc.start_appium, args=(*device_infos[i],),
                                              name="service_thread_%d" % (i))
            client_thread = threading.Thread(target=tmp.start_test, name="client_thread_%d" % (i))

            thread_group.append(service_thread)
            thread_group.append(client_thread)

        thread_group.sort(key=lambda t: t.getName()[0: 1], reverse=True)

        return thread_group


    # 执行appium、脚本线程
    def start_thread(self, thread_group):
        # 启动线程(先启动appium, 在执行脚本)
        for t in thread_group:
            if t.getName() == 'client_thread_0':
                time.sleep(20)
            # 设置守护线程
            t.setDaemon(True)
            t.start()
        for t in thread_group:
            if t.getName().startswith('client'):
                t.join()

    # 关闭所有node(也就是appium)
    def close_node(self):
        os.system('taskkill /f /im node.exe')
        print("all-test-finish")

if __name__ == '__main__':
    # 模拟器
    # sp = SimulatorPhone()
    # sp.start_phone()
    # time.sleep(20)

    pfc = PlatformCloud()
    device_infos = pfc.get_devices()
    thread_group = pfc.get_thread(device_infos)

    # 启动线程
    pfc.start_thread(thread_group)

    pfc.close_node()


