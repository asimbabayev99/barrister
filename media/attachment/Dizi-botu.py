from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import random
import time 
import string
import pytesseract
import cv2
from PIL import Image
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

req_proxy = RequestProxy()
proxies = req_proxy.get_proxy_list()

def captcha_resolver(img):
    im = Image.open('screenshot.png')
    im.crop((717,106,883,174)).save('screenshot.png')
    image = cv2.imread('screenshot.png')  
    threshold = 180
    _, img_binarized = cv2.threshold(image,threshold,255,cv2.THRESH_BINARY)
    pil_img = Image.fromarray(img_binarized)
    text = pytesseract.image_to_string(pil_img,config='--psm 6')
    return text

def change_proxy(num):
    proxy = proxies[num]
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", proxy.get_address())
    profile.set_preference("network.proxy.http_port", proxy.port)
    profile.set_preference("network.proxy.ssl", proxy.get_address())
    profile.set_preference("network.proxy.ssl_port",proxy.port) 
    profile.set_preference('general.useragent.override','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36')
    driver = webdriver.Firefox(profile)
    return driver





for i in range(100):
    browser = change_proxy(i)
    browser.get("http://webflex7.ru/ref173462")  
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    random_name  = "".join(random.choice(string.ascii_lowercase) for i in range(8))
    password = "".join(random.choice(string.ascii_letters) for i in range(8)) + str(random.randint(1,10))
   
    time.sleep(1)
    browser.find_element_by_id('ft_reg_1').send_keys(random_name)
    time.sleep(1)
    browser.find_element_by_id('ft_reg_2').send_keys(password)
    time.sleep(1)
    password_again = browser.find_element_by_id('ft_reg_3').send_keys(password)
    time.sleep(1)
    button = browser.find_element_by_xpath('//*[@id="page"]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div[4]')
    button.click()
    time.sleep(2)
    browser.save_screenshot('screenshot.png')
    text = captcha_resolver('screenshot.png')
    print(text)
    code_add = browser.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div[5]/div/div[1]')
    time.sleep(2)
    browser.find_element_by_id('ft_code').send_keys(text)
    code_add.click()
    time.sleep(5)
    if bool(EC.title_contains('ID')):
        try:
            logout = browser.find_element_by_xpath('//*[@id="BlockMnogo"]/div[6]/div/div[1]/div[1]/div/div[4]')
            logout.click()
            browser.delete_all_cookies()
            time.sleep(1) 
            browser.close()
            time.sleep(1)
        except Exception as e:
            time.sleep(1)
            print(e)
            browser.delete_all_cookies() 
            browser.close()
        continue
    else:
        time.sleep(4)
        browser.delete_all_cookies() 
        browser.close()
        time.sleep(1)
     












