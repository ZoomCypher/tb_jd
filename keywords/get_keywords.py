import requests
from lxml import etree

class GetList(object):
    
    def __init__(self):
        self.ListIndex = 'https://www.jd.com/allSort.aspx'
        self.BrandIndex = 'https://www.jd.com/brand.aspx'

    def run(self):
        res = requests.get(self.ListIndex)
        res.encoding='utf-8'
        html = res.text
        html = etree.HTML(html)
        # save main catelog
        bigCate = html.xpath("//div[@class='items']/dl/dt/a/text()")
        self.saveFile(bigCate, 'bigCate')
        # save tiny catelog
        smallCate = html.xpath("//div[@class='items']/dl/dt/a/text()")
        self.saveFile(smallCate, 'smallCate')
        # brand list
        brand_res = requests.get(self.BrandIndex)
        brand_res.encoding='utf-8'
        brand_html = brand_res.text
        print(brand_html)
        brand_html = etree.HTML(brand_html)
        brand_list = brand_html.xpath("//div/span[@class='b-name']/a/text()")
        self.saveFile(brand_list, 'brand_list')
        print("finish!")

    def saveFile(self, data, name):
        parse_data = name + " = " + str(data)
        with open('%s.py' % name, 'w', encoding='utf-8') as f:
            f.write(parse_data)

    def createfiles(self, filepathname):
        try:
            os.makedirs(filepathname)
        except Exception as err:
            print(str(filepathname) + "existed")

if __name__ == '__main__':
    getlist = GetList()
    getlist.run()