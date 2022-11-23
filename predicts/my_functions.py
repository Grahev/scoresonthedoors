import requests
from predicts.models import MatchEvents, MatchPrediction
from predicts.models import Match



def match_one_x_two(prediction):
    """return 1 X 2 for match"""
    if prediction.match.hTeamScore > prediction.match.aTeamScore:
        match_winner = '1'
    elif prediction.match.hTeamScore == prediction.match.aTeamScore:
        match_winner = 'X'
    elif prediction.match.hTeamScore < prediction.match.aTeamScore:
        match_winner = '2'
    return match_winner

def prediction_one_x_two(prediction):
    """return 1 X 2 for match prediction"""
    if prediction.homeTeamScore > prediction.awayTeamScore:
        prediction_winner = '1'
    elif prediction.homeTeamScore == prediction.awayTeamScore:
        prediction_winner = 'X'
    elif prediction.homeTeamScore < prediction.awayTeamScore:
        prediction_winner = '2'
    return prediction_winner

def single_match_points(match):
    unchacked_predictions = MatchPrediction.objects.filter(match__match_id=match.match_id)
    print(unchacked_predictions)

    for prediction in unchacked_predictions:
        points = 0
        goal_scorers = MatchEvents.objects.filter(match=prediction.match).filter(type='Goal').order_by('time')
        red_cards = MatchEvents.objects.filter(match=prediction.match).filter(detail='Red Card')
        print(f'number of red cards: {len(red_cards)}')
   
        if prediction.match.status == 'FT':
            print('Match Finished calculate points')
            #red card minus points
            # if MatchEvents.objects.filter(match=prediction.match).filter(detail='Red Card').filter(player=prediction.goalScorer).exists():
            if MatchEvents.objects.filter(match=prediction.match).filter(detail='Red Card').filter(team=prediction.goalScorer.team).exists():
            #minus points
                print('minus point for red card')
                points -= 1
            else:
                print('no penalty points for red card')
            
            #goalscorers points
            try:
                if goal_scorers[0].player.name == prediction.goalScorer.name:
                    points+=3
                    print('3 points for correct first goalscorer')
                else:
                  for goal in goal_scorers:
                    if goal.player.name == prediction.goalScorer.name:
                      print('1 point for anytime goalscorer')
                      points +=1
                      break
                    else:
                      continue
            except:
                points += 0
            
            #correct score points
            if prediction.homeTeamScore == prediction.match.hTeamScore and prediction.awayTeamScore == prediction.match.aTeamScore:
                points +=3
                print('3 points for correct score')
            #winning team points
            else: 
                match_winner = match_one_x_two(prediction)
                prediction_winner = prediction_one_x_two(prediction)
                if match_winner == prediction_winner:
                    points +=1
                    print('1 point for winner')
                else:
                    points +=0



            p = MatchPrediction.objects.filter(pk=prediction.pk)
            p.update(points=points, checked=True)
            print(f'points: {points} - {p} updated')

    
        else:
            print('match status not finished')

 