from datetime import datetime, timedelta
from dateutil import parser


def parse_date(date):
    if date == "Сегодня":
        now = datetime.now()
        return str(now.year)+" "+str(now.month)+" "+str(now.day)

    if date == "Вчера":
        yesterday = datetime.now() - timedelta(days=1)
        return str(yesterday.year)+" "+str(yesterday.month)+" "+str(yesterday.day)

    date_list = date.split(' ')
    month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
           'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    month = month_list.index(date_list[1]) + 1
    if month < 10:
        month = '0' + str(month)
    date = date.replace(date_list[1], str(month))
    return parser.parse(date)
