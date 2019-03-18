from enum import Enum
from collections import namedtuple

Team = namedtuple('Team', ['name', 'scheduleUrl'])

class Teams(Enum):

    @property
    def name(self):
        return self.value.name

    @property
    def scheduleUrl(self):
        return self.value.scheduleUrl

    @staticmethod
    def from_str(team_str):
        for team in Teams:
         if team_str.lower() == team.name.lower():
            return team
        print("Could not find team {}".format(team_str))

    COLUMBUS_CREW_SC = Team("Columbus Crew SC", "https://www.columbuscrewsc.com/schedule")
    TORONTO_FC = Team("Toronto FC", "https://www.torontofc.ca/schedule")
    DC_UNITED = Team("D.C. United", "https://www.dcunited.com/schedule")
    MONTREAL_IMPACT = Team("Montreal Impact", "https://www.impactmontreal.com/en/schedule")
    ORLANDO_CITY_SC = Team("Orlando City SC", "https://www.orlandocitysc.com/schedule")
    NEW_YORK_CITY_FC = Team("New York City FC", "https://www.nycfc.com/schedule")
    NEW_YORK_RED_BULLS = Team("New York Red Bulls", "https://www.newyorkredbulls.com/schedule")
    CHICAGO_FIRE = Team("Chicago Fire", "https://www.chicago-fire.com/schedule")
    NEW_ENGLAND_REVOLUTION = Team("New England Revolution", "https://www.revolutionsoccer.net/schedule")
    PHILADELPHIA_UNION = Team("Philadelphia Union", "https://www.philadelphiaunion.com/schedule")
    ATLANTA_UNITED_FC = Team("Atlanta United FC", "https://www.atlutd.com/schedule")
    FC_CINCINNATI = Team("FC Cincinnati", "https://www.fccincinnati.com/schedule")
    SEATTLE_SOUNDERS_FC = Team("Seattle Sounders FC", "https://www.soundersfc.com/schedule")
    MINNESOTA_UNITED_FC = Team("Minnesota United FC", "https://www.mnufc.com/schedule")
    FC_DALLAS = Team("FC Dallas", "https://www.fcdallas.com/schedule")
    HOUSTON_DYNAMO = Team("Houston Dynamo", "https://www.houstondynamo.com/schedule")
    REAL_SALT_LAKE = Team("Real Salt Lake", "https://www.realsaltlake.com/schedule")
    LOS_ANGELES_FOOTBALL_CLUB = Team("Los Angeles Football Club", "https://www.lafc.com/schedule")
    LA_GALAXY = Team("LA Galaxy", "https://www.lagalaxy.com/schedule")
    PORTLAND_TIMBERS = Team("Portland Timbers", "https://www.timbers.com/schedule")
    COLORADO_RAPIDS = Team("Colorado Rapids", "https://www.coloradorapids.com/schedule")
    SPORTING_KANSAS_CITY = Team("Sporting Kansas City", "https://www.sportingkc.com/schedule")
    VANCOUVER_WHITECAPS_FC = Team("Vancouver Whitecaps FC", "https://www.whitecapsfc.com/schedule")
    SAN_JOSE_EARTHQUAKES = Team("San Jose Earthquakes", "https://www.sjearthquakes.com/schedule")
