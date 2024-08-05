# ChatInsight - WhatsApp Chat Analyzer

This Streamlit-based WhatsApp Chat Analyzer provides detailed insights into WhatsApp chat data. It includes various analytical tools and visualizations such as sentiment analysis, activity timelines, emoji analysis, and more.

## Key Features

- **Message Statistics:** Displays the number of messages, total words, media shared, and links shared.
- **Sentiment Analysis:** Provides average sentiment polarity and subjectivity, along with overall sentiment.
- **Timelines:** Visualizes chat activity over time, including monthly, daily, and weekly timelines.
- **Activity Maps:** Shows the most active days and months and a weekly activity heatmap.
- **User Analysis:** Identifies the most active users in group chats and provides a word cloud and common words analysis.
- **Contact Analysis:** Extracts and displays contact information from messages.
- **Emoji Analysis:** Analyzes and visualizes emoji usage.

## Libraries and Technologies

- **Streamlit:** For building the interactive web app.
- **Matplotlib:** For creating visualizations and plots.
- **Seaborn:** For advanced data visualization.
- **Pandas:** For data manipulation and analysis.
- **Urlextract:** For extracting URLs from messages.
- **WordCloud:** For generating word clouds.
- **TextBlob:** For sentiment analysis.
- **Emoji:** For emoji analysis.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/whatsapp-chat-analyzer.git
   cd whatsapp-chat-analyzer
   pip install -r requirements.txt
   streamlit run app.py

## Usage

1. **Upload a File:**
   Use the file uploader in the sidebar to choose a WhatsApp chat export file.

2. **Select a User:**
   Choose a user from the dropdown menu to analyze or select "Overall" to view group-level statistics.

3. **Show Analysis:**
   Click the "Show Analysis" button to generate and display various analytical insights and visualizations.

## Files

- `app.py`: Main Streamlit application file.
- `preprocessor.py`: Contains functions for preprocessing chat data.
- `helper.py`: Contains helper functions for data analysis and visualization.
- `stop_hinglish.txt`: File containing stop words for word cloud generation.
- `requirements.txt`: List of required Python packages.

## Example Output

- **Statistics:** Number of messages, total words, media, and links.
- **Sentiment Analysis:** Average polarity and subjectivity.
- **Timelines:** Monthly, daily, and weekly activity plots.
- **Activity Maps:** Most active days and months, heatmap of weekly activity.
- **User Analysis:** Most active users, word cloud, and common words.
- **Contact Analysis:** Extracted contact information.
- **Emoji Analysis:** Visual representation of emoji usage.

