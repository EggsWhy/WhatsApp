import re
import datetime
import pandas as pd


def transform(data):
    
    # the pattern to split the data into just user messages
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[APMapm]{2})?\s-\s'

    # Gets all the user messages ([1:] is just because without it there is an empty string)
    messages = re.split(pattern, data)[1:]

    # basically finds all the dates
    dates = re.findall(pattern, data)

    # Converting to DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    # Converting Date Format
    if 'AM' in dates[0].upper() or 'PM' in dates[0].upper():
        # Convert using 12-hour format
        df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%Y, %I:%M %p - ", errors='coerce')
            
    else:
        # Convert using 24-hour format
        df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%Y, %H:%M - ", errors='coerce')
    
    df.rename(columns={'message_date': 'date'}, inplace=True)


    # Splitting user and message
    users = []
    messages = []

    for message in df['user_message']:
        
        # This splits the message into (user) and (message)
        entry = re.split(r'([\w\W]+?):\s', message)
            
        if entry[1:]: # Basically if length more than 1
            users.append(entry[1])
            messages.append(entry[2])
            
        else:
            users.append('whatsapp notifcation')
            messages.append(entry[0])
        
        
    df['user'] = users
    df['message'] = messages
    df = df.drop('user_message', axis=1)


    # Adding datetime columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day_name()
    df['day_num'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    return df

