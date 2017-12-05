"""
使用filder提取微信公众号消息
"""
import requests
import logging
import re
import html
import json
from multiprocessing import Pool
import os


logging.basicConfig(level=logging.DEBUG)


# url = 'https://mp.weixin.qq.com/s?__biz=MzAxOTc0NzExNg==&mid=2665514097&idx=1&sn=69f03561777ecd96026c48f05b79716a&chksm=80d67c32b7a1f524bba737832b0d59186ba186ba1ee19ad9704a306e11bba5e6492afc037ba9&scene=0&ascene=7&devicetype=android-25&version=26051036&nettype=WIFI&abtest_cookie=BAABAAgACgAMAA0ACgCehh4AT4geAGGIHgCBiB4AsIgeANWIHgD8iB4ADYkeAJeJHgCziR4AAAA%3D&pass_ticket=JH0%2BNXSvxN4jghAYtRdDsR6pwz20l5pDaCTQEr0Ekhu4IGT4wcUF9YXToqwAlBtd&wx_header=1'
url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzAxOTc0NzExNg==&scene=124&devicetype=android-25&version=26051036&lang=en&nettype=WIFI&a8scene=3&pass_ticket=%2F%2BD%2BSITlyVjpQ1FGtwsjiTWZoXBQYrCjNdyFcsyp7F0Yr2j%2FMRhr4hr0bqGv9W61&wx_header=1'
header = """Host: mp.weixin.qq.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Linux; Android 7.1.2; Pixel XL Build/NJH47F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 MicroMessenger/6.5.16.1120 NetType/WIFI Language/en
x-wechat-uin: MjQyMTM4MzM4MA%3D%3D
x-wechat-key: 63f29c76b0873f93fbbf5b7b562c8189a21a60580a2449d73366c179414dc7842cad63b8bb4dd17cc7adaa07c8be49ed183a963d450247fc8ef5e56f40bf6b28bee8d478311eeced6020d6aa1a9c18aa
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/sharpp,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: en,en-US;q=0.8
Cookie: wxticket=2239895926; wxticketkey=80257c45f273ba2ef85569706e89a8fdc08b6c6115b316267004103a78d29b88; sd_userid=57811504500511745; sd_cookie_crttime=1504500511745; pgv_pvi=1270763520; pgv_si=s4428417024; pgv_info=ssid=s2305215986; pgv_pvid=1698149402; rewardsn=8a038d21183ef5634c64; wxtokenkey=0455db455930de0eeb8285fc572037bfd731031945c71ae0f338cff5592598de; wxuin=2421383380; pass_ticket=/+D+SITlyVjpQ1FGtwsjiTWZoXBQYrCjNdyFcsyp7F0Yr2j/MRhr4hr0bqGv9W61; wap_sid2=CNTBzYIJEogBQ0VhQXNiZ3RKU2JaMURfMDVFbFdSb0EwbUUwbGxmMk5JSUZjRjdrSnU1Q3JrUFM1VUpaYTZiT0czbTQtZTJPbXlWZkJQbUVSWkNqenZ6aUtWdlczNi1XRmRrSHl5UTV6MV9PdjJhM1UtQUFrV0I0MndNcHp4cDFhb3Z5a2FSU3lwUU1BQUF+fjDb75TRBTgNQJVO
Q-UA2: QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.5.16&TBSVC=43601&CO=BK&COVC=043622&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= PixelXL &RL=1440*2392&OS=7.1.2&API=25
Q-GUID: 9e47146b1d2eafcf5002873e13b788cb
Q-Auth: 31045b957cf33acf31e40be2f3e71c5217597676a9729f1b"""






def to_dict(header):
    hs = header.split('\n')
    head_dict = {}
    for h in hs:
        key, value = h.split(':')
        head_dict[key] = value.strip()
    logging.debug(head_dict)
    return head_dict


def parse_html(html_content):
    # re.S：表示.匹配换行
    # compile vs match： pattern可以用多次
    # match vs search： match是从头开始匹配，search是匹配任意子字符串
    pattern = re.compile(r"msgList = '({.*?})'", flags=re.S)
    m = pattern.search(html_content)
    logging.debug(m)
    if m:
        msg = m.group(1)
        # No.	文字表記	10進表記	16進表記	文字	 	Comment
        # 001	&quot;	&#34;	&#x22;	"""	 	quotation mark = APL quote
        # 002	&amp;	&#38;	&#x26;	"&"	 	ampersand
        # 003	&lt;	&#60;	&#x3C;	"<"	 	less-than sign
        # 004	&gt;	&#62;	&#x3E;	">"	 	greater-than sign
        # 005	&nbsp;	&#160;	&#xA0;	" "	 	no-break space = non-breaking space
        msg = html.unescape(msg)  # 转义
        articles = json.loads(msg)['list']
        return articles


def download_task(name, url, head):
    print('Spider download %s, url %s, pid %s' % (name, url, os.getpid()))
    processed_url = html.unescape(url).replace('\\', '')
    dl_content = requests.get(processed_url, headers=head)
    dirname = os.getcwd() + '/wechat'
    # if os.path.exists(dirname)：
    #     os.makedirs(dirname)
    file_name = os.path.join(dirname, name + '.html')
    if dl_content.status_code == 200:
        print('download %s done' % name)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(dl_content.text)
    else:
        print('failed to download %s' % name)


if __name__ == '__main__':
    head_dict = to_dict(header)
    download = requests.get(url, headers=head_dict)
    logging.debug(download.status_code)
    with open('wechat_history.html', 'w', encoding='utf-8') as f:
        f.write(html.unescape(download.text))
    # with open('wechat_history.html', 'r') as f:
    #     data = f.read()
    articles = parse_html(download.text)
    p = Pool(10)
    for item in articles:
        logging.debug(item)
        app_msg = item['app_msg_ext_info']
        name = app_msg['title']
        cont_url = app_msg['content_url']
        p.apply_async(download_task, args=(name, cont_url, head_dict, ))
    print('Waiting for all processes done...')
    p.close()
    p.join()
    print('All subprocess done.')
