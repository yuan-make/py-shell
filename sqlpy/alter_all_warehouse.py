#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*- 
import sys,os,string
import MySQLdb
db = MySQLdb.connect( host = '192.168.143.233',user = 'root',passwd = 'jproot' ,db ='js_xiudang',port = 3306 )
cursor = db.cursor()
new_table=('js_worder_goods','js_worder_info','js_worder_info_extend')
id=['201501','201502','201503','201504','201505','201506','201507','201508','201509','201510','201511','201512','201601','201602','201603','201604','201605','201606','201607','201608']
for tbname in range(len(new_table)):
    for idnum in range(len(id)):    
        cursor.execute("describe js_order_warehouse.%s_%s last_modified" %(new_table[tbname],id[idnum]))
        data=cursor.fetchone()
        if(data):
            print "exist!"
        else:
            cursor.execute("alter  table js_order_warehouse.%s_%s ADD COLUMN last_modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP" %(new_table[tbname],id[idnum]))
            print "alter ok!!"
db.close()
