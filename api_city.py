from base.conn_base import BaseFun
from utlis import BASE_DIR

city_list = list()


class City(BaseFun):
    def __init__(self):
        self.conn = BaseFun.conn_database('ncov')
        self.res_data = BaseFun.read_json(BASE_DIR + '/data/api_province_v2.json')

    def data_4_list(self):
        for i in self.res_data['newslist']:
            for j in i['cities']:
                # 城市名称列表
                # print(j)
                city_list.append(j)
        print('城市名称-数据处理成功！')

    def write_data(self):
        BaseFun.write_json(BASE_DIR + '/data/api_city.json', city_list)

    def read_data(self):
        res_datas = BaseFun.read_json(BASE_DIR + '/data/api_city.json')
        return res_datas

    def update_sql(self):
        for res in self.read_data():
            sql = "update api_city set confirmedCount=%s, suspectedCount=%s, curedCount=%s, deadCount=%s where cityName =%s"

            # 获取一个光标
            self.conn.cursor()

            # 连接并执行
            self.conn.cursor().execute(sql, [res['confirmedCount'], res['suspectedCount'], res['curedCount'],
                                             res['deadCount'],
                                             res['cityName']])

            # 涉及写操作注意要提交
            self.conn.commit()
            # 关闭光标对象
            self.conn.cursor().close()
        # 关闭数据库连接
        self.conn.close()

    def start(self):
        self.data_4_list()
        self.write_data()
        self.update_sql()


if __name__ == '__main__':
    update_data = City()
    update_data.start()
    print('数据更新成功！')
