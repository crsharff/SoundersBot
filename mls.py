from bs4 import BeautifulSoup
import requests

MLS_STANDINGS_URL = "https://www.mlssoccer.com/standings"
MLS_SCHEDULE_URL = "https://www.soundersfc.com/schedule"
NUMBER_OF_CONFERENCES = 2

eastern_conference_teams = []
western_conference_teams = []

def getTeams():

def getEasternConferenceTeams():

def getWesternConferenceTeams():

def getStandings():
    page = requests.get("https://www.mlssoccer.com/standings")
    soup = BeautifulSoup(page.content, 'html.parser')
    conference_tables = soup.find_all(class_="standings_table")
    if conference_tables != NUMBER_OF_CONFERENCES:
        return Exception

    eastern_conference = conference_tables[0]
    western_conference = conference_tables[1]

    for team in eastern_conference.select("tbody tr")[1:]: #Skip first element of standings table since it is a header
        eastern_conference_teams.append(Team())

def getEasternConferenceStandings():

def getWesternConferenceStandings():

def getNumberOfTeamsInEasternConference():
    return len(getEasternConferenceTeams)

def getNumberofTeamsInWesternConference():
    return len(getWesternConferenceTeams)

def getSchedule(team):


class Team:
    def __init__(self, name, conference, details):
        self.name = name
        self.conference = conference
        self.details = details

class TeamDetails:
    def __init__(self, points, games_played, goals_for, goals_difference, wins, losses, ties):
        self.points = points
        self.games_played = games_played
        self.goals_for = goals_for
        self.goals_difference = goals_difference
        self.wins = wins
        self.losses = losses
        self.ties = ties