import json

import pymysql


class BaseFun(object):
    @staticmethod
    def conn_database(data_name):
        """
        连接数据库方法
        :param data_name: 传入-数据库名称
        :return: 连接后返回，conn
        """
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database=data_name,
            charset='utf8')
        print("连接数据库成功", conn.cursor())
        return conn

    @staticmethod
    def city_url():
        """
        各市级疫情数据api，只有城市情况
        :return:city_url
        """
        city_url = 'http://api.tianapi.com/txapi/ncovcity/index?key=fe8da86ad04723b18a2c590f47c89d91'
        print('连接【各市级】疫情数据api，成功')
        return city_url

    @staticmethod
    def prov_url():
        """
        各省级疫情数据api，包含新闻，全汇总
        :return: prov_rul
        """
        prov_rul = 'http://api.tianapi.com/txapi/ncov/index?key=fe8da86ad04723b18a2c590f47c89d91'
        print('连接【各省级】疫情数据api，成功')
        return prov_rul

    @staticmethod
    def read_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            res_data = json.load(f)
        print('读取数据成功')
        return res_data

    @staticmethod
    def write_json(file_path, data):
        with open(file_path, 'w', encoding='utf-8')as f:
            json.dump(data, f)
        print('写入数据成功')
