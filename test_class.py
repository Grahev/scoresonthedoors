import requests
import json

class Match_Prediction:
    def __init__(self, match_id:int, goalscorer_id:int, home_score:int, away_score:int):
        self.api_url = 'https://www.fotmob.com/api/matchDetails'
        self.match_id = match_id
        self.league_id = None
        self.league_name = None
        self.predicion_goalscorer = None
        self.predicion_goalscorer_id = goalscorer_id
        self.prediction_home_score = home_score
        self.prediction_away_score = away_score
        self.points = 0
        self.match_goalscorer = None
        self.match_goalscorer_id = None
        self.match_home_score = None
        self.match_away_score = None
        self.started = False
        self.finished = False

    def fetch_data(self):

        headers = {
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
        params = {
        'matchId': self.match_id,
        }
        r = requests.get(self.api_url, params=params, headers=headers)
        response = r.json()
        return response
    
    def get_goals(self):
        """return list of goals scorers"""
        goals_data = self.fetch_data()['header']['events']
        # Collect all goal events
        all_goals = []

        if goals_data:
          # Function to extract and append goal details
          def extract_goal_data(team_goals, is_home):
              for player_goals in team_goals.values():
                  for goal in player_goals:
                      goal_data = {
                          'name': goal['player']['name'],
                          'id': goal['player']['id'],
                          'time': goal['time'],
                          'is_home': is_home
                      }
                      all_goals.append(goal_data)


          # Extract home team goals
          extract_goal_data(goals_data['homeTeamGoals'], True)

          # Extract away team goals
          extract_goal_data(goals_data['awayTeamGoals'], False)

          # Sort goals by time
          all_goals.sort(key=lambda x: (x['time'], x.get('overloadTime', 0))) 

          return all_goals
        else:
            all_goals = None
    
    def first_goal(self):
        """return first goalscorer"""
        if self.get_goals():
          return self.get_goals()[0]
        else:
            return None
        
    def get_result(self):
        score = self.fetch_data()['header']['status']['scoreStr']
        return score
    
    def update_match_data(self):
        """fill all match data like home team etc."""
        data = self.fetch_data()
        league_id = data['general']['leagueId']
        league_name = data['general']['leagueName']
        home_tema_name = data['general']['homeTeam']['name']
        home_tema_id = data['general']['homeTeam']['id']
        away_tema_name = data['general']['awayTeam']['name']
        away_tema_id = data['general']['awayTeam']['id']
        started = data['general']['started']
        finished = data['general']['finished']

        if data:
            self.league_id = league_id
            self.league_name = league_name
            self.started = started
            self.finished = finished
            self.match_goalscorer = self.first_goal()['name']
            self.match_goalscorer_id = self.first_goal()['id']
            self.match_home_score = int(self.get_result()[0].strip())
            self.match_away_score = int(self.get_result()[-1].strip())

    def one_x_two(self,home:int,away:int):
        if home > away:
            return 1
        elif home == away:
            return 0
        else:
            return 2
        
    def prediction_result(self):
        return self.one_x_two(self.prediction_home_score, self.prediction_away_score)
    
    def match_result(self):
        return self.one_x_two(self.match_home_score, self.match_away_score)

    def calculate_points(self):
        """calculate points"""
        m_points = 0
        g_points = 0
        if self.prediction_home_score == self.match_home_score and self.prediction_away_score == self.match_away_score:
            m_points =+ 3
        elif self.prediction_result() == self.match_result():
            m_points =+1

        if self.match_goalscorer_id == self.predicion_goalscorer_id:
            g_points =+3
        else:
          for goal in self.get_goals():
            if self.predicion_goalscorer_id == goal['id']:
                g_points += 1
                break
        return m_points + g_points

m = Match_Prediction(4230905,127460,2,3)
# m = Match_Prediction(4475546,127460)
# m = Match_Prediction(4479843,127460) # draw 0-0

data = m.first_goal()
m.update_match_data()

# print(m.league_id)
# print(m.started)
# print(m.finished)
# print(m.match_goalscorer)
# print(m.match_goalscorer_id)
# print(m.match_home_score)
# print(m.match_away_score)
# print(m.prediction_result())
# print(m.match_result())
print(m.calculate_points())
print(m.get_goals())