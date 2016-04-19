import requests
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

baseurl = "http://www.bigbasket.com/"
# change to get a different set of categories
which_categories = [0, 1]


class City:

    def __init__(self):
        self.citylist = list()
        self.category_pages = dict()
        self.currentcategories = None
        self.getcitylist()

    def getcitylist(self):
        url = baseurl + "choose-city/?/"
        while True:
            try:
                r = requests.get(url)
                break
            except:
                pass
        soup = BeautifulSoup(r.content, "html.parser")
        for option in soup.find_all("option"):
            self.citylist.append((option['value']))
        self.citylist.pop()  # remove others option

    def getcityname(self, driver):
        while True:
            try:
                return driver.find_element(By.ID, "uiv2-selection").text.strip()
            except:
                print("cityname not found, trying again...")
                time.sleep(5)
                pass

    def addcategorypages(self, content, db):
        global which_categories
        self.category_pages.clear()
        soup = BeautifulSoup(content, "html.parser")
        cat = soup.find_all("div", class_="uiv2-search-category-listing-cover")
        links = list()
        for i in which_categories:
            subcats = cat[i].find_all("div", class_="DropDownColum")
            for subcat in subcats:
                links.extend(subcat.ul.find_all("a"))
                for link in links:
                    # categories are contained in the url
                    categories = link['href'].split("/")[2:-1]
                    self.category_pages[link['href']] = categories
                    for category in categories:
                        db.getcategoryid(category)

    def nextcity(self, db, driver):
        temp = -1
        while temp == -1:
            if(len(self.citylist) > 0):
                val = self.citylist.pop()
            else:
                return None
            driver.get(baseurl + "skip_explore/?c=" + val + "&l=0&s=0&n=/")
            print("getting city name...")
            city_name = self.getcityname(driver)
            print(city_name + " - done")
            # will return -1 if data has already been collected for city
            temp = db.insertcity(city_name)
        s = requests.Session()
        while True:
            try:
                r = s.get(baseurl + "skip_explore/?c=" + val + "&l=0&s=0&n=/")
                r = s.get(baseurl + "product/all-categories")
                break
            except:
                print("connection problem, retrying...")
                pass
        print("retrieving categories...")
        self.addcategorypages(r.content, db)
        print("done")
        return 1
