headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Mweibo-Pwa":"1",
    "Accept-Encoding":"gzip, deflate, br",
    "X-Requested-With":"XMLHttpRequest",
    "X-Xsrf-Token":"c79ebc",
    "Sec-Ch-Ua":'"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    "Sec-Ch-Ua-Mobile":"?1",
    "Sec-Ch-Ua-Platform":"Android",
    "Sec-Fetch-Dest":"empty",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Site":"same-origin",
    "X-Xsrf-Token":"c79ebc"
}
cookies = {
        "SINAGLOBAL":"1022129298118.4526.1609328884299",
        "XSRF-TOKEN":"Ggb1df340jsFfNAYyenu3v-d",
        "SCF":"AsGZKnOc_PM72DhV9RE3RFWOWOqf_Q0vA7A_QCS6Jwd6wXepX3LVIROV8pYJ1gC42nsePaPHJFq0vcnGv5ENXuo.",
        "SUB":"_2A25LjKpIDeRhGeBP6VQS8C3JyD-IHXVo46OArDV8PUJbkNANLVHYkW1NRWejPUxGvEq4Nxh0zxNpOtQ6ovrxPq4h",
        "SUBP":"0033WrSXqPxfM725Ws9jqgMF55529P9D9W5v1ED0B0LiqpSlMv3MxhXd5JpX5KzhUgL.Foqpeoq0ehefe0e2dJLoI7UrUgUf9NHo",
        "ALF":"1722836760",
        "WBPSESS":"SdNjAm69kt0J8TnnXl_t4xDcivTgPvH2uTkJlMoky5k3mpNXmE_AWkmOb5nIVKc0Bt0JjHZ1seEA5pW8kaKkV3NnxcxfZM3-qqF3wdztdBDeEbSg4aj3bGVG3s_uXIkR2Lb9k5jgpo11lx2bqgXZjA=="
}
proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

info_url = "https://weibo.com/ajax/profile/info?uid={id}"
detail_url = "https://weibo.com/ajax/statuses/mymblog?uid={id}&page={page_id}&"
image_url = "https://wx2.sinaimg.cn/orj360/{id}.jpg"
self_follower_url = "https://weibo.com/ajax/friendships/friends?uid={id}&relate=fans&count=20&fansSortType=fansCount"
other_follower_url = "https://weibo.com/ajax/friendships/friends?relate=fans&page={page_cnt}&uid={id}&type=all&newFollowerCount=0"
fans_url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{id}"
sqlite_tb_name = 'weibo_user'
