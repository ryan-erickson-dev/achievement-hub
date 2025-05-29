import re
from dotenv import dotenv_values
from requests import get
from flask import Flask, render_template_string, redirect, url_for

app = Flask(__name__)
STEAM_API_KEY = dotenv_values(".env")["STEAM_API_KEY"]

@app.route("/")
def main():
    username = ""
    data = get(f"https://steamcommunity.com/id/{username}/")
    
    try:
        # Capturing: "steamid":"012345"
        # "Match" matches the entire string from the start. "Findall" searches
        # for occurrences of the pattern in the string.
        user_id = re.findall(r"\"steamid\":\"(\d+)\"", data.text)[0]
    except:
        print("\nERROR: No Steam ID captured.\n")
    else:
        print(f"\nCaptured Steam ID: {user_id}\n")
        player_info = get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={user_id}&format=json")
        print(player_info.json())
    finally:
        return render_template_string(data.text)

@app.errorhandler(404)
def handle_errors():
    print("error detected.")
    pass

if __name__ == "__main__":
    app.run(debug=True)