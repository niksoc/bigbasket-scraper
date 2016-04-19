#Bigbasket Scraper
Collects product details from Bigbasket and stores it in a MySQL database for data analysis. Product name, price, discount, categories, quantity, unit, brand and cityname are collected. A crawl delay of approx. 10 seconds is in place. Written in Python v3.

---------------------------------

##Usage
*All instructions assume usage of python3.*

1. Execute the commands in mysql_setup in the mysql shell.
2. Install requirements with `pip install -r requirements.txt`.
3. Download phantomjs from [here](https://dn-cnpm.qbox.me/dist/phantomjs/phantomjs-2.1.1-linux-x86_64.tar.bz2) for linux or from an appropriate source and place the executable found in the bin directory into the project directory. 
4. To run execute `python collectdata.py`

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
 
---------------------------------

##Data Organisation
```
mysql> show tables;
+------------------+
| Tables_in_bbdata |
+------------------+
| brands           |
| categories       |
| cities           |
| prod_cat         |
| products         |
| test             |
+------------------+ 

mysql> describe products;

+-----------+------------------+------+-----+---------+----------------+
| Field     | Type             | Null | Key | Default | Extra          |
+-----------+------------------+------+-----+---------+----------------+
| id        | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| prod_name | varchar(70)      | NO   |     | NULL    |                |
| brand_id  | int(10) unsigned | YES  |     | NULL    |                |
| price     | float            | NO   |     | NULL    |                |
| discount  | float            | NO   |     | NULL    |                |
| quantity  | float            | NO   |     | NULL    |                |
| unit      | varchar(10)      | YES  |     | NULL    |                |
| city_id   | int(10) unsigned | NO   | MUL | NULL    |                |
+-----------+------------------+------+-----+---------+----------------+

mysql> describe prod_cat;

+---------+------------------+------+-----+---------+-------+
| Field   | Type             | Null | Key | Default | Extra |
+---------+------------------+------+-----+---------+-------+
| cat_id  | int(10) unsigned | NO   |     | NULL    |       |
| prod_id | int(10) unsigned | NO   |     | NULL    |       |
+---------+------------------+------+-----+---------+-------+
```
This table contains the product id and the category id of the category it belongs to. There may be be more than one category for a product, and there will be multiple rows.

The other tables just contain the id and name columns.
