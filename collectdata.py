from city import City
from db import DB
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

driver = None


def initdriver():
    global driver
    driver = webdriver.PhantomJS(executable_path='./phantomjs')
    driver.set_window_size(1120, 550)

bblist = dict()
baseurl = "http://www.bigbasket.com/"
currentcategories = None


def parseproduct(item):
    try:
        element = item.find_element(By.CLASS_NAME, "uiv2-combo-block").text
        mo = re.search(r"[\s\S]*?(\d+\.\d+)", element)
        discount = float(mo.group(1))
    except:
        discount = 0
    try:
        brand = item.find_element(By.CLASS_NAME, "uiv2-brand-title").text
    except:
        brand = ""
    element = item.find_element(
        By.CLASS_NAME, "uiv2-list-box-img-title").get_attribute("innerHTML")
    mo = re.search(
        r"brand-title.*?<\/span>([\s\S]*?)<\/a>", element, re.IGNORECASE)
    prod_name = mo.group(1).strip()
    element = item.find_element(By.CLASS_NAME, "uiv2-field-wrap").text
    mo = re.search(r".*?(\d+\.?\d?)\s([a-zA-Z]+)[\s\n]", element)
    try:
        quantity = float(mo.group(1))
        unit = mo.group(2)
    except:
        mo = re.search(
            r".*?(\d+\.?\d?)\s([a-zA-Z]{0,5})[\s\n]", item.get_attribute("innerHTML"))
        quantity = float(mo.group(1))
        unit = mo.group(2)
    element = item.find_element(By.CLASS_NAME, "uiv2-rate-count-avial").text
    mo = re.search(r"(\d+\.?(\d+)?)", element)
    price = float(mo.group(1))
    return {'discount': discount, 'brand': brand, 'prod_name': prod_name, 'quantity': quantity, 'unit': unit, 'price': price}


def scrolltoend():
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        try:
            temp = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "next-product-page")))
            temp.click()
        except:
            break


def collectdata():
    global currentcategories
    try:
        db = DB()
        initdriver()
        city = City()
        while city.nextcity(db, driver) is not None:
            prod_namelist = set()
            for suburl, categories in city.category_pages.items():
                driver.get(baseurl + suburl)
                currentcategories = categories
                scrolltoend()
                products = driver.find_elements(
                    By.XPATH, "//li[starts-with(@id,'product_')]")
                print(len(products))
                for product in products:
                    if(product.get_attribute("class") == "featured-product" or "display:none" in product.get_attribute("style") or len(product.text) < 5):
                        continue
                    try:
                        details = parseproduct(product)
                        if(details['prod_name'] not in prod_namelist):
                            prod_namelist.add(details['prod_name'])
                            db.insertproduct(details, currentcategories)
                    except Exception as e:
                        print("---------------------------------------")
                        print(e)
                        print("---------------------------------------")
                        continue
                time.sleep(10)
    finally:
        driver.close()
        db.conn.close()

collectdata()
