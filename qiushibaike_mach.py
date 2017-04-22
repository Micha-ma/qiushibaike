import requests
from bs4 import BeautifulSoup
import os

#这是糗事百科热门的一个爬虫模块程序，有多个接口
class QSBK(object):
    def __init__(self, init_url):
        self.init_url = init_url

    def get_Page(self, url=None):
        #这是获取热门中某一帖子下神评论的网页源码
        if url:
            compage = requests.get(url).content.decode('utf-8')
            com_soup = BeautifulSoup(compage, 'lxml')
            comdetail = com_soup.find_all('div', class_='comments-table')
            #print(comdetail)
            return comdetail
        #这是获取热门帖子页面的网页源码
        else:
            mainpage = requests.get(self.init_url).content.decode('utf-8')
            soup = BeautifulSoup(mainpage, 'lxml')
            postpage = soup.find_all('div', class_='article')
            #print(postpage)
            return postpage

    #这是获取作者昵称和年龄
    def get_Author(self, eachpost):
        author = eachpost.find('div', class_='author clearfix')
        author_name = author.h2.get_text()
        #有些网友的个人资料没有年龄，故需要判断年龄标签是否存在，否则会报NoneType的错误
        if author.find('div', class_='articleGender manIcon') != None:
            author_age = author.find('div', class_='articleGender manIcon').string
        else:
            author_age = '他很懒，没留下年龄'
        author_info = {
            'name': author_name,
            'age': author_age
        }
        #print(author_info)
        return author_info

    #这是获取帖子内容的函数
    def get_Content(self, eachpost):
        post_content = eachpost.find('div', class_='content').get_text().strip()
        #print(post_content)
        return post_content

    #这是获取帖子状态的函数，包括好笑和评论的次数，这里同样需要判断是否有好笑及评论，否则也会报错NoneType
    def get_Stat(self, eachpost):
        stat_vote = eachpost.find('span', class_='stats-vote')
        if stat_vote != None:
            vote = stat_vote.i.string
        else:
            vote = '(′д｀ )…彡…彡没人觉得好笑'
        stat_comment = eachpost.find('span', class_='stats-comments')
        if stat_comment != None:
            comment = stat_comment.i.string
        else:
            comment = '没有人发表高见~~~'
        stat = {
            '好笑': vote,
            '评论': comment
        }
        #print(stat)
        return stat

    #这个函数是获取某一帖子下的神评论的情况
    def get_ComDetail(self, eachpost):
        comdetailhref = eachpost.find('a', class_='indexGodCmt').get('href')
        comdetailurl = self.init_url + comdetailhref
        com_page = self.get_Page(comdetailurl)
        comments = []
        for i in range(0, len(com_page)):
            com_author = com_page[i].find('div', class_='cmt-name').string.split('\n')[1]
            com_content = com_page[i].find('div', class_='main-text').string
            data = {
                '吐槽作者': com_author,
                '吐槽内容': com_content
            }
            comments.append(data)
        print(comments)
        return comments


#这个函数是获取一个帖子的相关信息的汇总，包括作者昵称、年龄，帖子内容，好笑及评论数
    def get_OnePost(self, n=0):
        postpage = self.get_Page()
        postitem = postpage[n]
        data = {
            '内容': self.get_Content(postitem),
            '作者': self.get_Author(postitem)['name'],
            '年龄': self.get_Author(postitem)['age'],
            '好笑': self.get_Stat(postitem)['好笑'],
            '评论': self.get_Stat(postitem)['评论']
        }
        print(data)
        return data


#这个函数是获取所有该页热门帖子的相关信息，其实就是循环get_OnePost函数
    def get_AllPost(self):
        num = len(self.get_Page())
        all_data = []
        for i in range(0, num):
            all_data.append(self.get_OnePost(i))
        print(all_data)
        return all_data

#这个函数主要是将获取的帖子相关信息保存到本地
    def saveInFile(self, l=-1):
        #这里先判断是否存在路径save_path,没有就创建
        save_path = 'G:\\糗事百科\\spider模块\\'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        if l != -1:
            postdata = self.get_OnePost(l)
            with open(save_path + 'page' + str(l) + '.txt', 'a', encoding='utf-8') as f:
                f.write(postdata['内容'] + '\n')
                f.write('作者：' + postdata['作者'] + '\t' + '年龄：' + postdata['年龄'] + '\n')
                f.write('好笑：' + postdata['好笑'] + '\t' + '评论：' + postdata['评论'] + '\n')
                f.write('\n---------------------------------------------------------------\n\n')
            print('You have save one post in the file!')
        else:
            postdata = self.get_AllPost()
            with open(save_path + 'mainpage' + '.txt', 'a', encoding='utf-8') as f:
                for x in range(0, len(postdata)):
                    f.write('帖' + str(x) + ':\n')
                    f.write(postdata[x]['内容'] + '\n')
                    f.write('作者：' + postdata[x]['作者'] + '\t' + '年龄：' + postdata[x]['年龄'] + '\n')
                    f.write('好笑：' + postdata[x]['好笑'] + '\t' + '评论：' + postdata[x]['评论'] + '\n')
                    f.write('\n---------------------------------------------------------------\n\n')
            print('You have save all post in the file!')

if __name__ == '__main__':
    url = 'http://www.qiushibaike.com'
    qsbk = QSBK(url)
    postpage = qsbk.get_Page()
    #对自定义函数的测试
    #author = qsbk.get_Author(postpage[1])
    #content = qsbk.get_Content(postpage[0])
    #stat = qsbk.get_Stat(postpage[0])
    #com_url = qsbk.get_ComDetail(postpage[0])
    #comments = qsbk.get_ComDetail(postpage[0])
    #qsbk.get_AllPost()
    #qsbk.saveInFile()
    qsbk.saveInFile(1)
    qsbk.get_ComDetail(postpage[2])

