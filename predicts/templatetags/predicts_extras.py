from django import template
from datetime import datetime, timezone

register = template.Library()

@register.filter
def reverse_list(value):
    # Reverse the dictionary
    reversed_dict = dict(list(value.items())[::-1])
    return reversed_dict

@register.filter(name='date_only')
def date_only(value):
    return str(value).split('T')[0]

@register.filter(name='time_only')
def time_only(value):
    """
    Extracts only the time part (hours and minutes) from a datetime string.
    
    :param value: The datetime string.
    :return: The time part of the datetime string.
    """
    try:
        time = str(value).split('T')[1].split(':')[:2]
        return ':'.join(time)
    except (IndexError, AttributeError) as e:
        # Handle exceptions if necessary
        return value

# @register.filter(name='to_datetime')
# def to_datetime(value):
#     # print(f'This is my entry value {value}\n\n\n')
#     date_string = value.split('+')[0]
#     # print(date_string)
#     datetime_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
#     return datetime_object

@register.filter(name='to_datetime')
def to_datetime(value, date_format='%Y-%m-%d'):
    """
    Convert a datetime string to a datetime object and format it.
    
    :param value: The datetime string in ISO 8601 format.
    :param date_format: The format to convert the date to. Default is '%Y-%m-%d'.
    :return: Formatted date string.
    """
    try:
        # Remove timezone information if present
        date_string = value.split('Z')[0]
        # Convert to datetime object
        datetime_object = datetime.fromisoformat(date_string)
        # Format datetime object to desired format
        formatted_date = datetime_object.strftime(date_format)
        return formatted_date
    except (ValueError, TypeError) as e:
        # Log the error or handle it accordingly
        return value

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