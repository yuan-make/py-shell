#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*- 
import sys,os,string
import MySQLdb
db = MySQLdb.connect( host = '192.168.143.233',user = 'root',passwd = 'jproot' ,db ='js_xiudang',port = 3306 )
cursor = db.cursor()
id=['201501','201502','201503','201504','201505','201506','201507','201508','201509','201510','201511','201512','201601','201602','201603','201604','201605','201606','201607','201608']
for idnum in range(len(id)):    
    cursor.execute("alter  table js_order_warehouse.js_worder_info_%s DROP COLUMN soi_last_logistics" %(id[idnum]))
    print "alter  table js_order_warehouse.js_worder_info_%s ok" %(id[idnum])
db.close()
