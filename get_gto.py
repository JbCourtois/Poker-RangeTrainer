from collections import defaultdict
from pprint import pprint
from lxml import etree as ElementTree
import requests
import json


POSITIONS = ['UTG', 'UTG+1', 'LJ', 'HJ', 'CO', 'BTN', 'SB', 'BB']
ACTIONS = ['RFI', 'VS RAISE', 'VS 3BET', 'VS 4BET', 'VS 5BET ALLIN']


def parse_response(response):
    rrr = response.json()
    if not rrr['chart_available']:
        return

    jjj = rrr.pop('chart_html')

    jjj = f'<root>{jjj}</root>'
    eee = ElementTree.fromstring(jjj)
    hands = eee.xpath('.//div[@class="row_card"]')

    HAND_MAP = {}
    for card_row in hands:
        if len(card_row) <= 1:
            continue

        hand, actions = card_row
        hand = hand.text.strip()

        HAND_MAP[hand] = [action.text for action in actions]

    return HAND_MAP


def query(position, action='RFI', opp=''):
    url = "https://pokercoaching.com/wp-admin/admin-ajax.php"

    payload = {
        'action': 'preflop_chart_handler',
        'db': 'crawler',
        'rules': 'true',
        'filter[type]': 'cash_9max',
        'filter[blinds]': '100',
        'filter[position]': position,
        'filter[action]': action,
        'filter[opposition]': opp,
    }
    headers = {
        'authority': 'pokercoaching.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://pokercoaching.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://pokercoaching.com/cashpreflopcharts/',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'wordpress_sec_pocket_seises=jb.co.poker%7C1647547236%7CpdVRLnGp7rf7fP9qbWPaQHpRtrPKtIMYBHQMtN1Btiz%7C47637145ee6f0413c3f8191065d67bb7e1ad81be1d8de72a7bb77d35587ff735; _gcl_au=1.1.1675674071.1612275519; _ga=GA1.2.563094391.1612275519; wpf_ref[original_ref]=https%3A%2F%2Fwww.google.com%2F; wpf_ref[landing_page]=%2F; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2021-03-17%2019%3A56%3A08%7C%7C%7Cep%3Dhttps%3A%2F%2Fpokercoaching.com%2Flogin%2Fref%2F%5Bref%5D%2F%3Flp%3Dfrom_home%7C%7C%7Crf%3Dhttps%3A%2F%2Fpages.pokercoaching.com%2F; sbjs_first_add=fd%3D2021-03-17%2019%3A56%3A08%7C%7C%7Cep%3Dhttps%3A%2F%2Fpokercoaching.com%2Flogin%2Fref%2F%5Bref%5D%2F%3Flp%3Dfrom_home%7C%7C%7Crf%3Dhttps%3A%2F%2Fpages.pokercoaching.com%2F; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cmtke%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cmtke%3D%28none%29; ajs_anonymous_id=%223fc3de60-a6fc-4e44-9a4f-905c9f79216f%22; amplitude_idundefinedpokercoaching.com=eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==; wordpress_logged_in_pocket_seises=jb.co.poker%7C1647547236%7CpdVRLnGp7rf7fP9qbWPaQHpRtrPKtIMYBHQMtN1Btiz%7Cbc4f34ac69ee4c8810e3cd715ae60c78e6aa73eb467f409ae66e56cbd0b534e1; ajs_user_id=%22180204%22; browser_id=c9e706f4-deab-4532-a96c-d960d7c1e7a6; _gid=GA1.2.886698381.1618175307; mc_landing_site=https://pokercoaching.com/courses/master-the-fundamentals/; max_position=11; speed_of_play=0; difficulty_index=3; min_blinds=5; min_position=7; ante_index=0; sbjs_udata=vst%3D7%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2011_2_3%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F89.0.4389.114%20Safari%2F537.36; sbjs_session=pgs%3D9%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fpokercoaching.com%2Fcashpreflopcharts%2F; amplitude_id_acaae423faf755c75527a35f0b6aea02pokercoaching.com=eyJkZXZpY2VJZCI6ImU4ZTQxZTM4LTE4ZmItNDgyZi05OGNhLTY0MjhlYmNkYjE3ZlIiLCJ1c2VySWQiOiIxODAyMDQiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE2MTgzNTA5OTU2MzAsImxhc3RFdmVudFRpbWUiOjE2MTgzNTEzMTczNzQsImV2ZW50SWQiOjEyNywiaWRlbnRpZnlJZCI6NjYsInNlcXVlbmNlTnVtYmVyIjoxOTN9; _gali=main'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return parse_response(response)


def recursive_defaultdict():
    return defaultdict(recursive_defaultdict)


RANGES = recursive_defaultdict()
for hero_pos in POSITIONS:
    for action in ACTIONS:
        if action == 'RFI' and hero_pos != 'BB':
            RANGES[hero_pos]['RFI'] = query(hero_pos)
            continue

        for opp_pos in POSITIONS:
            print(hero_pos, action, opp_pos)
            qqq = query(hero_pos, action=action, opp=opp_pos)
            if qqq is None:
                print('Not found')
                continue
            RANGES[hero_pos][action][opp_pos] = qqq


with open('gto_ranges.json', 'w') as fff:
    fff.write(json.dumps(RANGES))
