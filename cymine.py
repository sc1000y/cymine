# -*- coding: utf-8 -*-
import requests
#from nltk import clean_html
from bs4 import BeautifulSoup
import codecs
import jieba
import jieba.analyse
import matplotlib.pyplot as plt
import random
import numpy
import pyparsing
from scipy.misc import imread,imresize
from wordcloud import WordCloud,ImageColorGenerator
"""
Cymine


"""

headers = {
    "Host": "m.weibo.cn",
    "Referer": "https://m.weibo.cn/u/--",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) "
                  "Version/9.0 Mobile/13B143 Safari/601.1",
}

params = {"uid": "{uid}",
          "luicode": "--",
          "featurecode": "--",
          "type": "uid",
          "containerid":"--",
          "value":"--",
          "page": "{page}"}

url="https://m.weibo.cn/api/container/getIndex"

txtName="weibo2.txt"
def fetch_data(uid=None, container_id=None):
    """
    抓取数据，并保存到TXT文件中
    :return:
    """
    page = 0
    total = 4754
    blogs = []
    for i in range(0, total // 10):
        params['uid'] = uid
        params['page'] = str(page)
        #params['containerid'] = container_id
        res = requests.get(url, params=params, headers=headers)
        #print(res.json())
        
        cards = res.json().get("data").get("cards")
        #print(cards)
        
        for card in cards:
            # 每条微博的正文内容
            if card.get("card_type") == 9:
                text = card.get("mblog").get("text")
                #text = clean_html(text)
                soup=BeautifulSoup(text)
                text=soup.get_text()
                blogs.append(text)
        page += 1
        print("抓取第{page}页，目前总共抓取了 {count} 条微博".format(page=page, count=len(blogs)))
        with codecs.open(txtName, 'w', encoding='utf-8') as f:
            f.write("\n".join(blogs))
#def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
#    return "hsl(0, 0%%, %d%%)" % random.randint(20, 100)

def generate_image():
    data = []
    jieba.analyse.set_stop_words("./stopwords2.txt")
    
    with codecs.open(txtName, 'r', encoding="utf-8") as f:
        for text in f.readlines():
            data.extend(jieba.analyse.extract_tags(text, topK=20))
        data = " ".join(data)
        mask_img = imread('./tst3.jpg')
        '''
        wordcloud = WordCloud(
            font_path='msyh.ttc',
            background_color='white',
            mask=mask_img
        ).generate(data)
        
        #plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3),
        #           interpolation="bilinear")
        
        '''
        image_colors = ImageColorGenerator(mask_img)
        wordcloud = WordCloud(background_color='white',  # 背景颜色
               font_path='msyh.ttc',
               mask=mask_img,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
               random_state=42, ).generate(data)
        plt.imshow(wordcloud.recolor(color_func=image_colors))
        plt.axis('off')
        plt.savefig('./fun.jpg', dpi=1600)
if __name__=="__main__":
    fetch_data(---);
    generate_image()