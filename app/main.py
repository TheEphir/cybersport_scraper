import requests
from enum import Enum
from typing import Union
from datetime import datetime
import requests
import re
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

def scrap_matches(game:str):
    site_url={
        "dota_2":"https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches",
        "rocket_league":"https://liquipedia.net/rocketleague/Liquipedia:Matches",
        "counter_strike":"https://liquipedia.net/counterstrike/Liquipedia:Matches"
    }
    
    site = requests.get(site_url[game]).text
    soup = BeautifulSoup(site, features="html.parser")
    matches = soup.find_all("table", class_=re.compile(r"\Dmatches\D"))
    
    matches_info = []
    
    for match in matches:
        try:
            left_team = match.find("td", class_="team-left").find("a")["title"]
            right_team = match.find("td", class_="team-right").find("a")["title"]
            match_time = datetime.isoformat(datetime.astimezone(datetime.fromtimestamp(int(match.find("td", class_="match-filler").find("span", class_="timer-object")["data-timestamp"])))) # find timestamp and convert it into readable format)
            # frometimestamp = read timestamp, astimezone = make time to local tz, isoformat = make all this things to readable str format
            
            if game == 'dota_2':
                tournament_name = match.find("td", class_="match-filler").find("div", class_=re.compile(r"tournament-text")).find("a").text
            if game == 'rocket_league':
                tournament_name = match.find("td", class_="match-filler").find("td", class_=not "match-countdown").find("a").text
            if game == 'counter_strike':
                tournament_name = match.find("td", class_="match-filler").find("div", class_=re.compile(r"text")).find("a").text
        except TypeError:
            left_team = "TBD"
            right_team = "TBD"
                
        matches_info.append({
            "left_team":left_team,
            "right_team":right_team,
            "match_time":match_time.replace("T"," ")[:-6], # isoformat match time was 2024-08-25T13:30:00+03:00, so its should made readable
            "tournament_name":tournament_name,
        })
    
    return matches_info


class Games(str, Enum):
    dota_2 = "dota_2"
    rocket_league = "rocket_league"
    counter_strike = "counter_strike"


@app.get("/")
def read_root():
    return {"Check Docs ": "please))"}


@app.get("/game/{game}")
def read_item(game: Games):
    return scrap_matches(game)