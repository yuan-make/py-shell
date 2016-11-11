#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*- 
import sys,os,string
import MySQLdb
db = MySQLdb.connect( host = '192.168.143.233',user = 'root',passwd = 'jproot' ,db ='js_xiudang',port = 3306 )
new_table = ('js_sorder_goods')
cursor = db.cursor()
for dbnum in range(4):
    dbname="js_order_pop"+str(dbnum)
    for tbtp in  range(1):
        tbid_min=dbnum*128
        tbid_max=tbid_min+128
        for table_id in range(tbid_min,tbid_max):
            cursor.execute("alter  table   %s.%s_%d  DROP COLUMN sg_picking_time;" %(dbname,new_table[tbtp],table_id))
            print "alter table   %s.%s_%d ok!" %(dbname,new_table[tbtp],table_id)
db.close()
