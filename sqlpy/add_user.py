#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*- 
import sys,os,string
import MySQLdb
db = MySQLdb.connect( host = '192.168.143.233',user = 'root',passwd = 'jproot' ,db ='js_xiudang',port = 3306 )
cursor = db.cursor()
new_table = ('js_uorder_main','js_uorder_main_extend','js_uorder_main_seller','js_uorder_info','js_uorder_info_extend','js_uorder_goods','js_uorder_activity_relation','js_uorder_address','js_uorder_deliver')
for dbnum in range(4):
    dbname="js_order_user"+str(dbnum)
    cursor.execute("create database IF NOT EXISTS %s" % dbname )
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print "\n"
    print "The database  %s create  success!" % dbname
    print "\n"
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"  
    for tbtp in range(len(new_table)):
        tbid_min=dbnum*128
        tbid_max=tbid_min+128
        for table_id in range(tbid_min,tbid_max):
           #print  "create table  if not exists %s.%s_%d like template_user.%s" % (dbname,new_table[tbtp],table_id,new_table[tbtp])
            cursor.execute("create table  if not exists %s.%s_%d like template_user.%s" % (dbname,new_table[tbtp],table_id,new_table[tbtp]))
            print "%s.%s_%d copy  success !" % (dbname,new_table[tbtp],table_id)

db.close()
