import requests
import re
import pymysql

api_key = ""  # set this to be your google api key
mysql_passwd = ""  # set this to be your mysql password


def getcitycoords(cityname):
    cityname = re.sub(" ", "+", cityname)
    print(cityname)
    while(True):
        try:
            r = requests.get(
                "https://maps.googleapis.com/maps/api/geocode/json?address=" + cityname + "&key=" + api_key)
            break
        except:
            pass
    response_json = r.json()
    latitude = response_json['results'][0]['geometry']['location']['lat']
    longitude = response_json['results'][0]['geometry']['location']['lng']
    return latitude, longitude


def storecoords():
    try:
        conn = pymysql.connect(
            host='127.0.0.1', port=3306, user='root', passwd=mysql_passwd, db='bbdata', charset='utf8mb4')
        cur = conn.cursor()
        sql = 'SELECT * FROM cities'
        cur.execute(sql)
        sql = "ALTER TABLE cities ADD (latitude DOUBLE, longitude DOUBLE)"
        # cur.execute(sql)
        for row in cur.fetchall():
            cityname = row[1]
            coords = getcitycoords(cityname)
            sql = "UPDATE cities SET latitude=% s, longitude=% s WHERE id=% s"
            cur.execute(sql, (coords[0], coords[1], row[0]))
            conn.commit()
    finally:
        conn.close()


storecoords()
