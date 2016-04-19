import pymysql


class DB:

    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1', port=3306, user='root', passwd='youwish', db='bbdata', charset='utf8mb4')
        self.cur = self.conn.cursor()
        self.currentcityid = None
        sql = 'Select * FROM cities'
        self.cur.execute(sql)  # are we resuming a previous collecting session?
        if(self.cur.rowcount > 0):
            sql = "SELECT id FROM cities ORDER BY id DESC LIMIT 1"
            self.cur.execute(sql)
            cityid = self.cur.fetchone()[0]
            sql = "SELECT id FROM products WHERE city_id=(% s)"
            self.cur.execute(sql, (int(cityid)))
            prodlist = self.cur.fetchall()
            for prod in prodlist:
                sql = "DELETE FROM prod_cat WHERE prod_cat.prod_id= (% s)"
                self.cur.execute(sql, (int(prod[0])))
            sql = "DELETE FROM products WHERE city_id= (% s)"
            self.cur.execute(sql, (int(cityid)))
            sql = "DELETE FROM cities ORDER BY id DESC LIMIT 1"
            # the last city should be redone as it may be incomplete
            self.cur.execute(sql)
            self.conn.commit()

    def insertcity(self, city):
        sql = "SELECT * FROM cities WHERE name=(% s)"
        self.cur.execute(sql, (city))
        if(self.cur.rowcount > 0):
            return -1  # already collected
        else:
            sql = "INSERT INTO cities (name) VALUES (% s)"
            self.cur.execute(sql, (city))
            self.conn.commit()
            self.currentcityid = self.cur.lastrowid
            return self.currentcityid

    def getbrandid(self, brand):
        sql = "SELECT * FROM brands WHERE name=(% s)"
        self.cur.execute(sql, (brand))
        if(self.cur.rowcount == 1):
            return self.cur.fetchone()[0]
        else:
            sql = "INSERT INTO brands (name) VALUES (% s)"
            self.conn.commit()
            self.cur.execute(sql, (brand))
            return self.cur.lastrowid

    def getcategoryid(self, category):
        sql = "SELECT * FROM categories WHERE name=(% s)"
        self.cur.execute(sql, (category))
        if(self.cur.rowcount == 1):
            return self.cur.fetchone()[0]
        else:
            sql = "INSERT INTO categories (name) VALUES (% s)"
            self.cur.execute(sql, (category))
            self.conn.commit()
            return self.cur.lastrowid

    def insertproduct(self, product, currentcategories):
        brand_id = self.getbrandid(product['brand'])
        sql = "INSERT INTO products VALUES (NULL, % s, %s, %s, %s, %s, %s, %s)"
        try:
            self.cur.execute(sql, (product['prod_name'], brand_id, product['price'], product[
                'discount'], product['quantity'], product['unit'], self.currentcityid))
        except:
            print("duplicate product")
        self.conn.commit()
        prod_id = self.cur.lastrowid
        for category in currentcategories:
            category_id = self.getcategoryid(category)
            sql = "INSERT INTO prod_cat VALUES (%s, %s)"
            self.conn.commit()
            self.cur.execute(sql, (category_id, prod_id))
        return prod_id
