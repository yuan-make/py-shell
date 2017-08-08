#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*- 
import sys,os,string
import MySQLdb
db = MySQLdb.connect( host = '192.168.143.233',user = 'xxxxx',passwd = 'xxxxx' ,db ='js_xiudang',port = 3306 )
cursor = db.cursor()
new_table=('js_sorder_address_history','js_sorder_deliver','js_sorder_deliver_history','js_sorder_delivery_code','js_sorder_delivery_code_history','js_sorder_gift_coupon','js_sorder_gift_goods','js_sorder_info_map','js_sorder_info_map_history','js_sorder_orderno_map','js_sorder_pay','js_sorder_payno_map','js_sorder_refund','js_sorder_relation','tmp_business_order','tmp_user_order')
for tbname in range(len(new_table)):
    cursor.execute("describe js_order_common.%s last_modified" %(new_table[tbname]))
    data=cursor.fetchone()
    if(data):
        print "column exist!"
    else:
        cursor.execute("alter table js_order_common.%s ADD COLUMN `last_modified`  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP" %(new_table[tbname]))
        print "add   js_order_common.%s ok" % ( new_table[tbname] )
db.close()
