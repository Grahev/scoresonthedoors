from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='date_only')
def date_only(value):
    return str(value).split('T')[0]

@register.filter(name='time_only')
def time_only(value):
    return str(value).split('T')[1].split('+')[0]

@register.filter(name='to_datetime')
def to_datetime(value):
    print(f'This is my entry value {value}\n\n\n')
    date_string = value.split('+')[0]
    print(date_string)
    datetime_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    return datetime_object