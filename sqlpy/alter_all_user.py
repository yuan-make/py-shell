#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*- 
import sys,os,string
import MySQLdb
db = MySQLdb.connect( host = '192.168.143.233',user = 'root',passwd = 'jproot' ,db ='js_xiudang',port = 3306 )
new_table = ('js_uorder_main','js_uorder_main_extend','js_uorder_main_seller','js_uorder_info','js_uorder_info_extend','js_uorder_goods','js_uorder_activity_relation','js_uorder_address','js_uorder_deliver')
cursor = db.cursor()
for dbnum in range(4):
    dbname="js_order_user"+str(dbnum)
    for tbtp in  range(len(new_table)):
        tbid_min=dbnum*128
        tbid_max=tbid_min+128
        for table_id in range(tbid_min,tbid_max):
            cursor.execute("describe %s.%s_%d last_modified" %(dbname,new_table[tbtp],table_id))
            data=cursor.fetchone()
            if(data):
                print "exist"
            else:
                cursor.execute("alter  table   %s.%s_%d ADD COLUMN `last_modified`  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP" %(dbname,new_table[tbtp],table_id))
                print "add  clounm ok!"
db.close()
