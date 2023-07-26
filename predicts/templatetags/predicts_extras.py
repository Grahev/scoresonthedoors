from django import template
from datetime import datetime, timezone

register = template.Library()

@register.filter(name='date_only')
def date_only(value):
    return str(value).split('T')[0]

@register.filter(name='time_only')
def time_only(value):
    return str(value).split('T')[1].split('+')[0]

@register.filter(name='to_datetime')
def to_datetime(value):
    # print(f'This is my entry value {value}\n\n\n')
    date_string = value.split('+')[0]
    # print(date_string)
    datetime_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    return datetime_object

@register.filter
def is_past_due(date_string):
    try:
        # Convert the date string to a datetime object with timezone information
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    
        
        # Get the current date and time with timezone information
        current_datetime = datetime.now(timezone.utc)

        # Compare the dates and return True if the date is past due
        return date_obj < current_datetime

    except (ValueError, AttributeError):
        # If the date string is not in the correct format, return False
        return False