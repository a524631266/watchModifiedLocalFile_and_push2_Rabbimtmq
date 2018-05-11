# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 09:13:26 2018

@author: dell
"""
import pika

#from 

ipAddress = "localhost"#需要指定服务器地址
ipAddress = "192.168.10.65"#需要指定服务器地址
port = 5672
queue_name = "nerualtime2"#需要指定队列名称
exchange_name= "tsne"#需要指定交换机名称 默认为"" 这里需要确定是什么类型的exchange ： 
virtual_host = "/had_host"
username = 'had'
password = 'had123'


#创建消息队列账号密码
credentials = pika.PlainCredentials(username,password)
connection = pika.BlockingConnection(pika.ConnectionParameters(ipAddress,port,virtual_host,credentials))
channel = connection.channel()


#channel.queue_declare(queue='nerualtime0')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
channel.start_consuming()
#connection.close()
channel.stop_consuming()