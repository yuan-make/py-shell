#/bin/env  python
# -*- coding: utf-8 -*-

"""
info: migrate redis cache （redist to twemproxy）
date: 2016-05-12
author: DcHuang
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


"""创建线程执行导出导入函数"""
src_keys_all=src_redis.keys()
pool = ThreadPool(10)
results = pool.map(dump_restore,src_keys_all)
pool.close() 
pool.join()

new_time = int(time.time())

################
print "use time(s):",str(new_time - now_time)
