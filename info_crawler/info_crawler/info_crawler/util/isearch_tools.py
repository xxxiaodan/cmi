# -*- coding: UTF-8 -*-

import re
import datetime
import time
import logging
from HTMLParser import HTMLParser


class ISearchTools(object):
    '''
    工具类
    '''
    # bettrRegexs=[r"\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}",
    #         r"\d{4}年\d{1,2}月\d{1,2}日\d{1,2}:\d{1,2}",
    #         r"\d{4}年\d{1,2}月\d{1,2}日\s+\d{1,2}:\d{1,2}",
    #         r"\d{4}/\d{1,2}/\d{1,2}\s+\d{1,2}:\d{1,2}"]
    regexs = [r"\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}",
                r"\d{4}年\d{1,2}月\d{1,2}日\d{1,2}:\d{1,2}",
                r"\d{4}年\d{1,2}月\d{1,2}日\s+\d{1,2}:\d{1,2}",
                r"\d{4}/\d{1,2}/\d{1,2}\s+\d{1,2}:\d{1,2}",
                r"\d{4}年\d{1,2}月\d{1,2}日",
                r"\d{4}-\d{1,2}-\d{1,2}",
                r"\d{4}/\d{1,2}/\d{1,2}"]
    dateFormats = {regexs[0]: '%Y-%m-%d %H:%M',
                        regexs[1]: '%Y年%m月%d日%H:%M',
                        regexs[2]: '%Y年%m月%d日 %H:%M',
                        regexs[3]: '%Y/%m/%d %H:%M',
                        regexs[4]: '%Y年%m月%d日',
                        regexs[5]: '%Y-%m-%d',
                        regexs[6]: '%Y/%m/%d'}
    dateRegexObj={regexs[0]:re.compile(regexs[0]),
            regexs[1]:re.compile(regexs[1]),
            regexs[2]:re.compile(regexs[2]),
            regexs[3]:re.compile(regexs[3]),
            regexs[4]:re.compile(regexs[4]),
            regexs[5]:re.compile(regexs[5]),
            regexs[6]:re.compile(regexs[6])}
    extraObj0=re.compile(r'发表(于|在)\s*(\d+)\s*秒钟?前',re.LOCALE)
    extraObj1=re.compile(r'发表(于|在)\s*(\d+)\s*分钟前',re.LOCALE)
    extraObj2=re.compile(r'发表(于|在)\s*半分钟前',re.LOCALE)
    extraObj3=re.compile(r'发表(于|在)\s*(\d+)\s*小时前',re.LOCALE)
    extraObj4=re.compile(r'发表(于|在)\s*半小时前',re.LOCALE)
    extraObj5=re.compile(r'发表(于|在)\s*昨天\s*(\d{1,2}):(\d{1,2})',re.UNICODE)
    extraObj6=re.compile(r'发表(于|在)\s*前天\s*(\d{1,2}):(\d{1,2})',re.LOCALE)
    extraObj7=re.compile(r'发表(于|在)\s*(\d+)\s*天前',re.LOCALE)
    extraObj8=re.compile(r'发表(于|在)\s*半天前',re.LOCALE)
    extraObj9=re.compile(r'\d{1,2}:\d{1,2}',re.LOCALE)

    # 特殊字符串识别
    intReg = re.compile(r'\d+')
    floatReg = re.compile(r'\d+(\.\d+)?')

    @staticmethod
    def extractDateTimeFromStr(timeStr):
        '''
        从一个字符串中解析出时间对象，返回标准时间格式（'%Y-%m-%d %H:%M:%S'）的字符串
        '''
        #预处理
        timeStr=timeStr.decode('UTF-8')
        timeStr=timeStr.replace(u'\xa0', u' ')
        timeStr=timeStr.encode('UTF-8')
        #先采用默认格式解析
        result=None
        for regex in ISearchTools.regexs:
            reObj=(ISearchTools.dateRegexObj)[regex]
            rs=reObj.search(timeStr)
            if rs!=None:
                result=datetime.datetime.strptime(rs.group(0),(ISearchTools.dateFormats)[regex])
                try:
                    #格式转换
                    result=result.strftime('%Y-%m-%d %H:%M:%S')
                except Exception:
                    result=None
                    logging.log(logging.ERROR,"format time error:"+str(result)+' for str:'+rs.group(0)+' source:'+timeStr)
                break
        else:
            logging.log(logging.INFO,"specail timeStr:"+timeStr)
            flag=False
            rs=ISearchTools.extraObj0.search(timeStr)
            if rs!=None:
                now=datetime.datetime.now()
                realTime=now-datetime.timedelta(seconds=int(rs.group(1)))
                result=realTime.strftime('%Y-%m-%d %H:%M:%S')
                flag=True
            if not flag:
                #temp=re.compile(r'发表(于|在){1}\s*(\d+)\s*分钟前')
                rs=ISearchTools.extraObj1.search(timeStr)
                if rs!=None:
                    now=datetime.datetime.now()
                    realTime=now-datetime.timedelta(minutes=int(rs.group(2)))
                    result=realTime.strftime('%Y-%m-%d %H:%M:%S')
                    flag=True
            if not flag:
                rs=ISearchTools.extraObj2.search(timeStr)
                if rs!=None:
                    now=datetime.datetime.now()
                    realTime=now-datetime.timedelta(seconds=30)
                    result=realTime.strftime('%Y-%m-%d %H:%M:%S')
                    flag=True
            if not flag:
                rs=ISearchTools.extraObj3.search(timeStr)
                if rs!=None:
                    now=datetime.datetime.now()
                    realTime=now-datetime.timedelta(hours=int(rs.group(2)))
                    result=realTime.strftime('%Y-%m-%d %H:%M:%S')
                    flag=True
            if not flag:
                rs=ISearchTools.extraObj4.search(timeStr)
                if rs!=None:
                    now=datetime.datetime.now()
                    realTime=now-datetime.timedelta(minutes=30)
                    result=realTime.strftime('%Y-%m-%d %H:%M:%S')
                    flag=True
            if not flag:
                rs=ISearchTools.extraObj5.search(timeStr)
                if rs!=None:
                    now=datetime.datetime.now()
                    realTime=now-datetime.timedelta(days=1)
                    realTime=realTime.replace(hour=int(rs.group(2)),minute=int(rs.group(3)),second=0)
                    result=realTime.strftime('%Y-%m-%d %H:%M:%S')
                    flag=True
            if not flag:
                rs=ISearchTools.extraObj6.search(timeStr)
                if rs!=None:
                    now=datetime.datetime.now()
                    realTime=now-datetime.timedelta(days=2)
                    realTime=realTime.replace(hour=int(rs.group(2)),minute=int(rs.group(3)),second=0)
                    result=realTime.strftime('%Y-%m-%d %H:%M:%S')
                    flag=True
            if not flag:
                rs=ISearchTools.extraObj7.search(timeStr)
                if rs!=None:
                    now=datetime.datetime.now()
                    realTime=now-datetime.timedelta(days=int(rs.group(2)))
                    result=realTime.strftime('%Y-%m-%d %H:%M:%S')
                    flag=True
            if not flag:
                rs=ISearchTools.extraObj8.search(timeStr)
                if rs!=None:
                    now=datetime.datetime.now()
                    realTime=now-datetime.timedelta(hours=12)
                    result=realTime.strftime('%Y-%m-%d %H:%M:%S')
                    flag=True
            if not flag:
                rs=ISearchTools.extraObj9.search(timeStr)
                if rs!=None:
                    now=time.strftime("%Y-%m-%d", time.localtime())
                    strTime=now+' '+rs.group(0)
                    result=datetime.datetime.strptime(strTime,'%Y-%m-%d %H:%M')
                    flag=True
            # 暂时不做其他处理
            if not flag:
                logging.log(logging.ERROR,'unknown time str'+timeStr)
        return result

    @staticmethod
    def extractHtmlText(body):
        '''粗略提取网页正文,采用基于文本密度的方法'''
        content = ISearchTools.remove_empty_line(ISearchTools.remove_js_css(body))
        left,right,x,y = ISearchTools.method_1 (content)
        result='\n'.join(content.split('\n')[left:right])  
        result=ISearchTools.remove_any_tag(result)
        r = re.compile(r'\s+', re.M|re.S)  
        result = r.sub (' ', result)
        return result 
    
    @staticmethod
    def remove_js_css(content):
        """ remove the the javascript and the stylesheet and the comment content (<script>....</script> and <style>....</style> <!-- xxx -->) """  
        r = re.compile(r'<script.*?</script>',re.I|re.M|re.S)  
        s = r.sub ('',content)  
        r = re.compile(r'<style.*?</style>',re.I|re.M|re.S)  
        s = r.sub ('', s)  
        r = re.compile(r'<!--.*?-->', re.I|re.M|re.S)  
        s = r.sub('',s)  
        r = re.compile(r'<meta.*?>', re.I|re.M|re.S)  
        s = r.sub('',s)  
        r = re.compile(r'<ins.*?</ins>', re.I|re.M|re.S)  
        s = r.sub('',s)  
        return s  
    
    @staticmethod
    def remove_empty_line(content):
        """remove multi space """  
        r = re.compile(r'^\s+&', re.M|re.S)  
        s = r.sub('', content)
        r = re.compile(r'\n+',re.M|re.S)  
        s = r.sub('\n',s)  
        return s  
    
    @staticmethod
    def remove_any_tag(s):
        s = re.sub(r'<[^>]+>', '', s)
        return s.strip()  
    
    @staticmethod
    def remove_any_tag_but_a(s):
        text = re.findall(r'<a[^r][^>]*>(.*?)</a>',s,re.I|re.S|re.S)
        text_b = ISearchTools.remove_any_tag(s)
        return len(''.join(text)), len(text_b)
    
    @staticmethod
    def remove_image(s, n=50):
        image = 'a' * n  
        r = re.compile(r'<img.*?>', re.I|re.M|re.S)
        s = r.sub(image, s)
        return s  
    
    @staticmethod
    def remove_video(s, n=1000):
        video = 'a' * n  
        r = re.compile(r'<embed.*?>',re.I|re.M|re.S)
        s = r.sub(video, s)
        return s  
    
    @staticmethod
    def sum_max(values):
        cur_max = values[0]  
        glo_max = -999999  
        left, right = 0, 0
        for index, value in enumerate(values):
            cur_max += value  
            if cur_max > glo_max:
                glo_max = cur_max  
                right = index  
            elif cur_max < 0:
                cur_max = 0  
      
        for i in range(right, -1, -1):  
            glo_max -= values[i]  
            if abs(glo_max < 0.00001):  
                left = i  
                break  
        return left, right+1
    
    @staticmethod
    def method_1(content, k=1):
        if not content:  
            return None, None, None, None
        tmp = content.split('\n')  
        group_value = []  
        for i in range(0,len(tmp), k):
            group = '\n'.join(tmp[i:i+k])  
            group = ISearchTools.remove_image(group)
            group = ISearchTools.remove_video(group)
            text_a, text_b = ISearchTools.remove_any_tag_but_a(group)
            temp = (text_b - text_a) - 8   
            group_value.append(temp)
        left, right = ISearchTools.sum_max (group_value)
        return left, right, len('\n'.join(tmp[:left])), len('\n'.join(tmp[:right]))
    # 去除文本中的标签

    @staticmethod
    def strip_tags(html):
        result = []
        parse = HTMLParser()
        parse.handle_data = result.append
        parse.feed(html)
        parse.close()
        return "".join(result)


if __name__ == '__main__':
    test='<td align="center" class="jianjie"> 【 <a href="http://www.newssc.org">http://www.newssc.org </a>】 【 2015-12-11 15:43 】 【来源：四川新闻网教育频道 】 </td>'
    '''print(repr(test))
    test=unicode(test.decode('UTF-8'))
    test=test.replace(u'\xa0', u' ')
    print(repr(test))
    temp=re.sub(r'\s+', '', test,re.UNICODE)
    print(temp)'''
    result = ISearchTools.extractDateTimeFromStr(test)
    print(ISearchTools.strip_tags(''))
    print(result)