import re
from dotenv import dotenv_values
from requests import get, exceptions
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
STEAM_API_KEY = dotenv_values(".env")["STEAM_API_KEY"]

@app.route("/")
def index():
    return render_template("index.html")


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