import requests


def push_serverchain(title, content, key):
    post_data = {
        'text': title,
        'desp': content
    }
    url = 'https://sc.ftqq.com/' + key + '.send'

    response = requests.post(url=url, data=post_data)
    return str(response.content, encoding="utf-8")
