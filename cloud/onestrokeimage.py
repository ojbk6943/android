#! /usr/bin/env python
# -*- coding: utf-8 -*-

from appium import webdriver
import cv2 as cv
import os
import time


class OneStrokeImage:

    def __init__(self):
        desired_caps = {
            "platformName": "Android",
            "deviceName": "Android_5.0",
            "platformVersion": "5.0.2",
            "appPackage": "com.mobivans.onestrokecharge",
            "appActivity": "com.stub.stub01.Stub01"
        }
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        time.sleep(5)

    def find_image(self, target):
        base_path = os.path.join(os.getcwd(), 'source')
        screen_path = os.path.join(base_path, 'onestroke.png')
        self.driver.get_screenshot_as_file(screen_path)
        screen = cv.imread(screen_path)
        template = cv.imread(os.path.join(base_path, target))
        result = cv.matchTemplate(screen, template, cv.TM_CCOEFF_NORMED)
        min, similarity, min_loc, left_loc = cv.minMaxLoc(result)
        if similarity < 0.95:
            return -1, -1
        return left_loc[0] + int(template.shape[1] / 2), left_loc[1] + int(template.shape[0] / 2)

    def check_exist(self, target):
        x, y = self.find_image(target)
        return x != -1 and y != -1

    def click(self, target):
        x, y = self.find_image(target)
        if x == -1 or y == -1:
            print('not found %s.' % target)
            return
        self.driver.tap([(x, y)])
        print('click %s at [%d, %d].' % (target, x, y))
        time.sleep(1)

    def start_test(self):
        self.click('new.png')
        self.click('type.png')
        self.click('number2.png')
        self.click('number3.png')
        self.click('number8.png')
        self.click('done.png')
        time.sleep(2)
        self.click('tip.png')
        time.sleep(3)
        if self.check_exist('list.png'):
            print('test success.')
        else:
            print('test fail.')
        self.driver.quit()


if __name__ == '__main__':
    OneStrokeImage().start_test()
