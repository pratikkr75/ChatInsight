import re
import pandas as pd
from textblob import TextBlob

def preprocess(data):
    # Regular expression pattern
    pattern = re.compile(r'(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s?[ap]m) - (.*)')

    # Find all matches
    matches = re.findall(pattern, data)

    # Create a DataFrame with columns in the desired order
    df = pd.DataFrame(matches, columns=['message_date', 'user_message'])

    # Convert message_date to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p')

    # Rearrange columns to have 'user_message' first and 'message_date' second
    df = df[['user_message', 'message_date']]

    # separate users and messages
    users = []
    messages = []

    # for sentiment analysis
    polarities = []
    subjectivities = []
    sentiments = []

    #contacts
    contacts = []

    for message in df['user_message']:
        entry = re.split(r'([^:]+):\s', message)
        if len(entry) > 2:  # user name and message are present
            users.append(entry[1].strip())
            messages.append(entry[2].strip())
        else:
            users.append('group notification')
            messages.append(entry[0].strip())

        # Perform sentiment analysis
        analysis = TextBlob(messages[-1])
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        polarities.append(polarity)
        subjectivities.append(subjectivity)

        if polarity > 0:
            sentiments.append("positive")
        elif polarity < 0:
            sentiments.append("negative")
        else:
            sentiments.append("neutral")

        #extract phone numbers
        phone_pattern = re.compile(r'\+?\d{10,}')  # Regular expression pattern for phone numbers
        contacts.extend(re.findall(phone_pattern, message))

    # Add new columns to the DataFrame
    df['user'] = users
    df['message'] = messages
    df['polarity'] = polarities
    df['subjectivity'] = subjectivities
    df['sentiment'] = sentiments

    # Drop the old 'user_message' column
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['message_date'].dt.date
    df['year'] = df['message_date'].dt.year
    df['month_num'] = df['message_date'].dt.month
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.day_name()
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

def extract_contacts_from_messages(messages):
    contacts = []
    phone_pattern = re.compile(r'\+?\d{10,}')  # Regular expression pattern for phone numbers

    for message in messages:
        contacts.extend(re.findall(phone_pattern, message))

    return contacts