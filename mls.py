from bs4 import BeautifulSoup
import requests
import requests_cache

MLS_STANDINGS_URL = "https://www.mlssoccer.com/standings"
SOUNDERS_FC_SCHEDULE_URL = "https://www.soundersfc.com/schedule"
NUMBER_OF_CONFERENCES = 2
EASTERN_CONFERENCE = "Eastern"
WESTERN_CONFERENCE = "Western"
EASTERN_CONFERENCE_INDEX = 0
WESTERN_CONFERENCE_INDEX = 1
HOME = 'H'
AWAY = 'A'

requests_cache.install_cache('mls_cache', backend='memory')

def getTeams():
    return getEasternConferenceTeams() + getWesternConferenceTeams()

def getEasternConferenceTeams():
    conference_tables = getConferenceTables()
    eastern_conference_table = conference_tables[EASTERN_CONFERENCE_INDEX]
    eastern_conference_teams = parseTable(EASTERN_CONFERENCE, eastern_conference_table)
    return eastern_conference_teams

def getEasternConferenceStandings():
    eastern_conference_teams = getEasternConferenceTeams()
    return sorted(eastern_conference_teams, key=lambda team: team.rank)

def getWesternConferenceTeams():
    conference_tables = getConferenceTables()
    western_conference_table = conference_tables[WESTERN_CONFERENCE_INDEX]
    western_conference_teams = parseTable(WESTERN_CONFERENCE, western_conference_table)
    return western_conference_teams

def getWesternConferenceStandings():
    western_conference_teams = getWesternConferenceTeams()
    return sorted(western_conference_teams, key=lambda team: team.rank)

def getNumberOfTeamsInEasternConference():
    return len(getEasternConferenceTeams())

def getNumberOfTeamsInWesternConference():
    return len(getWesternConferenceTeams())

def getSchedule(team):
    page = requests.get(SOUNDERS_FC_SCHEDULE_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    matches = soup.find(class_="schedule_list").find_all(class_="row")
    for match in matches:
        home_away = match.select_one(".match_home_away").text
        opponent = getTeam(match.select_one(".match_matchup"))
        location = match.select_one(".match_location_short")
        league = match.select_one(".match_competition")
        date = match.select_one(".match_date")
        result = match.select_one(".match_result")
        details = MatchDetails(date, location, league, result)
        match = Match(team if home_away == HOME else opponent, team if home_away == AWAY else opponent, details)
    return match

def getTeam(team):
    for team in getTeams():
        if team.name.lower() == team.lower():
            return team

def getConferenceTables():
    page = requests.get(MLS_STANDINGS_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    conference_tables = soup.find_all(class_="standings_table")
    if len(conference_tables) != NUMBER_OF_CONFERENCES:
        return Exception
    return conference_tables

def parseTable(conference, conference_table):
    teams = []
    for team in conference_table.select("tbody tr")[1:]: #Skip first element of standings table since it is a header
        club_name = team.find("td", {"data-title": "Club"}).select('a .hide-on-mobile-inline')[0].getText()
        rank = int(team.find("td", {"data-title": "Rank"}).getText())
        points = int(team.find("td", {"data-title": "Points"}).getText())
        games_played = int(team.find("td", {"data-title": "Games Played"}).getText())
        points_per_game = float(team.find("td", {"data-title": "Points Per Game"}).getText())
        goals_for = int(team.find("td", {"data-title": "Goals For"}).getText())
        goals_difference = int(team.find("td", {"data-title": "Goal Difference"}).getText())
        wins = int(team.find("td", {"data-title": "Wins"}).getText())
        losses = int(team.find("td", {"data-title": "Losses"}).getText())
        ties = int(team.find("td", {"data-title": "Ties"}).getText())

        details = TeamStatistics(points, games_played, points_per_game, goals_for, goals_difference, wins, losses, ties)
        team = Team(club_name, conference, rank, details)
        teams.append(team)
    return teams

class Team:
    def __init__(self, name, conference, rank, details):
        self.name = name
        self.conference = conference
        self.rank = rank
        self.details = details

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class TeamStatistics:
    def __init__(self, points, games_played, points_per_game, goals_for, goals_difference, wins, losses, ties):
        self.points = points
        self.games_played = games_played
        self.points_per_game = points_per_game
        self.goals_for = goals_for
        self.goals_difference = goals_difference
        self.wins = wins
        self.losses = losses
        self.ties = ties

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class Schedule:
    def __init__(self):
        self.matches = []

    def addMatch(self, match):
        self.matches.append(match)

class Match:
    def __init__(self, home_team, away_team, details):
        self.home_team = home_team
        self.away_team = away_team
        self.details = details

class MatchDetails:
    def __init__(self, date, location, league, result):
        self.date = date
        self.location = location
        self.league = league
        self.result = result
