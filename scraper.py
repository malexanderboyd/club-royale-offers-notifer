import os
from datetime import datetime
from pathlib import PurePath

import requests
from bs4 import BeautifulSoup
import winotify
import redis
from dataclasses import dataclass


@dataclass
class Reward:
    name: str
    number: str
    offer_name: str
    offer_type: str
    expires: str
    certificate: str
    offer_code: str
    trade_in_value: str


def notify_new_reward(reward: Reward):
    message = f"New reward available for {reward.name}: {reward.offer_name}"
    link = "https://www.clubroyaleoffers.com/"
    notification = winotify.Notification(msg=message, title="Club Royale Offers",
                                         duration="long", app_id="casino scraper")
    notification.add_actions(
        label="Check Now!", launch=link
    )
    notification.show()


def scrape_website(lastname: str, rewardnumber: str):
    # set up redis connection
    r = redis.Redis(host=os.getenv('REDIS_HOST', "localhost"), port=os.getenv('REDIS_PORT', 6379), db=0)

    # build request payload
    payload = {
        "tbxLNameLookup": lastname,
        "tbxPlayerLookup": rewardnumber
    }

    # make POST request
    response = requests.post("https://www.clubroyaleoffers.com/PlayerLookup.asp", data=payload)

    # parse HTML response
    soup = BeautifulSoup(response.content, 'html.parser')
    redeem_forms = soup.find_all("form", {"id": "frmRedeem"})
    rewards = []
    for form in redeem_forms:
        td_with_redeem_form = form.findParent().find_next_siblings("td")
        name = td_with_redeem_form[0].text.strip()
        reward_number = td_with_redeem_form[1].text.strip()
        offer_name = td_with_redeem_form[2].text.strip()
        offer_type = td_with_redeem_form[3].text.strip()
        expires = td_with_redeem_form[4].text.strip()
        certificate = td_with_redeem_form[5].text.strip()
        offer_code = td_with_redeem_form[6].text.strip()
        trade_in_value = td_with_redeem_form[7].text.strip()


        reward_id = f'{rewardnumber}{offer_code}'
        # check if offer code has been seen before
        if r.get(reward_id):
            print(f'{lastname} - {offer_code} already found, skipping!')
            continue  # skip already seen offer code

        # add offer code to Redis
        r.set(reward_id, 1)

        # create Reward object and add to list
        reward = Reward(name, reward_number, offer_name, offer_type, expires, certificate, offer_code, trade_in_value)
        rewards.append(reward)

        # notify if new reward
        notify_new_reward(reward)

    return rewards


if __name__ == '__main__':
    # get environment variables
    lastname = os.environ['LASTNAME']
    rewardnumber = os.environ['REWARDNUMBER']

    rewards = scrape_website(lastname, rewardnumber)

    last_ran_filename = PurePath(os.getcwd(), "last-ran.txt")
    with open(last_ran_filename, 'w') as last_ran_file:
        last_ran_file.write(datetime.now().isoformat())