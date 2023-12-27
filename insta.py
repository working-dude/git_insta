file_content = """
from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return "Alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == '__main__':
    keep_alive()
"""

file_name = 'keep_alive.py'

with open(file_name, 'w') as file:
    file.write(file_content)

print(f"File '{file_name}' has been created with Flask app code.")

import json

data = {
    "uuids": {
        "phone_id": "a4d7e595-f67b-4ec4-83d6-6b57be56cc7e",
        "uuid": "78ed6eb6-4f7f-4105-9273-97727653bc1a",
        "client_session_id": "77530588-55d3-468e-a9c9-6f34b83539c6",
        "advertising_id": "dc6cbb11-af1b-4623-98db-5e24ece806d7",
        "android_device_id": "android-898dd7123b892321",
        "request_id": "691881af-4919-43b6-ac12-d47c3d196356",
        "tray_session_id": "44c89261-a189-461d-a61d-755911b163fb"
    },
    "mid": "ZYW80gABAAFZW0d_HQtXYfd1saZj",
    "ig_u_rur": None,
    "ig_www_claim": None,
    "authorization_data": {
        "ds_user_id": "63253668568",
        "sessionid": "63253668568%3AYDtMACGZTYIdVY%3A28%3AAYcQu7uWIfTmpe6IPZVaMY7RH7UCzdrAGBjQWQcBWQ"
    },
    "cookies": {},
    "last_login": 1703263451.1986449,
    "device_settings": {
        "app_version": "269.0.0.18.75",
        "android_version": 26,
        "android_release": "8.0.0",
        "dpi": "480dpi",
        "resolution": "1080x1920",
        "manufacturer": "OnePlus",
        "device": "devitron",
        "model": "6T Dev",
        "cpu": "qcom",
        "version_code": "314665256"
    },
    "user_agent": "Instagram 269.0.0.18.75 Android (26/8.0.0; 480dpi; 1080x1920; OnePlus; 6T Dev; devitron; qcom; en_US; 314665256)",
    "country": "US",
    "country_code": 1,
    "locale": "en_US",
    "timezone_offset": -14400
}

file_name = 'dump.json'

with open(file_name, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"JSON file '{file_name}' has been created with Instagram data.")
from instagrapi import Client
from instagrapi.types import  StoryMedia
import time, schedule
from pathlib import Path
import os
from keep_alive import keep_alive
import random
from datetime import datetime

keep_alive()

cl = Client()

USERNAME = "Bacchematrimony"
PASSWORD = "kanishkisacckabaaphai"

cl.load_settings(Path('dump.json'))

def takingReelFromExplore():
    reelfeed = []
    post_ids = []
    post_id =''

    cl.get_timeline_feed()

    reelfeed=cl.explore_reels()

    # Iterate through each StoryMedia object in the reelfeed
    for item in reelfeed:
        post_id = item.pk
        if post_id:
            # Append the post ID to the list
            post_ids.append(post_id)
    post_ids = random.sample(post_ids, random.randint(1,3))
    print("List of Post IDs:", post_ids)
    return post_ids

def requiredReel():
    post_ids = []
    post_ids=takingReelFromExplore()
    # print("new ",post_ids)
    while len(post_ids)<2:
        post_ids=post_ids+takingReelFromExplore()
        # print("new if ",post_ids)
    return post_ids

# Print the list of post IDs
def uploadingreel():
    post_ids = []
    post_ids=requiredReel()

    while post_ids:
        random_index = random.randint(0, len(post_ids) - 1)
        media_path = cl.video_download(int(post_ids[random_index]))
        print(media_path)
        time.sleep(random.randint(60,120))
        cl.video_upload_to_story(
            media_path,
            medias=[StoryMedia(media_pk=int(post_ids[random_index]))],
        )
        os.remove(media_path)
        media_path = str(media_path) + '.jpg'
        os.remove(media_path)
        post_ids.pop(random_index)

# takingReelFromExplore()
# uploadingreel()

# schedule.every().day.at("01:35").do(uploadingreel)
# schedule.every().day.at("08:35").do(uploadingreel)
# schedule.every().day.at("15:35").do(uploadingreel)
# schedule.every().day.at(f"{random.randint(1,2):02d}:{random.randint(0, 30):02d}").do(uploadingreel)
# schedule.every().day.at(f"{random.randint(8, 10):02d}:{random.randint(30, 60):02d}").do(uploadingreel)
# schedule.every().day.at(f"{random.randint(15, 17):02d}:{random.randint(0, 60):02d}").do(uploadingreel)

def generate_random_time():
    # Generate a random time within specific ranges
    hour_ranges = [
        f"{random.randint(1,2):02d}:{random.randint(0, 30):02d}",
        f"{random.randint(8, 10):02d}:{random.randint(30, 60):02d}",
        f"{random.randint(15, 17):02d}:{random.randint(0, 60):02d}"
    ]
    return hour_ranges

# Schedule the initial job at a random time
random_time = generate_random_time()
print("Initial Random Times:", random_time)
schedule.every().day.at(random_time[0]).do(uploadingreel)
schedule.every().day.at(random_time[1]).do(uploadingreel)
schedule.every().day.at(random_time[2]).do(uploadingreel)

current_time = datetime.now()
print("Current Time:", current_time.strftime("%H:%M:%S"))

# if current_time.hour == 0 and current_time.minute == 0:
#     random_time = generate_random_time()
#     print("New Random Times:", random_time)
#     schedule.clear()
#     schedule.every().day.at(random_time[0]).do(uploadingreel)
#     schedule.every().day.at(random_time[1]).do(uploadingreel)
#     schedule.every().day.at(random_time[2]).do(uploadingreel)

while True:
    current_time = datetime.now()
    # print("Current Time:", current_time.strftime("%H:%M:%S"))

    # Check if it's a new day and generate new random times for each range
    if current_time.hour == 0 and current_time.minute == 0 and current_time.second == 0:
        random_time = generate_random_time()
        print("New Random Times:", random_time)
        print("Current Time:", current_time.strftime("%H:%M:%S"))
        schedule.clear()
        schedule.every().day.at(random_time[0]).do(uploadingreel)
        schedule.every().day.at(random_time[1]).do(uploadingreel)
        schedule.every().day.at(random_time[2]).do(uploadingreel)

    # Run pending scheduled jobs
    schedule.run_pending()
    time.sleep(10)