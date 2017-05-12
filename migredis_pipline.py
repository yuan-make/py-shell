#/bin/env  python
# -*- coding: utf-8 -*-

"""
info: migrate redis cache （redist to twemproxy）
date: 2016-05-12
author: Make
"""

import redis
import os
import sys
import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


def usage():
    print "Usage: %s src['1.1.1.1:4500'] dst['2.2.2.2:14500']" % sys.argv[0]


try:
    src=str(sys.argv[1])
    dst=str(sys.argv[2])

    src_ip = src.split(':')[0]
    src_port = src.split(':')[1]

    dst_ip = dst.split(':')[0]
    dst_port = dst.split(':')[1]

except Exception,e:
    usage()
    sys.exit()

now_time = int(time.time())

"""connect redis"""
try:
    src_pool = redis.ConnectionPool(host=str(src_ip), port=int(src_port))  
    src_redis = redis.Redis(connection_pool=src_pool)
except:
    print  "src redis %s connection fail" % src
    sys.exit()

try:
    dst_pool = redis.ConnectionPool(host=str(dst_ip), port=int(dst_port))  
    dst_redis = redis.Redis(connection_pool=dst_pool)
except:
    print  "dst redis %s connection fail" % dst
    sys.exit()


"""导入导出"""
def dump_restore(key):

    """获取pttl"""
    s_pttl = src_redis.pttl(key)
    if s_pttl == -2 :
        return "1"
    elif s_pttl == -1 :
        s_pttl = 0
    else:
        s_pttl = 0

    """获取key的dump,并且restore 导入到新的redis中"""
    try:
        s_dump = src_redis.dump(key)
        if s_dump:
            d_status = dst_redis.restore(key,int(s_pttl),s_dump)
            #print "key:",str(key)," type:",str(src_redis.type(key))," pttl:",str(s_pttl) ##," d_status:",str(d_status)
    except:
        return "1"
	print "-----------restore error--------------"
    return "0"


def dump(keys_all):
    pipe=src_redis.pipeline()
    for  key in keys_all :
        pipe.dump(key)
    s_dump=pipe.execute()
    return s_dump


def getttl(keys_all):
    dpipe=src_redis.pipeline()
    for  key in keys_all :
        dpipe.pttl(key)
    s_ttl=dpipe.execute()
    for index in range(len(s_ttl)):
        if s_ttl[index] == -2 :
            return "1"
        elif s_ttl[index]  == -1 :
            s_ttl[index]  = 0
        elif s_ttl[index] == None:
            s_ttl[index] = 0
    return s_ttl

def  mig(dumpval,ttlarry,keysall):
    if len(dumpval) == len(ttlarry) :
        pipe=dst_redis.pipeline()
        for index in range(len(ttlarry)):
            if dumpval[index]:
                pipe.restore(keysall[index],ttlarry[index],dumpval[index]) 
        try:
            pipe.execute()
        except Exception,e:
            print Exception,e
    else:
        print "ttl <--------> dumpval"
        sys.exit(1)

 
def migsrc(keysall):
    ttlarry=getttl(keysall)
    dumpval=dump(keysall)
    if len(dumpval) == len(ttlarry) :
        pipe=dst_redis.pipeline()
        for index in range(len(ttlarry)):
            if dumpval[index]:
                pipe.restore(keysall[index],ttlarry[index],dumpval[index]) 
        try:
            pipe.execute()
        except Exception,e:
            print Exception,e
    else:
        print "ttl <--------> dumpval"
        sys.exit(1)


"""创建线程执行导出导入函数"""
src_keys_all=src_redis.keys()
pool = ThreadPool(20)
SIZE = 800
for index  in range(len(src_keys_all)/SIZE):
    pool.apply_async(migsrc,args=(src_keys_all[index*SIZE:index*SIZE+SIZE],))

pool.apply_async(migsrc,args=(src_keys_all[0-len(src_keys_all)%SIZE:],))
pool.close() 
pool.join()
#mig(dump(src_keys_all),getttl(src_keys_all),src_keys_all)
new_time = int(time.time())
print "use time(s):",str(new_time - now_time)
