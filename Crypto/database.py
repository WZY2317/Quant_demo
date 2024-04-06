from influxdb import InfluxDBClient
client = InfluxDBClient('192.168.1.8', 8086,'admin','admin') # 初始化
print(client.get_list_database())  # 显示所有数据库名称
client.create_database('testdb') # 创建数据库
print(client.get_list_database())  # 显示所有数据库名称
client.drop_database('testdb') # 删除数据库
print(client.get_list_database()) # 显示所有数据库名称