import time

from appium import webdriver
import os


class AndroidMatch:

    # 初始化
    def __init__(self, device_version, port):
        apk_path = os.path.join(os.getcwd(), "source/yibijizhang.apk")
        self.desired_dir = {
            "platformName": "Android",
            "platformVersion": device_version,
            "deviceName": "Android_5",
            "appPackage": "com.mobivans.onestrokecharge",
            "appActivity": "com.stub.stub01.Stub01",
            "app": apk_path,
            "unicodeKeyboard": "true"
        }
        self.url = "http://127.0.0.1:%s/wd/hub" %(port)

    # 键入值
    def input_content(self, ele, text):
        ele.click()
        ele.clear()
        ele.send_keys(text)

    # 验证
    def assert_result(self, actual, expect):
        if actual == expect:
            return True
        else:
            return False

    def start_test(self):
        print(self.url, self.desired_dir)
        driver = webdriver.Remote(self.url, self.desired_dir)
        driver.implicitly_wait(15)
        try:
            # 脚本
            driver.find_element_by_android_uiautomator('text("记一笔")').click()
            # 滑动
            driver.scroll(
                driver.find_element_by_android_uiautomator('text("办公")'),
                driver.find_element_by_android_uiautomator('text("果蔬")')
            )
            # 消费的模块
            driver.find_element_by_android_uiautomator('text("汽车")').click()
            self.input_content(driver.find_element_by_id("add_et_remark"), "吃肉肉")

            # 记录
            driver.find_element_by_id("keyb_btn_1").click()
            driver.find_element_by_id("keyb_btn_6").click()
            driver.find_element_by_id("keyb_btn_finish").click()

            driver.find_element_by_android_uiautomator('text("长按记录可删除")').click()

            # 验证、结果
            category_eles = driver.find_elements_by_id("account_item_txt_remark")
            money_eles = driver.find_elements_by_id("account_item_txt_money")

            # 比较最新的一笔业务
            if self.assert_result(category_eles[0].text, "吃肉肉") and \
                   self.assert_result(money_eles[0].text, "-16"):
                print("test-success")
            else:
                print("test-fail")
        # 报错，截图，报错日志
        except Exception as e:
            with open(os.path.join(os.getcwd(), "error","Android_5.log"), 'a') as file:
                file.write(str(e)+"\n")
                format_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            driver.get_screenshot_as_file(
                os.path.join(os.getcwd(), "source", "Android_5%s.png" %(format_time))
            )

        finally:
            # 关闭
            driver.quit()


if __name__ == '__main__':
    AndroidMatch("5.1.1", "4723").start_test()
