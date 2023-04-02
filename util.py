from datetime import datetime


def formatted_time():

    now = datetime.now()
    weekday_kr = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    weekday = weekday_kr[now.weekday()]
    
    if now.hour < 12:
        am_pm = "오전"
    else:
        am_pm = "오후"
    
    hour = now.strftime("%I시")
    return "{}, {} {}".format(weekday, am_pm, hour)

