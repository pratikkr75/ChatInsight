import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import pandas as pd
from collections import Counter

st.sidebar.title("Whatsapp Chat Analyzer")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group notification' in user_list:
        user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        #stats area
        num_messages, words, num_media_messages, num_of_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_of_links)

        # Sentiment analysis
        st.title("Sentiment Analysis")
        average_polarity, average_subjectivity, overall_sentiment = helper.sentiment_analysis(selected_user, df)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("Average Polarity")
            st.write(average_polarity)

        with col2:
            st.header("Average Subjectivity")
            st.write(average_subjectivity)

        with col3:
            st.header("Overall Sentiment")
            st.write(overall_sentiment)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # weekly activity timeline
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        #find busiest users in group(group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, percent_of_messages_each_user = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            # Assign different colors to each bar
            colors = cm.rainbow([i / len(x) for i in range(len(x))])
            ax.bar(x.index, x.values, color=colors)

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color=colors)
                plt.xticks(rotation=45)
                st.pyplot(fig)
            with col2:
                st.dataframe(percent_of_messages_each_user)

        # WordCloud
        st.title("WordCloud")
        df_wc = helper.create_wordcload(selected_user, df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation=90)
        st.title('Most common Words')
        st.pyplot(fig)

        # extract contacts
        st.title("Contact Analysis")
        contacts = preprocessor.extract_contacts_from_messages(df[df['user'] == selected_user]['message'])
        contact_counts = Counter(contacts)
        total_contacts = len(contacts)

        if contact_counts:
            st.write(f"Total Contacts: {total_contacts}")
            st.write("Top Contacts:")
            st.write(pd.DataFrame(contact_counts.most_common(), columns=['Contact', 'Frequency']))
        else:
            st.write("No contacts found in the selected user's messages.")

        #emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)