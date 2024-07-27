import requests
import random
import time
import logging

from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style

from config import info_url,detail_url,self_follower_url,other_follower_url,headers,cookies,sqlite_tb_name
from writer import create_table, insert_table


class ColorFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format(self, record):
        log = super().format(record)
        prefix = ''
        if record.levelno == logging.DEBUG:
            prefix = f"{Fore.CYAN}"
        elif record.levelno == logging.INFO:
            prefix = f"{Fore.GREEN}"
        elif record.levelno == logging.WARNING:
            prefix = f"{Fore.YELLOW}"
        elif record.levelno == logging.ERROR:
            prefix = f"{Fore.RED}"
        elif record.levelno == logging.CRITICAL:
            prefix = f"{Fore.RED} + {Style.BRIGHT}"
        return f"{prefix}{log}{Style.RESET_ALL}"

class JsonParser:
    def __init__(self, json_content:dict):
        self.json_content = json_content

    def check_key(self, keys:list):
        for key in keys:
            if self.json_content.get(key) != None:
                continue
            else:
                print(f"{self.json_content} no key:{key}")

    def get(self, key):
        ret = self.json_content.get(key, None)
        return ret

    def collect(self, keys):
        ret = []
        for item in keys:
            ret.append(self.get(item))
        return ret

class User:
    def __init__(self, user_id, user_name, profile_image_url, followers_cnt,follow_cnt):
        self.user_id = user_id
        self.user_name = user_name
        self.profile_image_url = profile_image_url
        self.followers_cnt = followers_cnt
        self.follow_cnt = follow_cnt
        self.followers = []

    def set_weibo(self, weibos:list):
        self.weibos = weibos

    def write_to_db(self):
        for user in self.followers:
            insert_table(sqlite_tb_name, self.user_id, user.user_id, user.user_name, user.profile_image_url)


class Weibo:
    def __init__(self, id, create_time, text, image_urls:list):
        self.create_time = create_time
        self.text = text
        self.image_urls = image_urls
        self.fetch_comments()

    def fetch_comments(self):
        pass


class Spider:
    def __init__(self, user_id, max_search_depth=1):
        logging.basicConfig(level=logging.INFO,
                            filename='log.log',
                            filemode='w',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.user_id = user_id
        self.info_url = info_url.format(id=user_id)
        self.user = User(user_id, '', '', 0, 0)
        self.config_logger()
        self.visit_cnt = 0

    def config_logger(self):
        # 创建一个logger对象
        logger = logging.getLogger('spider')
        logger.setLevel(logging.DEBUG)  # 设置日志级别
        # 创建一个文件处理器，并设置级别为DEBUG
        file_handler = logging.FileHandler('spider.log')
        file_handler.setLevel(logging.DEBUG)
        # 创建一个控制台处理器，并设置级别为ERROR
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        # 创建并设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        terminal_formatter = ColorFormatter(fmt=formatter._style._fmt, datefmt=formatter.datefmt)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(terminal_formatter)
        # 将文件处理器和控制台处理器添加到logger中
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        self.logger = logger

    def run(self):
        create_table(sqlite_tb_name)
        self.logger.info(f'start to crawl user {self.user_id}')
        self.user = self.get_user(self.user_id)
        self.logger.info(f'get followers {self.user.user_name}')
        fans = self.get_self_follower(self.user_id)
        self.user.followers = fans
        # 将粉丝信息写入数据库
        self.logger.debug(f'write fans info to sqlite db, id:{self.user_id}')
        self.user.write_to_db()
        for user in fans:
            followers = self.get_other_follower(user.user_id)
            user.followers = followers
            user.write_to_db()
            for follower in followers:
                self.logger.debug(f'write fans info to sqlite db, id:{follower.user_id}')
        #self.user.set_weibo(weibos)
        # followers = self.get_other_follower(self.user_id)
        # for item in followers:
        #     print(item.user_id, item.user_name)
        # print(len(followers))
        # for item in self.user.weibos:
        #     print(item.create_time, item.text)
        # print(f'total {len(self.user.weibos)} weibos')

    def get_user(self, user_id):
        self.visit_cnt += 1
        user = None
        url = info_url.format(id=user_id)
        if self.visit_cnt % 40 == 0:
            wait_tm = random.randint(1, 5)
            time.sleep(wait_tm)
        try:
             resp = requests.get(url,
                                 headers=headers,
                                 cookies=cookies)
             parser = JsonParser(resp.json())
             keys = ['ok', 'data']
             parser.check_key(keys)
             if not parser.get('ok'):
                 return user
             parser = JsonParser(parser.get('data'))
             keys = ['user', "tabList"]
             parser.check_key(keys)
             parser = JsonParser(parser.get('user'))
             keys = ['screen_name', "profile_image_url", "followers_count", "friends_count"]
             parser.check_key(keys)
             user_name = parser.get('screen_name')
             profile_image = parser.get('profile_image_url')
             follower_cnt = parser.get('followers_count')
             follow_cnt = parser.get('friends_count')
             user = User(user_id, user_name, profile_image, follower_cnt, follow_cnt)
             self.logger.debug(f'user_id:{user_id}, user name: {user_name}')
        except Exception as e:
            print(e)
            raise
        return user

    def batch_get_user(self, user_ids):
        users = []
        with ThreadPoolExecutor(max_workers=1) as executor:  # 可以调整工作线程数量
            future_to_url = {executor.submit(self.get_user, id): id for id in user_ids}
            # 遍历future对象，当完成时获取结果
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    user = future.result()
                    users.append(user)
                except Exception as exc:
                    print(f"URL: {url} generated an exception: {exc}")
        return users

    def get_weibo(self, user:User):
        page_cnt = 1
        weibos = []
        while True:
            url = detail_url.format(id=user.user_id, page_id=page_cnt)
            resp = requests.get(url,headers=headers,cookies=cookies)
            parser = JsonParser(resp.json())
            keys = ['data', 'ok']
            parser.check_key(keys)
            parser = JsonParser(parser.get('data'))
            keys = ['list']
            parser.check_key(keys)
            if not parser.get('list'):
                break
            items = parser.get('list')
            for item in items:
                parser = JsonParser(item)
                keys = ['created_at', 'text', 'id', 'pic_num']
                parser.check_key(keys)
                tm = parser.get("created_at")
                text = parser.get("text")
                id = parser.get('id')
                image_urls = []
                weibo = Weibo(id, tm, text, image_urls)
                weibos.append(weibo)
            page_cnt += 1
            if page_cnt % 10 == 0:
                wait_tm = random.randint(1, 5)
                time.sleep(wait_tm)
        return weibos

    def get_self_follower(self, user_id):
        self.logger.info(f'start to get {user_id} self followers')
        url = self_follower_url.format(id=user_id)
        fans = []
        try:
            resp = requests.get(url, headers=headers, cookies=cookies)
            resp_json = resp.json()
            parser = JsonParser(resp_json)
            parser.check_key(['users', 'new_follows'])
            old_parser = deepcopy(parser)
            parser = parser.get('users')
            ids = []
            for item in parser:
                parser = JsonParser(item)
                keys = ['id']
                parser.check_key(keys)
                ids.append(parser.get('id'))
            parser = JsonParser(old_parser.get('new_follows'))
            parser.check_key(['list'])
            parser = parser.get('list')
            for item in parser:
                parser = JsonParser(item)
                keys = ['id']
                parser.check_key(keys)
                ids.append(parser.get('id'))
            ids = list(set(ids))
            fans = [ self.get_user(id) for id in ids]
            for item in fans:
                self.logger.info(f'get follower id: {item.user_id}, username:{item.user_name}')
            self.logger.info(f'total {len(ids)} followers')
        except Exception as e:
            print(e)
        return fans

    def get_other_follower(self, user_id, max_depth=1):
        user = self.get_user(user_id)
        self.logger.debug(f'user_id:{user_id}, user url: {info_url.format(id=user_id)}, user name: {user.user_name}')
        self.logger.info(f'start to get {user_id} followers')
        page_cnt = 1
        url = other_follower_url.format(page_cnt=page_cnt, id=user_id)
        ids = []
        try:
            while True:
                resp = requests.get(url, headers=headers, cookies=cookies)
                resp_json = resp.json()
                parser = JsonParser(resp_json)
                parser.check_key(['users', 'display_total_number'])
                total_cnt = parser.get('display_total_number')
                items = parser.get('users')
                for item in items:
                    parser = JsonParser(item)
                    keys = ['id']
                    parser.check_key(keys)
                    id = parser.get('id')
                    ids.append(id)
                if len(ids) >= total_cnt or not items:
                    break
                else:
                    page_cnt += 1
                    url = other_follower_url.format(page_cnt=page_cnt, id=user_id)
                if page_cnt % 20 == 0:
                    wait_tm = random.randint(1, 5)
                    time.sleep(wait_tm)
                print(f'\rtotal {total_cnt} followers, current {len(ids)}', end='')
        except Exception as e:
            print(e)
        fans = self.batch_get_user(ids)
        fans = [item for item in fans if item is not None]
        for user in fans:
            self.logger.info(f'get follower id: {user.user_id}, username:{user.user_name}')
        return fans

if __name__ == '__main__':
    spider = Spider(6126303533)
    spider.run()

