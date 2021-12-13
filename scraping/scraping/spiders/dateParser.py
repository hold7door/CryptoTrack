from datetime import datetime

def get_month_index(month):
    month_idx_map = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12',
    }
    return month_idx_map[month]

def dateTimeFromString(publish_date):
    if 'at' in publish_date:
        the_date, the_time = publish_date.split(' at ')
        
        # Construct Date        
        month, date_num, year = the_date.split(' ')
        date_num = date_num.strip(',')
        if len(date_num) == 1:
            date_num = '0' + date_num
        month = get_month_index(month)

        # Construct Time
        the_time = the_time.strip(' UTC')
        tme, ampm = the_time.split(' ')
        hrs, mins = tme.split(':')
        # print(ampm)
        if ampm == 'p.m.' and 1 <= int(hrs) < 12:
            hrs = str(int(hrs) + 12)
        if len(hrs) == 1:
            hrs = '0' + hrs
        # print(publish_date)
        # print(f'{year}-{month}-{date_num}T{hrs}:{mins}:00')
        dt = datetime.fromisoformat(f'{year}-{month}-{date_num}T{hrs}:{mins}:00')
        return dt

def getHoursDiff(d1, d2):
    hours = (d2 - d1).total_seconds() // (60 * 60)
    # print(d1, hours)
    return hours
