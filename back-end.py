import re
import time
from dotenv import dotenv_values
from requests import get, exceptions
from flask import Flask, request, render_template, jsonify
import threading

app = Flask(__name__)
STEAM_API_KEY = dotenv_values(".env")["STEAM_API_KEY"]

# User info cache and its lock for use by daemon thread
USER_CACHE = {}
CACHE_LOCK = threading.Lock()

# Evict entries if they go unused for an hour or greater
CACHE_TIME_LIMIT = 60 * 60 

# The rate, in seconds, at which the daemon checks the cache
DAEMON_RATE = 60

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/playerachievements", methods=["post"])
def get_player_achievements():
    username = request.get_json()["username"]


    with CACHE_LOCK:
        # If username is not in the cache, fetch it from Steam API
        if username not in USER_CACHE:
            uid = get_uid_from_username(username)
            if uid is None:
                return jsonify({ 'response' : 'error', 'status' : 'User does not exist.'})
            USER_CACHE[username] = { "steam_id" : uid }
        else:
            uid = USER_CACHE[username]["steam_id"]

        # Update the user info's time of most recent access
        USER_CACHE[username]["last_accessed"] = time.time()
    list = get(f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=440&key={STEAM_API_KEY}&steamid={uid}")
    return jsonify(list.text)

def get_uid_from_username(username: str) -> str|None:
    try:
        data = get(f"https://steamcommunity.com/id/{username}/")

        # Raise HTTP error if status value indicates one
        data.raise_for_status()

        # Capturing: "steamid":"012345"
        uid = re.search(r"\"steamid\":\"(\d+)\"", data.text).group(1)
    except exceptions.HTTPError as _:
        print(f"ERROR: Steam API fetch for username {username} failed.")
    except IndexError as _:
        print(f"ERROR: username \"{username}\" does not exist.")
    else:
        # Return Steam ID if no error occurred
        return uid
    return None

def thread_check_user_cache():
    while True:
        curr = time.time()
        with CACHE_LOCK:
            for user in USER_CACHE:
                last_accessed = USER_CACHE[user]["last_accessed"]
                if curr - last_accessed >= CACHE_TIME_LIMIT:
                    USER_CACHE.pop(user)
        time.sleep(DAEMON_RATE)

if __name__ == "__main__":
    t = threading.Thread(target=thread_check_user_cache, daemon=True)
    t.start()
    app.run(debug=True)