from datetime import datetime

import requests

from base.conn_base import BaseFun
from utlis import BASE_DIR, time_change

data_list = list()
now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d')


class Desc(BaseFun):
    url = BaseFun.prov_url()

    def __init__(self):
        self.res_data = requests.get(self.url)
        self.response_data = self.res_data.json()
        self.conn = BaseFun.conn_database('ncov')
        BaseFun.write_json(BASE_DIR + '/data/api_desc.json', self.response_data)

    def read_data(self):
        res_data = BaseFun.read_json(BASE_DIR + '/data/api_desc.json')
        return res_data['newslist'][0]['desc']

    def data_4_list(self):
        for res in self.read_data():
            data_list.append(self.read_data()[res])
        # print(data_list)

    def insets_sql(self):
        sql = "INSERT INTO api_desc (createTime,modifyTime,infectSource,passWay,imgUrl,dailyPic,countConfirmedCount,countSuspectedCount,countCuredCount,countDeadCount,virus,remark1,remark2,generalRemark,ccTime) " \
              "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) " \
              "ON DUPLICATE KEY UPDATE ccTime=%s,modifyTime=%s,countConfirmedCount=%s,countSuspectedCount=%s,countCuredCount=%s,countDeadCount=%s"
        # 获取一个光标
        self.conn.cursor()

        # 连接并执行
        int_val = (time_change(data_list[1]), time_change(data_list[2]), data_list[3], data_list[4],
                   data_list[5], data_list[6], data_list[10], data_list[11], data_list[12], data_list[13],
                   data_list[20], data_list[21], data_list[22],
                   data_list[26], formatted_date)
        upd_val = (formatted_date, time_change(data_list[2]), data_list[10],
                   data_list[11], data_list[12], data_list[13])
        val = (*int_val, *upd_val)
        self.conn.cursor().execute(sql, val)
        # 涉及写操作注意要提交
        self.conn.commit()
        # 关闭光标对象
        self.conn.cursor().close()
        # 关闭数据库连接
        self.conn.close()

    def start(self):
        self.data_4_list()
        self.insets_sql()

if __name__ == '__main__':
    insets_data = Desc()
    insets_data.start()
    print('数据更新成功！')