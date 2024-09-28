import emoji.unicode_codes
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
import emoji
import matplotlib.pyplot as plt
import pandas as pd





def fetch_data(dataframe, user):
    
    if user != 'Everyone':
        dataframe = dataframe[dataframe['user'] == user] 
        
    # 1. Get number of messages
    num_messages = dataframe.shape[0]
    
    # 2. Get number of words
    num_words = []
    for message in dataframe['message']:
        
        if message.startswith('https') or message.startswith('<Media omitted>'):
            continue
        
        else:
            num_words.extend(message.split())
            
    # 3. Get number of characters
    num_characters = sum(len(word) for word in num_words)
            
    # 4. Get number of media
    num_media = dataframe[dataframe['message'] == '<Media omitted>\n'].shape[0] 
    
    # 5. Get most active user
    user_activity = dataframe['user'].value_counts()
    most_active_user = user_activity.index[0]
                
    # 6. Get number of links
    num_links = dataframe['message'].str.startswith(('http://', 'https://', 'www.')).sum()  
            
    # Return data        
    return num_messages, len(num_words), num_characters, num_media, most_active_user, num_links
        
        
def fetch_active_user_graph(dataframe):
    people = dataframe['user'].value_counts().head()
    x = dataframe['user'].value_counts()
    
    index = x.index
    values = x.values
    
    return people, x, index, values


def fetch_characters(dataframe):
    dataframe = dataframe[~dataframe.isin(['<Media omitted>\n', emoji.EMOJI_DATA])]
    
    characters_data = dataframe.groupby('user')['message'].agg(lambda x: x.str.replace(r'\s+', '', regex=True).str.len().sum()).reset_index()
    characters_data = characters_data.sort_values(by='message', ascending=False).head()
    
    return characters_data


def create_worldcloud(dataframe, user):
    if user != 'Everyone':
        dataframe = dataframe[dataframe['user'] == user] 
    
    dataframe = dataframe[dataframe['message'] != '<Media omitted>\n']
    
    # WordCloud
    stopwords = set(STOPWORDS)
    
    wc = WordCloud(width=400, height=400, min_font_size = 10, background_color ='white', stopwords=stopwords)
    wc = wc.generate(dataframe['message'].str.lower().str.cat(sep=' '))
    
    plt.axis('off')
    plt.imshow(wc)
    
    # Word Count
    words = []
    
    for message in dataframe['message']:
        for word in message.split():
            if word.lower() in stopwords:
                continue
                
            else: 
                words.append(word.lower())
                
    words = pd.DataFrame(Counter(words).most_common(10)).rename(columns={0: 'Word', 1: 'Count'})

    return plt, words
            
        
def fetch_media_graph(dataframe):
    
    media_df = dataframe[dataframe['message'] == '<Media omitted>\n']['user'].value_counts().head()
    media_df = pd.DataFrame(media_df)
 
    media_people = media_df.index
    media_count = media_df.values
    
    return media_df, media_people, media_count 
    
    
def fetch_emoji_graph(dataframe, user):
    if user != 'Everyone':
        dataframe = dataframe[dataframe['user'] == user] 
                
    emojis = []
    for message in dataframe['message']:
        emojis.extend([w for w in message if w in emoji.EMOJI_DATA])             
                
    emoji_df = pd.DataFrame(Counter(emojis).most_common(10))
    emoji_df = emoji_df.rename(columns={0: 'Emoji', 1: 'Count'})
    
    return emoji_df


def fetch_trend_data(dataframe, user):
    if user != 'Everyone':
        dataframe = dataframe[dataframe['user'] == user] 

    timeline = dataframe.groupby(['year', 'month_num', 'month'])['message'].count().reset_index()
    time = []

    for i in range(timeline.shape[0]):
        time.append(f"{timeline['month_num'][i]}-{timeline['year'][i]}")
        
    timeline['time'] = time

    month_order = ['January', 'February', 'March', 'April', 'May', 
                'June', 'July', 'August', 'September', 'October', 
                'November', 'December']

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    month_df = dataframe.groupby(['month'])['message'].count().reset_index()
    month_df['month'] = pd.Categorical(month_df['month'], categories=month_order, ordered=True)
    month_df = month_df.sort_values('month')

    day_df = dataframe.groupby(['day'])['message'].count().reset_index()
    day_df['day'] = pd.Categorical(day_df['day'], categories=day_order, ordered=True)
    day_df = day_df.sort_values('day')

        
    return timeline, month_df, day_df


def fetch_activity_data(dataframe):
    
   
    
    return dataframe