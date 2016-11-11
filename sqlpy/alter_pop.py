#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*- 
import sys,os,string
import MySQLdb
db = MySQLdb.connect( host = '192.168.143.233',user = 'root',passwd = 'jproot' ,db ='js_xiudang',port = 3306 )
cursor = db.cursor()
for dbnum in range(4):
    dbname="js_order_pop"+str(dbnum)
    tbid_min=dbnum*128
    tbid_max=tbid_min+128
    for table_id in range(tbid_min,tbid_max):
        #print "ALTER TABLE %s.js_sorder_info_%d ADD COLUMN soi_country INT(11) DEFAULT 0 NULL COMMENT '国家编码' AFTER soi_pay_no" %(dbname,table_id)
         cursor.execute("ALTER TABLE %s.js_sorder_goods_%d  DROP COLUMN sg_picking_time" %(dbname,table_id))
         print "%s.js_sorder_goods_%d  alter ok  !" %(dbname,table_id)
db.close()
