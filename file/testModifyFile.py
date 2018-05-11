# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 09:25:44 2018

@author: dell
"""

aa = open("file/test.txt","a+")

for x in range(100000000):
    if x%1000==0:    
        aa.writelines(str(x)+"\n")
aa.flush()
aa.close()
