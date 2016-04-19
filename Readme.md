#Bigbasket Scraper
Collects product details from Bigbasket and stores it in a MySQL database for data analysis. Product name, price, discount, categories, quantity, unit, brand and cityname are collected. A crawl delay of approx. 10 seconds is in place. Written in Python v3.

---------------------------------

##Usage
*All instructions assume usage of python3.*
1. Execute the commands in mysql_setup in the mysql shell.
2. Install requirements with `pip install -r requirements.txt`.
3. Download phantomjs from [here](https://dn-cnpm.qbox.me/dist/phantomjs/phantomjs-2.1.1-linux-x86_64.tar.bz2) for linux or from an appropriate source and place the executable found in the bin directory into the project directory. 
3. To run execute `python collectdata.py`

Was written as a learning exercise and does not have a UI of any sort in place. By default it only collects data from the top level categories Fruits and Vegetables and Groceries and Staples sections. To change this, modify the which_categories variable in city.py.

```python
which_categories = [0, 1]
``` 
The indices correspond to the order the top level categories are displayed in [their categories page](http://www.bigbasket.com/product/all-categories/)

---------------------------------

##Tools/Libraries used
- Selenium w/PhantomJS
- Requests
- BeautifulSoup4
- pymysql
 
