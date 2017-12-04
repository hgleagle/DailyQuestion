"""
使用filder提取微信公众号消息
"""
import requests
import logging
import re
import html
import json


logging.basicConfig(level=logging.DEBUG)


# url = 'https://mp.weixin.qq.com/s?__biz=MzAxOTc0NzExNg==&mid=2665514097&idx=1&sn=69f03561777ecd96026c48f05b79716a&chksm=80d67c32b7a1f524bba737832b0d59186ba186ba1ee19ad9704a306e11bba5e6492afc037ba9&scene=0&ascene=7&devicetype=android-25&version=26051036&nettype=WIFI&abtest_cookie=BAABAAgACgAMAA0ACgCehh4AT4geAGGIHgCBiB4AsIgeANWIHgD8iB4ADYkeAJeJHgCziR4AAAA%3D&pass_ticket=JH0%2BNXSvxN4jghAYtRdDsR6pwz20l5pDaCTQEr0Ekhu4IGT4wcUF9YXToqwAlBtd&wx_header=1'
url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzAxOTc0NzExNg==&scene=124&devicetype=android-25&version=26051036&lang=en&nettype=WIFI&a8scene=3&pass_ticket=jvhdslP2naY0SvlcMx5Ug3f1wVJaQ0wwy5Vgwp06q4qCPiIDBNlUw%2Bo4T2tODPiY&wx_header=1'
header = """Host: mp.weixin.qq.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Linux; Android 7.1.2; Pixel XL Build/NJH47F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 MicroMessenger/6.5.16.1120 NetType/WIFI Language/en
x-wechat-uin: MjQyMTM4MzM4MA%3D%3D
x-wechat-key: b7c2b41476280334cc64cc2ecb771273e488852896647ea59dd7e709485b80b707604d5428b8cd55e5a27664150e4827a6bfe8d6f9787aa722c6990cc5b5e25d83d094836704b353c54602a39db5dc27
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/sharpp,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: en,en-US;q=0.8
Cookie: wxticket=2239895926; wxticketkey=80257c45f273ba2ef85569706e89a8fdc08b6c6115b316267004103a78d29b88; sd_userid=57811504500511745; sd_cookie_crttime=1504500511745; pgv_pvi=1270763520; pgv_si=s4428417024; pgv_info=ssid=s2305215986; pgv_pvid=1698149402; wxtokenkey=1e0745b4aeea67e113aa328daf5120ef5a8157f3972445cbcf2d6d3cf18c7525; wxuin=2421383380; pass_ticket=JH0+NXSvxN4jghAYtRdDsR6pwz20l5pDaCTQEr0Ekhu4IGT4wcUF9YXToqwAlBtd; wap_sid2=CNTBzYIJEnBDRWFBc2JndEpTYloxRF8wNUVsV1JqcUo2cFVONjZzWTVvNlhnNVl1UUNScDJIdzN2QmlVX2RWN1htYWhLZnlHNTJDNnNXcmNBLVVDWkFaNF9uU1ZVSENJbU9oVjR0LTVUS3FXOVladHIwbWxBd0FBMLnGk9EFOA1AAQ==; rewardsn=d5d32f505d962fb736de
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
        logging.debug(articles)
        return articles



if __name__ == '__main__':
    head_dict = to_dict(header)
    download = requests.get(url, headers=head_dict)
    logging.debug(download.status_code)
    with open('wechat_history.html', 'w', encoding='utf-8') as f:
        f.write(html.unescape(download.text))
    # with open('wechat_history.html', 'r') as f:
    #     data = f.read()
    parse_html(download.text)