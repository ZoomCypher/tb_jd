from pymongo import MongoClient
from keywords import bigCate, smallCate, brand_list 
import requests
import json
import time
import os

class TbSpider(object):

    def __init__(self):
        self.keyword = input('production keyword:')
        self.page = 1
        self.connection = MongoClient('localhost', 27017)
        self.db = self.connection['tb'] 
        self.items = self.db['items']
    
    def auto_keyword(self):
        """get keyword from index"""

        if len(smallCate.pop()) != 0:
            keyword = smallCate.pop()
        elif len(brand_list.pop()) != 0:
            keyword = brand_list.pop()
        return keyword
            
    def start_request(self):
        """
        functions:
            1. first request to get cookie and keep status
            2. modify element of 'q' and 'page' for loop
            3. get json to parse
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
        }
        # get cookie and keep cookie
        session = requests.session()
        session.get("https://s.m.taobao.com/", headers=headers)
        # organzie request header
        getData = {
                "event_submit_do_new_search_auction": "1",
                "search": "提交",
                "tab": "all",
                "_input_charset": "utf-8",
                "topSearch": "1",
                "atype": "b",
                "searchfrom": "1",
                "action": "home:redirect_app_action",
                "from": "1",
                "q": self.keyword,
                "sst": "1",
                "n": "20",
                "buying": "buyitnow",
                "m": "api4h5",
                "abtest": "30",
                "wlsort": "30",
                "style": "list",
                "closeModues": "nav,selecthot,onesearch",
                "page": str(self.page)
            }

        preUrl = "http://s.m.taobao.com/search?"
        # add Referer and Host into headers
        headers.update(dict(Referer="http://s.m.taobao.com", Host="s.m.taobao.com"))
        # 抓取网页 sleep 5
        aliUrl = session.get(url=preUrl, params=getData, headers=headers)
        content = aliUrl.content
        dictInfo = json.loads(content.decode("utf-8", "ignore"))
        listItems = dictInfo['listItem']
        self.parse_data(listItems)

    def parse_data(self, listItems):
        """
        function: 
            1. parse data
        """
        for listItem in listItems:
            try:
                item = {}
                # 商品列表
                item['title'] = listItem['title']                 # 商品标题
                item['sold'] = listItem['sold']                   # 销量
                if listItem['commentCount']:
                    item['comment'] = listItem['commentCount']    # 意见
                # item['item_id'] = listItem['item_id']           # id
                item['shipping'] = listItem['shipping']           # 运费
                item['fastPostFee'] = listItem['fastPostFee']     # 快速运费
                # item['userId'] = listItem['userId']             # 用户id
                item['nick'] = listItem['nick']                   # 店名
                item['location'] = listItem ['location']          # 发货地址
                item['itemNumId'] = listItem['itemNumId']         # 商品编号
                item['originalPrice'] = listItem['originalPrice'] # 原价
                item['price'] = listItem['price']                 # 打折价格
                item['zkType'] = listItem['zkType']               # 折扣政策
                item['coinLimit'] = listItem['coinLimit']         # 金币折扣
                item['area'] = listItem['area']                   # 地点
            except Exception:
                pass
            else:
                print(item)
                self.save_data(item)
    
    def save_data(self, item):
        """
        save to mongodb
        """ 
        try:
            self.item.insert(dict(item))
        except Exception:
            pass
        
    def run(self):
        """
        main entrance
        """
        while self.page < 101:
            self.start_request()
            time.sleep(2)
            self.page += 1
        print('done!')

if __name__ == "__main__":
    
    tb = TbSpider()
    tb.run()
        
        
