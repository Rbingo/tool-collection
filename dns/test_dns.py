#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dns.resolver
import os
import requests
iplist=[]
appdomain="www.ctrip.com"
def get_iplist(domain=""): 
	try: 
		A=dns.resolver.resolve(domain,'A') 
	except Exception(e):
		print("dns resolver error:"+str(e)) 
	for i in A.response.answer: 
		for j in i.items: 
			if j.rdtype == 1: 
				iplist.append(j.address) 
				return True
def checkip(ip): 
	checkurl=ip+":80" 
	getcontent="" 
	try: 
		r = requests.get(checkurl,headers={"Host":appdomain}) 
		getcontent=r.content 
	finally: 
		print(getcontent) 
		if getcontent=="": 
			print(ip+":80端口正常  [ok]" )
		else: 
			print(ip+":80端口异常  [error]")

if __name__=="__main__": 
	if get_iplist(appdomain) and len(iplist)>0: 
		for ip in iplist: 
			checkip(ip) 
		else: 
			print("dns resolver error")