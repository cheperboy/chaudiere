import time, calendar
from datetime import datetime, timedelta

def hostname():
    import subprocess
    cmd = """cat /etc/hostname"""
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    return (stdout)

def pretty_date_ago(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"
    
def pretty_date(given_date=False):
    from datetime import datetime
    if type(given_date) is int:
        dt = datetime.fromtimestamp(given_date)
    elif isinstance(given_date,datetime):
        dt = given_date
    elif not given_date:
        return ''
    return('{0}/{1} {2}h{3}'.format(str(dt.day).zfill(2), str(dt.month).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2)))
        
def datetime_to_timestamp(dt):
    """ 
    Return a timestamp(Int) from datetime object 
    Take care of Summer/Spring variation
    """
    if dt is None:
        return None
#    return int(time.mktime(dt.timetuple())*1000)
    return int(calendar.timegm(dt.timetuple())*1000)

def timestamp_to_datetime(ts):
    """ 
    Return a Datetime object from timestamp (Int) 
    """
    return time.mktime(ts.timetuple())

def timedelta_in_minute(dt_begin, dt_end):
    """Return the number of minutes between 2 dates"""
    ts_begin = time.mktime(dt_begin.timetuple())
    ts_end = time.mktime(dt_end.timetuple())

    # subtract values is in seconds then divide by 60 to get minutes.
    return int(ts_end - ts_begin) / 60
    
         
