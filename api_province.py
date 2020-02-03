import requests
from base.conn_base import BaseFun
from utlis import BASE_DIR

data_list = list()


class Prov(BaseFun):
    url = BaseFun.city_url()

    def __init__(self):
        self.res_data = requests.get(self.url)
        self.response_data = self.res_data.json()
        self.conn = BaseFun.conn_database('ncov')
        BaseFun.write_json(BASE_DIR + '/data/api_province_v2.json', self.response_data)

    def read_data(self):
        res_data = BaseFun.read_json(BASE_DIR + '/data/api_province_v2.json')
        return res_data['newslist']

    def data_4_list(self):
        for res in self.read_data():
            data_list.append([
                res.get('provinceName'),
                res.get('provinceShortName'),
                res.get('confirmedCount'),
                res.get('suspectedCount'),
                res.get('curedCount'),
                res.get('deadCount'),
                res.get('comment'),
                str(res.get('cities')),
            ])

    def update_sql(self):
        for i in range(len(data_list)):
            self.sql = "update api_province_v2 set provinceName=%s, provinceShortName=%s, confirmedCount=%s, suspectedCount=%s, curedCount=%s, deadCount=%s, comment=%s, cities=%s where provinceShortName=" + '"' + \
                       data_list[i][1] + '"'
            # 获取一个光标
            self.conn.cursor()

            # 连接并执行
            self.conn.cursor().execute(self.sql, [data_list[i][0], data_list[i][1], data_list[i][2], data_list[i][3],
                                                  data_list[i][4],
                                                  data_list[i][5], data_list[i][6], data_list[i][7]])
            # 涉及写操作注意要提交
            self.conn.commit()
        # 关闭光标对象
        self.conn.cursor().close()
        # 关闭数据库连接
        self.conn.close()

    def start(self):
        self.data_4_list()
        self.update_sql()

if __name__ == '__main__':
    update_data = Prov()
    update_data.start()
    print('数据更新成功！')
