import streamlit as st  
import requests  
from nltk.sentiment import SentimentIntensityAnalyzer  
from gtts import gTTS  
import os  

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to fetch news from NewsAPI
def get_news(company):
    API_KEY = "aca1c572cc1c4319b9a54d1ff63cee36"  # Replace with your API Key
    url = f"https://newsapi.org/v2/everything?q={company}&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    
    response = requests.get(url)
    data = response.json()
    
    if "articles" in data:
        return data["articles"][:10]  # Return top 10 news articles
    else:
        return []

# Function to analyze sentiment
def analyze_sentiment(news_articles):
    sentiment_results = []
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    for article in news_articles:
        title = article["title"]
        sentiment_score = sia.polarity_scores(title)["compound"]

        if sentiment_score > 0:
            sentiment = "Positive"
            positive_count += 1
        elif sentiment_score < 0:
            sentiment = "Negative"
            negative_count += 1
        else:
            sentiment = "Neutral"
            neutral_count += 1

        sentiment_results.append({"Title": title, "Sentiment": sentiment, "Link": article["url"]})

    return sentiment_results, positive_count, negative_count, neutral_count

# Function to generate Hindi Text-to-Speech
def generate_hindi_tts(company, positive, negative, neutral):
    hindi_summary = f"Aaj {company} ke baare mein {positive} sakaratmak, {negative} nakaratmak, aur {neutral} madhyasth samachar hain."
    
    if positive > negative:
        hindi_summary += f" Kul milakar, {company} ke liye adhik sakaratmak samachar hain."
    elif negative > positive:
        hindi_summary += f" Chetavani! {company} ke liye adhik nakaratmak samachar hain."
    else:
        hindi_summary += f" Aaj {company} ke liye samaan roop se sakaratmak aur nakaratmak samachar hain."

    tts = gTTS(text=hindi_summary, lang='hi')
    tts.save("summary.mp3")
    return "summary.mp3"

# Streamlit Web App
st.title("News Sentiment Analysis App")  

# Ensure company_name is always defined
company_name = st.text_input("Enter Company Name (e.g., Tesla)").strip() or "Unknown"

# Debugging - Check if company_name is received correctly
st.write(f"Debug: You searched for news about {company_name}")  # This will always run

if company_name and company_name != "Unknown":  # Ensure user entered something
    if st.button("Analyze News"):
        news = get_news(company_name)

        if news:
            sentiment_data, pos_count, neg_count, neu_count = analyze_sentiment(news)

            st.subheader("News Articles & Sentiment")
            for item in sentiment_data:
                st.write(f"**{item['Title']}**")
                st.write(f"Sentiment: {item['Sentiment']}")
                st.write(f"[Read More]({item['Link']})")
                st.write("---")

            st.subheader("Sentiment Summary")
            st.write(f"Positive News: {pos_count}")
            st.write(f"Negative News: {neg_count}")
            st.write(f"Neutral News: {neu_count}")

            # Generate and Play Hindi TTS
            audio_file = generate_hindi_tts(company_name, pos_count, neg_count, neu_count)
            st.audio(audio_file)

            # Delete the audio file after playing
            os.remove(audio_file)
        else:
            st.write("No news found. Try a different company.")  
