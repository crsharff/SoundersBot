#!/usr/bin/python3
import os
import sys
import re

import praw
import logging.handlers
import datetime
import time
import traceback
import configparser

### Config ###
import mls
from teams import Teams

LOG_FOLDER_NAME = "logs"
SUBREDDIT = "SoundersFC"
SUBREDDIT_TEAMS = "mls"
USER_AGENT = "SoundersSideBarUpdater (by /u/Watchful1)"
TEAM_NAME = "Seattle Sounders FC"

### Logging setup ###
LOG_LEVEL = logging.DEBUG
if not os.path.exists(LOG_FOLDER_NAME):
    os.makedirs(LOG_FOLDER_NAME)
LOG_FILENAME = LOG_FOLDER_NAME + "/" + "bot.log"
LOG_FILE_BACKUPCOUNT = 5
LOG_FILE_MAXSIZE = 1024 * 256

log = logging.getLogger("bot")
log.setLevel(LOG_LEVEL)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
log_stderrHandler = logging.StreamHandler()
log_stderrHandler.setFormatter(log_formatter)
log.addHandler(log_stderrHandler)
if LOG_FILENAME is not None:
    log_fileHandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=LOG_FILE_MAXSIZE,
                                                           backupCount=LOG_FILE_BACKUPCOUNT)
    log_formatter_file = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_fileHandler.setFormatter(log_formatter_file)
    log.addHandler(log_fileHandler)

comps = [{'name': 'MLS', 'link': '/MLS', 'acronym': 'MLS'}
    , {'name': 'Preseason', 'link': '/MLS', 'acronym': 'UNK'}
    , {'name': 'CONCACAF', 'link': 'http://category/champions-league/schedule-results', 'acronym': 'CCL'}
    , {'name': 'Open Cup', 'link': '/MLS', 'acronym': 'OPC'}
         ]

teams = [{'link': '/r/dynamo', 'contains': 'Houston Dynamo'}
    , {'link': '/SEA', 'contains': 'Seattle Sounders FC'}
    , {'link': '/r/SportingKC', 'contains': 'Sporting Kansas City'}
    , {'link': '/r/fcdallas', 'contains': 'FC Dallas'}
    , {'link': '/r/timbers', 'contains': 'Portland Timbers'}
    , {'link': '/r/SJEarthquakes', 'contains': 'San Jose Earthquakes'}
    , {'link': '/r/whitecapsfc', 'contains': 'Vancouver Whitecaps FC'}
    , {'link': '/r/realsaltlake', 'contains': 'Real Salt Lake'}
    , {'link': '/r/LAGalaxy', 'contains': 'LA Galaxy'}
    , {'link': '/r/Rapids', 'contains': 'Colorado Rapids'}
    , {'link': '/r/minnesotaunited', 'contains': 'Minnesota United'}
    , {'link': '/r/LAFC', 'contains': 'Los Angeles Football Club'}]

def parseSchedule():
    page = requests.get("https://www.soundersfc.com/schedule?year=2019")
    tree = html.fromstring(page.content)

    schedule = []
    date = ""
    for i, element in enumerate(tree.xpath("//ul[contains(@class,'schedule_list')]/li[contains(@class,'row')]")):
        match = {}
        dateElement = element.xpath(".//div[contains(@class,'match_date')]/text()")
        if not len(dateElement):
            log.warning("Couldn't find date for match, skipping")
            continue

        timeElement = element.xpath(".//span[contains(@class,'match_time')]/text()")
        if not len(timeElement):
            log.warning("Couldn't find time for match, skipping")
            continue

        if 'TBD' in timeElement[0]:
            match['datetime'] = datetime.datetime.strptime(dateElement[0].strip(), "%A, %B %d, %Y")
            match['status'] = 'tbd'
        else:
            match['datetime'] = datetime.datetime.strptime(dateElement[0] + timeElement[0], "%A, %B %d, %Y %I:%M%p PT")
            match['status'] = ''

        statusElement = element.xpath(".//span[contains(@class,'match_result')]/text()")
        if len(statusElement):
            match['scoreString'] = statusElement[0].replace('IN', '').replace('OSS', '').replace('RAW', '')
            match['status'] = 'final'
            homeScores = re.findall('(\d+).*-', statusElement[0])
            if len(homeScores):
                match['homeScore'] = homeScores[0]
            else:
                match['homeScore'] = -1

            awayScores = re.findall('-.*(\d+)', statusElement[0])
            if len(awayScores):
                match['awayScore'] = awayScores[0]
            else:
                match['awayScore'] = -1
        else:
            match['status'] = ''
            match['homeScore'] = -1
            match['awayScore'] = -1

        opponentElement = element.xpath(".//div[contains(@class,'match_matchup')]/text()")
        homeAwayElement = element.xpath(".//span[contains(@class,'match_home_away')]/text()")

        if not len(opponentElement) or not len(homeAwayElement):
            log.debug("Could not find any opponent")
            continue

        if homeAwayElement[0] == 'H':
            match['home'] = TEAM_NAME
            match['away'] = opponentElement[0].title()
        elif homeAwayElement[0] == 'A':
            match['home'] = opponentElement[0][3:].title()
            match['away'] = TEAM_NAME
        else:
            log.debug("Could not find opponent")
            continue

        compElement = element.xpath(".//span[contains(@class,'match_competition ')]/text()")
        if len(compElement):
            match['comp'] = compElement[0]
        else:
            match['comp'] = ""

        tvElement = element.xpath(".//div[@class='match_info']/text()")
        if len(tvElement):
            match['tv'] = tvElement[0][0:tvElement[0].find(',')].replace('\n', '')
        else:
            match['tv'] = ""

        schedule.append(match)

    return schedule


log.debug("Connecting to reddit")

once = False
debug = False
user = None

if len(sys.argv) >= 2:
    user = sys.argv[1]
    for arg in sys.argv:
        if arg == 'once':
            once = True
        elif arg == 'debug':
            debug = True
else:
    log.error("No user specified, aborting")
    sys.exit(0)

log.debug("User: {0}, Once: {1}, Debug: {2}".format(user, once, debug))

try:
    r = praw.Reddit(
        user
        , user_agent=USER_AGENT)
except configparser.NoSectionError:
    log.error("User " + user + " not in praw.ini, aborting")
    sys.exit(0)

while True:
    startTime = time.perf_counter()
    log.debug("Starting run")

    strListGames = []
    strListTable = []
    skip = False

    # schedule = []
    # standings = []
    # try:
    #     schedule = parseSchedule()
    #     standings = parseTable()
    # except Exception as err:
    #     log.warning("Exception parsing schedule")
    #     log.warning(traceback.format_exc())
    #     skip = True

    try:
        # teamGames = []
        # nextGameIndex = -1
        # lastRecentIndex = 0
        # log.debug("Schedule Length: {}".format(len(schedule)))
        # for game in schedule:
        #     if game['home'] == TEAM_NAME or game['away'] == TEAM_NAME:
        #         teamGames.append(game)
        #         if game['datetime'] + datetime.timedelta(hours=2) > datetime.datetime.now() and nextGameIndex == -1:
        #             log.debug("Setting nextGameIndex to {}".format(len(teamGames) - 1))
        #             nextGameIndex = len(teamGames) - 1
        schedule = mls.getSchedule(Teams.SEATTLE_SOUNDERS_FC)
        recentMatches = schedule.getPreviousMatches(10)

        strListGames.append("##Recent Match Results\n\n")
        strListGames.append("Date|||Opponent|Result\n")
        strListGames.append(":---:|:---:|---|:---|:---:|:---:\n")

        for match in recentMatches:
            strListGames.append(match.details.date.strftime("%m/%d"))
            strListGames.append("|[](")
            strListGames.append("/MLS") #TODO
            strListGames.append(")|")
            if match.home_team == Teams.SEATTLE_SOUNDERS_FC.name:
                strListGames.append("H")
                strListGames.append("|")
                strListGames.append(match.away_team.name)
            else:
                strListGames.append("A")
                strListGames.append("|")
                strListGames.append(match.home_team.name)
            strListGames.append("|[")
            strListGames.append(match.details.result)
            strListGames.append("]")
            strListGames.append("\n")

        upcomingMatches = schedule.getUpcomingMatches(6)

        strListGames.append("##Upcoming Matches\n\n")
        strListGames.append("Date|||Opponent|PDT|Watch\n")
        strListGames.append(":---:|:---:|---|---|---|:---\n")
        for match in upcomingMatches:
            strListGames.append(match.details.date.strftime("%m/%d"))
            strListGames.append("|")
            strListGames.append("[](")
            strListGames.append("/MLS") #TODO
            strListGames.append(")|")
            if match.home_team == Teams.SEATTLE_SOUNDERS_FC.name:
                strListGames.append("H|")
                strListGames.append(match.away_team.name)
            else:
                strListGames.append("A|")
                strListGames.append(match.home_team.name)
            strListGames.append("|")
            # if game['status'] == 'tbd':
            #     strListGames.append("TBD")
            # else:
            #     strListGames.append(game['datetime'].strftime("%I:%M %p"))
            # strListGames.append("|")
            # strListGames.append(game['tv'])
            # strListGames.append("\n")

        strListGames.append("\n\n")


    except Exception as err:
        log.warning("Exception parsing table")
        log.warning(traceback.format_exc())
        skip = True

    #buildWesternConferenceStandingsTable()
    try:
        strListTable.append("##2019 Western Conference Standings\n\n")
        strListTable.append("Club|Pts|GP|W|L|D|GD\n")
        strListTable.append(":---|:---:|:---:|:---:|:---:|:---:|:---:\n")

        for team in mls.getWesternConferenceStandings():
            strListTable.append(team.name)
            strListTable.append(" | ")
            strListTable.append(team.details.points)
            strListTable.append(" | ")
            strListTable.append(team.details.games_played)
            strListTable.append(" | ")
            strListTable.append(team.details.wins)
            strListTable.append(" | ")
            strListTable.append(team.details.losses)
            strListTable.append(" | ")
            strListTable.append(team.details.ties)
            strListTable.append(" | ")
            strListTable.append(team.details.goal_difference)
            strListTable.append(" |\n")

        strListTable.append("\n\n\n")
    except Exception as err:
        log.warning("Exception parsing table")
        log.warning(traceback.format_exc())
        skip = True

    if not skip:
        try:
            subreddit = r.subreddit(SUBREDDIT)
            description = subreddit.description
            begin = description[0:description.find("##Recent Match Results")]
            mid = description[description.find("##Tacoma Defiance Matches"):description.find("##2019 Western Conference Standings")]
            end = description[description.find("##2019 Top Goal Scorers "):]

            if debug:
                log.info("{0}{1}{2}{3}{4}".format(begin, ''.join(strListGames), mid, ''.join(strListTable), end))
                #log.info(begin + ''.join(strListGames) + mid + ''.join(strListTable) + end)
            else:
                try:
                    subreddit.mod.update(description=begin + ''.join(strListGames) + mid + ''.join(strListTable) + end)
                except Exception as err:
                    log.warning("Exception updating sidebar")
                    log.warning(traceback.format_exc())
        except Exception as err:
            log.warning("Broken sidebar")
            log.warning(traceback.format_exc())
            skip = True

    log.debug("Run complete after: %d", int(time.perf_counter() - startTime))
    if once:
        break
    time.sleep(15 * 60)
