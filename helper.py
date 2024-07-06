import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import re
import emoji
extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Fetch number of messages
    num_messages = df.shape[0]

    # Fetch total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # Fetch number of urls shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    percent_of_messages_each_user = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'user', 'count': 'percent'}
    )
    return x, percent_of_messages_each_user

def create_wordcload(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notification']
    temp = temp[~temp['message'].str.contains('<Media omitted>', na=False)]

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            # Remove numbers and symbols using regex
            word = re.sub(r'[^a-zA-Z]', '', word)
            if word and word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()


    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notification']
    temp = temp[~temp['message'].str.contains('<Media omitted>', na=False)]

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            # Remove symbols but keep phone numbers (e.g., +1234567890)
            if re.match(r'^\+?[0-9]{10,15}$', word):  # Match phone numbers
                words.append(word)
            else:
                # Remove numbers and symbols from other words
                word = re.sub(r'[^a-zA-Z]', '', word)
                if word and word not in stop_words:
                    words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # Create a new 'time' column combining 'month' and 'year'
    # timeline['time'] = timeline.apply(lambda row: f"{row['month']}-{row['year']}", axis=1)

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return  timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


def sentiment_analysis(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    average_polarity = df['polarity'].mean()
    average_subjectivity = df['subjectivity'].mean()

    sentiment_counts = df['sentiment'].value_counts()
    positive_count = sentiment_counts.get('positive', 0)
    negative_count = sentiment_counts.get('negative', 0)

    if positive_count > negative_count:
        overall_sentiment = "positive"
    elif negative_count > positive_count:
        overall_sentiment = "negative"
    else:
        overall_sentiment = "neutral"

    return average_polarity, average_subjectivity, overall_sentiment


