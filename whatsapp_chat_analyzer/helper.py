from urlextract import URLExtract
extract = URLExtract()

from wordcloud import WordCloud
import pandas as pd
from collections import Counter
def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for msg in df['message']:
        words.extend(msg.split())

    num_media_message = df[df['message'] == '<Media omitted>'].shape[0]

    links=[]
    for msg in df['message']:
        links.extend(extract.find_urls(msg))

    return num_messages, len(words),num_media_message,len(links)



def fetch_most_busy_users(df):
    y = df['user'].value_counts().head(6)

    for i, j in y.items():
        if i == "Group":
            y.drop(i, inplace=True)

    y = y[:5]

    df = round((df['user'].value_counts() / df['message'].shape[0]) * 100, 2).reset_index().rename(
        columns={'count': 'Percent', 'user': 'Name'})
    return y,df

def create_wordcloud(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'Group') & (df['message'] != '<Media omitted>') & (
            df['message'] != 'This message was deleted')]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc


def most_common_words(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'Group') & (df['message'] != '<Media omitted>') & (
                df['message'] != 'This message was deleted')]

    words = []
    for i in temp['message']:
        words.extend(i.lower().split())

    most_common_word_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_word_df


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['only_date'] = df['date'].dt.date

    timeline = df.groupby('only_date').count()['message'].reset_index()

    return timeline


def week_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_heatmap