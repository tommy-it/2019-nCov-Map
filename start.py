from api_city import City
from api_desc import Desc
from api_news import News
from api_province import Prov


class Start(object):
    def __init__(self):
        Prov().start()
        print('全省数据更新-成功')
        News().start()
        print('新闻数据更新-成功')
        Desc().start()
        print('全国数据更新-成功')
        City().start()
        print('全市数据更新-成功')
        print('--------------')
        print('全数据更新-成功')

if __name__ == '__main__':
    Start()
