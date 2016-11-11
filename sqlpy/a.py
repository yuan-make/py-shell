#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import sys
import getopt
import time
## 变量定义
shortargs='he:f:'
longargs=['help','execute=','file=']
HOST='192.168.143.233'
USER='root'
PASSWORD='jproot'
PORT=3306
SOCKET='/data/mysql/3306/var/run/mysql.sock'


def usage():
    print '''
         -h or -H or --help  show usage
         '''
##########################################
#函数：get_table_from_sql
#参数：sql
#返回值:  table_name
#########################################
def get_table_from_sql(sql):
    sql_sp=sql.split()
    change_type=sql_sp[0].upper()
    if change_type == "UPDATE":
         tb_sp=sql_sp[1].split()
         return tb_sp
    if  change_type == "INSERT":
        return sql_sp[2]
    if change_type == "ALTER":
        return sql_sp[2]
    if change_type == "DELETE":
        return sql_sp[2]

##########################################
#函数：get_db_from_name
#参数：tablename
#返回值:  dbname_pre
######################################### 
def get_db_from_table(tablename):
    user_table_prefix = ['js_uorder_goods','js_uorder_deliver','js_uorder_main_seller',
                        'js_uorder_main_extend','js_uorder_main','js_uorder_info_extend',
                        'js_uorder_info','js_uorder_activity_relation','js_uorder_address']
    pop_table_prefix  = ['js_sorder_info_extend','js_sorder_info','js_sorder_goods']
    comm_table_prefix = ['js_sorder_address_history','js_sorder_deliver','js_sorder_deliver_history','js_sorder_delivery_code','js_sorder_delivery_code_history','js_sorder_exchange',
                        'js_sorder_delivery_code','js_sorder_delivery_code_history','js_sorder_exchange',
                        'js_sorder_gift_coupon','js_sorder_gift_goods','js_sorder_info_map','js_sorder_info_map_history',
                        'js_sorder_orderno_map','js_sorder_pay','js_sorder_payno_map','js_sorder_refund','js_sorder_relation']
    whouse_table_prefix = ['js_worder_info','js_worder_info_extend','js_worder_goods']
    if tablename in user_table_prefix:
        return "js_order_user"
    if tablename in pop_table_prefix:
        return "js_order_pop"
    if tablename in comm_table_prefix:
        return "js_order_common"
    if tablename in  whouse_table_prefix:
        return "js_order_warehouse"


##########################################
#函数：mysql 连接
#参数：host,user,pwd,db,port
#返回值:  conn
######################################### 
def db_connect(host,user,pwd,db,port):
    try:
        return MySQLdb.connect( host=host,user=user,passwd=pwd,db=db,port=port )
    except Exception,e:
        print "%s : Erro : Connect Erro %s:%s - %s" % (time.ctime(),host,port,e)
        return None


##########################################
#函数：alter
#参数：_tbname,_dbname,sql
#返回值:
######################################### 
def get_table_sql(_dbname,_tbname,sql):
    sp_sql=sql.split()
    change_type=sp_sql[0].upper()
    if change_type == "ALTER":
        sp_sql[2]=_dbname+"."+_tbname
        str_sql=(' ').join(sp_sql)
        return str_sql
    if  change_type == "UPDATE":
        sp_sql[1]=_dbname+"."+_tbname
        str_sql=(' ').join(sp_sql)
        return str_sql
    if  change_type == "INSERT":
        sp_sql[2]=_dbname+"."+_tbname
        str_sql=(' ').join(sp_sql)
        return str_sql
    if  change_type == "DELETE":
        sp_sql[2]=_dbname+"."+_tbname
        str_sql=(' ').join(sp_sql)  
        return str_sql


    

##########################################
#函数：change  table  sql
#参数：tablename  sql
#返回值:sql
######################################### 
def mult_schema(sql):
    _tbname=get_table_from_sql(sql)
    _dbname=get_db_from_table(_tbname)
    if _dbname == "js_order_pop" or _dbname == "js_order_user":
        for dbnum in range(4):
            dbname=_dbname+str(dbnum)
            tbid_min=dbnum*128
            tbid_max=tbid_min+128
            for table_id in range(tbid_min,tbid_max):
                table_name=_tbname+str(table_id)
                print get_table_sql(dbname,table_name,sql)
    else:
        get_table_sql(_dbname,_tbname,sql)


mult_schema("alter table js_uorder_goods add cloumn id int not null;")

#def main():
#    opts,args=getopt.getopt(sys.argv[1:],shortargs,longargs)
#    if args:
#        print 'please input -h or --help for  detail'
#        sys.exit(1)
#    print "%s,%s" %(opts,args)
#    for  opt,val in opts:
#        if opt in ('-h','--help'):
#            usage()         
# print get_table_from_sql("update jsorder.js_ims_inventory SET ii_locked_stock=ii_locked_stock+2 WHERE")
# print get_db_from_table("js_sorder_orderno_map")
# db=db_connect(HOST,USER,PASSWORD,"js_xiudang",PORT)
# cursor=db.cursor()
# cursor.execute("select version()")
# data=cursor.fetchone()
# print data
# db.close
