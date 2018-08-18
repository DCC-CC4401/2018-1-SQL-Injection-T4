from django.template.defaulttags import register
from datetime import datetime, timedelta, date

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def zipWith(a, b):
    return zip(a,b)


@register.filter
def weekDayToDate(day, weekDate):
    return (datetime.strptime(weekDate, "%d/%m/%Y") + timedelta(days=int(day))).strftime("%d/%m/%Y")
     

@register.filter
def dayNumberToWeekDay(day, weekDate):
    return weekDate[int(day)]
