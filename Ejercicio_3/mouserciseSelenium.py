from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

reglas = {
    1: "//p/a[@href='m2.htm']",
    2: "//p/a[@href='m3.htm']",
    3: "//td/a[@href='m4.htm']",
    4: "//td/a[@href='m5.htm']",
    5: "//td/a[@href='m6.htm']",
    6: "//p/a[@href='m7.htm']",
    7: "//p/a[@href='m8.htm']",
    8: "//p/a[@href='m9.htm']",
    9: "//td/a[@href='m10.htm']",
    10: "//td/a[@href='m11.htm']",
    11: "//td/a[@href='m12.htm']",
    12: "//td/a[@href='m13.htm']",
    13: "//td/a[@href='m14.htm']",
    14: "//td/a[@href='m15.htm']",
    15: "//td/a[@href='m16.htm']",
    16: "//form[@action='m17.htm']/input",
    17: "//form[@action='m18.htm']/input",
    18: "//form[@action='m19.htm']/button",
    19: "//form[@action='m20.htm']/input",
    20: "//td//a[@href='m21.htm']/img",
    21: "//td//a[@href='m22.htm']/img",
    22: ["//tr//td/img[@onclick]", "//tr//td/a", False],
    23: ["//tr//td/form/input | //tr//td/img[@onclick]", "//tr//td/a", False],
    24: ["//tr//td/img", "//tr//td/a", True],
    25: "//tr//td/a[@href='m26.htm']",
    26: "//p/a[@href='m27.htm']",
    27: "//p/a[@href='m28.htm']",
    28: "//p/a[@href='m29.htm']",
    29: "//p/a[@href='m30.htm']",
    30: "//td/p/a[@href='m31.htm']",
    31: "//tr//td/a",
    32: "//tr//td/span/a[@href='m33.htm']",
    33: ["//form/input[@type='checkbox']", "//p/a", False],
    34: ["//form/input[@type='checkbox']", "//form/input[@type='submit']", False],
    35: ["//form/input[@type='radio']", "//p/a", False],
    36: ["//form[@action='m37.htm']/input[@data-com.bitwarden.browser.user-edited]", "//form[@action='m37.htm']/input[@type='submit']", False],
    37: ["//form/select/option[text()='Cinco']", "//form/p/a", False],
    38: ["//form/select/option[text()='Bote']", "//form/input[@type='submit']", False],
    39: ["//form/select/option[text()='Seis']", "//form/p/a", False],
    40: ["//form/select/option[text()='Chicago Estilo']", "//form/input[@type='submit']", False],
    41: ["//form/input[@type='text']", "//form/input[@type='submit']"]
}

driver = webdriver.Chrome('C:/Users/steve/Documents/Git/Trabajo/PracticaPythonNodel/EjerciciosDeLaPrueba/SeleniumOlx/chromedriver.exe')

driver.get('http://www.pbclibrary.org/raton/mousercise.htm')

button_start = driver.find_element_by_xpath('//form[@action="m1.htm"]/input')
button_start.click()

for key, value in reglas.items():
    sleep(1)
    if key < 22 or (key > 24 and key < 31) or key == 32:
        number_click = driver.find_element_by_xpath(value)
        number_click.click()
    elif key == 41:
        elements = driver.find_elements(By.XPATH, value[0])
        elements[0].send_keys('Steven')
        elements[1].send_keys('Araujo')
        sleep(0.1)
        driver.find_element_by_xpath(value[1]).click()
    elif (key >= 22 and key <= 24) or (key > 32):
        elements = driver.find_elements(By.XPATH, value[0])
        for element in elements:
            if value[2]:
                actionChains = ActionChains(driver)
                actionChains.double_click(element).perform()
            else:
                element.click()
            sleep(0.15)
        result = driver.find_element_by_xpath(value[1])
        result.click()
    else:
        driver.find_element_by_xpath(value).click()
        sleep(0.1)
        driver.switch_to_alert().accept()
