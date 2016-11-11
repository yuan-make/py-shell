#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*- 
import sys,os,string
import MySQLdb
db = MySQLdb.connect( host = '192.168.143.233',user = 'root',passwd = 'jproot' ,db ='js_xiudang',port = 3306 )
cursor = db.cursor()
new_table = ('js_sorder_goods','js_sorder_info_extend','js_sorder_info')
for dbnum in range(4):
    dbname="js_order_pop"+str(dbnum)
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
            cursor.execute("create table  if not exists %s.%s_%d like template_pop.%s" % (dbname,new_table[tbtp],table_id,new_table[tbtp]))
            print "%s.%s_%d copy  success !" % (dbname,new_table[tbtp],table_id)

db.close()
