from dotenv import dotenv_values
from requests import get

def main():
    STEAM_API_KEY = dotenv_values(".env")["STEAM_API_KEY"]
    data = get("http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid=440&format=json")
    print(data.json())

if __name__ == "__main__":
    main()