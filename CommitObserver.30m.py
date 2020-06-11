#!/usr/bin/env LC_ALL=en_US.UTF-8 /usr/local/bin/python3

# <bitbar.title>CommitObserver</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Fitware Jay</bitbar.author>
# <bitbar.author.github>JAY-Chan9yu</bitbar.author.github>
# <bitbar.image></bitbar.image>
# <bitbar.desc>If you want to monitor whether your teammates are committing or not, try this plugin.(joke)</bitbar.desc>
# <bitbar.dependencies>python3</bitbar.dependencies>

import requests
import os
from bs4 import BeautifulSoup
import yaml

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

    source = requests.get("https://github.com/{}".format(user.get('id'))).text
    soup = BeautifulSoup(source, "html.parser")
    if soup.select('rect'):
        user_commit = soup.select('rect')[-1].get('data-count')

        if int(user_commit) == 0:
            print("{} {} : {}".format(emoji, user.get('name'), BAD))
        else:
            print("{} {} : {}".format(emoji, user.get('name'), GOOD))
