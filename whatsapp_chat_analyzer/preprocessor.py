import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format="%m/%d/%y, %H:%M - ")

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for msg in df['user_message']:
        match = re.search(r'^([^:]+):(.*)', msg)
        if match:
            name = match.group(1).strip()
            users.append(name)

            cont = match.group(2).strip()
            messages.append(cont)
        else:
            users.append("Group")
            messages.append(msg)

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['day_name'] = df['date'].dt.day_name()

    period = []

    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period

    return df