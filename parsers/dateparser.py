import datetime
from pytz import timezone

months = {
    "января": '01',
    "февраля": '02',
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": "10",
    "ноября": "11",
    "декабря": "12"}

def published_at_parser(date: str, tz: str) -> str | None:
    '''
        На вход принимает дату в виде *12 января* и timezone
        На выходе конвертирует в дату в строку UTC формата
    '''
    try:
        date = date.split(" ")
        month = months.get(date[1])
        new_date = f"{date[0]}.{month}.{datetime.datetime.now().year}"

        local_tz = timezone(tz)
        local_dt = local_tz.localize(datetime.datetime.strptime(new_date, "%d.%m.%Y")) 
        return local_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None
    
def created_at_parser(tz: str) -> str | None:
    try:
        now = datetime.datetime.now()
        local_tz = timezone(tz)
        local_dt = local_tz.localize(now)
        return local_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None


