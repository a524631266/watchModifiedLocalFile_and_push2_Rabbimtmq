# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 15:17:23 2018

@author: dell

生产者的功能主要是对生成的数据进行传递

"""
import pika
import json
import logging
#import pandas as pd
import numpy as np
#import scipy
from sklearn import manifold
#import matplotlib.pyplot as ppl
#import pika.exceptions as exceptions


logger = logging.getLogger("mylogger")


def catch_error(func):
    """
        通用装饰方法：
        获取rabbitmq错误执行情况并重新创建链接
    """
    try:
        import pika.exceptions as exceptions
        connect_exceptions = (
                exceptions.ChannelClosed,
                exceptions.ConnectionClosed,
                exceptions.AMQPChannelError
                )
    except ImportError:
        connect_exceptions =()
    def warp(self,*args,**kwargs):
        try:
            func(self,*args,**kwargs)
        except connect_exceptions as e:
            print("RabbitMQ error")
            logger.error('RabbitMQ error: %r, reconnect.', e)
            self.reconnect()#重新建立链接
            return func(self,*args,**kwargs)
    return warp


class Producer(object):
    ipAddress = "192.168.10.65"#需要指定服务器地址
    port = 5672
    route_key = "metann"
    queue_name = "nnqueue"#需要指定队列名称 没有的话就直接生成
    exchange_name= "nnexchange"#需要指定交换机名称 默认为"" 这里需要确定是什么类型的exchange ： 
    virtual_host = "neuralnetwork"
    username = 'rabbit'
    password = 'rabitpasswor'
    
    def __init__(self):
        
        self.reconnect()
    
    @catch_error
    def pushData(self,jsondata):
            #如何没有消息队列queuename名，默认创建一个队列名
        self.channel.queue_declare(queue=self.queue_name,durable=True)
        #绑定队列到交换机中，否则，队列无法接收从交换机传来的数据，也就是会瞬间删除掉
        self.channel.queue_bind(self.queue_name,self.exchange_name,self.route_key)
        #发送消息 routing_key为消息队列名称
        self.channel.basic_publish(exchange=self.exchange_name,
                              routing_key=self.route_key,
                              body=jsondata)#postPanelData()
#        except Exception:
#            logger.error("OtherError+++++++++++")
#            print("其他错误。。。。。。。。")
        
    def reconnect(self):
        #创建消息队列账号密码
        credentials = pika.PlainCredentials(self.username,self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.ipAddress,self.port,self.virtual_host,credentials))
        self.channel = self.connection.channel()
    
    def __del__(self):
        self.connection.close()
        print("Close the rabbitmq connection!!!!!")
        logger.info("Close the rabbitmq connection!!!!!")
    

def gen_jsondata100p100():
    return np.random.rand(100,100).tolist()

#生成模拟样本数据
def gen_neuron_testData(sample_n = 10000,input_D=10):
    gendata  =  []
#    fornum = int(np.sqrt(sample_n))
    for i in range(sample_n):
        gendata.append(np.random.rand(1,input_D).tolist()[0])
    label = np.random.randint(0,2,size=sample_n) #0 1平均分布
    return {"inputdata":gendata,"label":label}
#降低纬度，这里如果数据量很大，需要做其他处理（spark或其他方式）
def reductionTo2D(samplelist,n_components=2):
    tsne = manifold.TSNE(n_components=n_components, init='pca', random_state=0,perplexity=25.0,learning_rate=1.0,n_iter=10000)
    X_tsne = tsne.fit_transform(samplelist)
    return X_tsne

#在这里需要处理数据
def postPanelData():
#    with open("test.json") as f:
#        data = json.load(f)
    neuronName = "0"
    return json.dumps({neuronName:gen_jsondata100p100()})
    #return json.dumps(data)


#abc = reductionTo2D(gen_neuron_testData(10000,10)["inputdata"],2)
#ppl.scatter([x[0] for x in abc],[x[1] for x in abc])
