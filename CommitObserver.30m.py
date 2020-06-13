#!/usr/bin/env LC_ALL=en_US.UTF-8 /usr/local/bin/python3

# <bitbar.title>CommitObserver</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Fitware Jay</bitbar.author>
# <bitbar.author.github>JAY-Chan9yu</bitbar.author.github>
# <bitbar.image></bitbar.image>
# <bitbar.desc>If you want to monitor whether your teammates are committing or not, try this plugin.(joke)</bitbar.desc>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/JAY-Chan9yu/BitBar-CommitObserver</bitbar.abouturl>

import datetime
import os

import requests
import yaml
from bs4 import BeautifulSoup

GOOD = "💚"
BAD = "🚨"
EMOJI_LIST = ['🐶', '🐱', '🐭', '🐹', '🐻', '🐰', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐸', '🐵']
DIR_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'commit_observer',
    'github_user_list.yml'
)

print("😈 COMMIT OBSERVER")
with open(DIR_PATH, 'r', encoding='utf-8') as f:
    user_yaml = yaml.load(f, Loader=yaml.FullLoader)
    temp_emoji_list = EMOJI_LIST
    user_dict = user_yaml.get('githubID')

for user in user_dict:
    try:
        emoji = temp_emoji_list.pop()
    except IndexError:
        temp_emoji_list = EMOJI_LIST
        emoji = temp_emoji_list.pop()

    # If you don't use {to} in the url parameter, you can't see today's commit for local time due to utc time
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    source = requests.get('https://github.com/{}?to={}'.format(
        user.get('id'),
        today
    )).text
    soup = BeautifulSoup(source, "html.parser")

    if soup.select('rect'):
        user_commit = soup.find(
            "rect",
            attrs={"data-date": today}
        ).get('data-count')

        if int(user_commit) == 0:
            print("{} {} : {}".format(emoji, user.get('name'), BAD))
        else:
            print("{} {} : {}".format(emoji, user.get('name'), GOOD))
