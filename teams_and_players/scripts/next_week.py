from predicts.models import Week

def run():
    week = Week.objects.get(pk=1)
    week.next_week()
    week.save()
    print(week)