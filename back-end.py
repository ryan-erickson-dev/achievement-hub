import re
import time
from dotenv import dotenv_values
from requests import get, exceptions
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
STEAM_API_KEY = dotenv_values(".env")["STEAM_API_KEY"]
USER_CACHE = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/playerachievements", methods=["post"])
def get_player_achievements():
    username = request.form["username"]
    print(username)
    if username not in USER_CACHE:
        print("user not in cache.\n")
        uid = get_uid_from_username(username)
        if uid == None:
            return
        USER_CACHE[username] = { 
            "steam_id" : get_uid_from_username(username),
            "last_accessed": time.time()
        }
        print(USER_CACHE[username])
    else:
        print("user found in cache!\n")
        USER_CACHE[username]["last_accessed"] = time.time()
        print(USER_CACHE[username])
    
    uid = USER_CACHE[username]["steam_id"]
    list = get(f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=440&key={STEAM_API_KEY}&steamid={uid}")
    print(list.text)
    return "Hello"

def get_uid_from_username(username: str) -> str|None:
    try:
        data = get(f"https://steamcommunity.com/id/{username}/")
        data.raise_for_status()

        # Capturing: "steamid":"012345"
        # "Match" matches the entire string from the start. "Findall" searches
        # for occurrences of the pattern in the string.
        uid = re.findall(r"\"steamid\":\"(\d+)\"", data.text)[0]
    except exceptions.HTTPError as http_error:
        print("ERROR:", http_error)
        return None
    else:
        return uid


if __name__ == "__main__":
    app.run(debug=True)