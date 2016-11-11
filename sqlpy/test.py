#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
import os
import sys

for root,dirs,files in os.walk('/data/conf/redis'):
    print  root
    print  dirs
    print  files
