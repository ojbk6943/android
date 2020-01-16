import os
import time
from pymouse import PyMouse


class SimulatorPhone:

    def __init__(self):
        self.im = ImageMatch()
        self.mouse = PyMouse()
    '''启动逍遥多开模拟器'''
    def open(self):
        start_path = os.path.join(os.getcwd(), "source", "start.lnk")
        os.system(start_path)

    # 单击
    def click(self, x, y):
        self.mouse.click(x, y)
        time.sleep(1)

    # 启动模拟器机型
    def start_phone(self):

        # self.open()
        img_path = os.path.join(os.getcwd(), "source", "png", "start.png")
        print(img_path)
        x, y = self.im.find_image(img_path)
        self.click(x, y)
        print("click location %s %s" %(x, y))

    '''关闭多开程序'''
    def close(self):
        os.system('taskkill /f /im MEmuConsole.exe')

if __name__ == '__main__':

    # 点击启动一个模拟器机型
    sp = SimulatorPhone()
    # sp.open()
    # im = ImageMatch()
    # img_path = os.path.join(os.getcwd(), "source", "png", "start.png")
    # print(img_path)
    # x,y = im.find_image(img_path)
    # print(x, y)
    # sp.click(x,y)