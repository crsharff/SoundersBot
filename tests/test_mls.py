import mls
from teams import Teams

NUMBER_OF_EASTERN_CONFERENCE_TEAMS = 12
NUMBER_OF_WESTERN_CONFERENCE_TEAMS = 12
MLS_GAMES_PER_SEASON = 34

def test_number_of_eastern_conference_teams():
    teams = mls.getNumberOfTeamsInEasternConference()
    assert teams == NUMBER_OF_EASTERN_CONFERENCE_TEAMS

def test_number_of_western_conference_teams():
    teams = mls.getNumberOfTeamsInWesternConference()
    assert teams == NUMBER_OF_WESTERN_CONFERENCE_TEAMS

def test_get_eastern_conference_standings():
    standings = mls.getEasternConferenceStandings()
    expected_rank = 1
    for team in standings:
        assert team.rank == expected_rank
        expected_rank += 1

def test_get_western_conference_standings():
    standings = mls.getWesternConferenceStandings()
    expected_rank = 1
    for team in standings:
        assert team.rank == expected_rank
        expected_rank += 1

def test_get_western_conference_teams():
    teams = mls.getWesternConferenceTeams()
    assert len(teams) == NUMBER_OF_WESTERN_CONFERENCE_TEAMS

def test_get_eastern_conference_teams():
    teams = mls.getWesternConferenceTeams()
    assert len(teams) == NUMBER_OF_EASTERN_CONFERENCE_TEAMS

def test_get_teams():
    teams = mls.getTeams()
    assert len(teams) == (NUMBER_OF_EASTERN_CONFERENCE_TEAMS + NUMBER_OF_WESTERN_CONFERENCE_TEAMS)

def test_get_team():
    team = mls.getTeam(Teams.SEATTLE_SOUNDERS_FC)
    assert team is not None
    assert isinstance(team, mls.Team)
    assert team.name == Teams.SEATTLE_SOUNDERS_FC.name

def test_get_schedule():
    schedule = mls.getSchedule(Teams.SEATTLE_SOUNDERS_FC)
    assert schedule is not None
    assert isinstance(schedule, mls.Schedule)
    assert len(schedule) >= MLS_GAMES_PER_SEASON