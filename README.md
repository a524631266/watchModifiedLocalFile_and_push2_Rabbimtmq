# watchModifiedLocalFile_and_push2_Rabbimtmq
用来监控本地文件是否有更新，一旦更新数据就会把更新的数据按照业务逻辑输出数据到rabbitmq队列

某块分解

file 为指定的监控文件路径 ，一旦file中有文件修改就会更新数据到rabbitmq

observer 为定义了监控对象，其中使用的是watchdog包

rabbitmq为与服务器定义的关键内容，其中producer.py为数据生产者，定义了账户、密码、ip地址、以及相应的虚拟用户名和它下面管理的交换机名称以及队列名称

utils 为定义了一些工具类，公用的方法







入口总程序，run.py 使用python中的click包作为修饰命令操作的方法,定义了整个程序应用方法

