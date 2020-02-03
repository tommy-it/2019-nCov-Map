import requests

from base.conn_base import BaseFun
from utlis import BASE_DIR, time_change

data_list = list()


class News(BaseFun):
    url = BaseFun.prov_url()

    def __init__(self):
        self.res_data = requests.get(self.url)
        self.response_data = self.res_data.json()
        self.conn = BaseFun.conn_database('ncov')
        BaseFun.write_json(BASE_DIR + '/data/api_desc.json', self.response_data)

    def read_data(self):
        res_data = BaseFun.read_json(BASE_DIR + '/data/api_desc.json')
        return res_data['newslist'][0]['news']

    def insets_sql(self):
        for res in self.read_data():
            if 'provinceName' in res.keys():
                # 更新sql语句
                sql = "INSERT INTO api_news (id, pubDate, pubDateStr, title, summary,infoSource,sourceUrl, provinceId, provinceName, createTime,modifyTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE id = id"

                # 获取一个光标
                cursor = self.conn.cursor()

                # 连接并执行
                cursor.execute(sql, [res['id'], time_change(res['pubDate']), res['pubDateStr'], res['title'],
                                     res['summary'], res['infoSource'], res['sourceUrl'], res['provinceId'],
                                     res['provinceName'], time_change(res['createTime']),
                                     time_change(res['modifyTime'])])
            else:
                sql = "INSERT INTO api_news (id, pubDate, pubDateStr, title, summary,infoSource,sourceUrl, provinceId, createTime, modifyTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE id = id"

                # 获取一个光标
                cursor = self.conn.cursor()
                cursor.execute(sql, [res['id'], time_change(res['pubDate']), res['pubDateStr'], res['title'],
                                     res['summary'], res['infoSource'], res['sourceUrl'], res['provinceId'],
                                     time_change(res['createTime']),
                                     time_change(res['modifyTime'])])

                # 涉及写操作注意要提交
                self.conn.commit()
                # 关闭光标对象
                cursor.close()
        # 关闭数据库连接
        self.conn.close()

    def start(self):
        self.insets_sql()

if __name__ == '__main__':
    insets_data = News()
    insets_data.start()
    print('数据更新成功！')
