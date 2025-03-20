import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import json
from gtts import gTTS
import os
from deep_translator import GoogleTranslator
from flask import Flask, jsonify, request, send_file

app = Flask(__name__)

def fetch_news(company):
    search_url = f"https://www.bing.com/news/search?q={company}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(search_url, headers=headers, timeout=10)
    if response.status_code != 200:
        return {"error": f"Failed to fetch news. Status code: {response.status_code}"}

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("div.t_t, div.news-card")
    if not articles:
        return {"error": "No articles found."}

    sentiment_scores = {"Positive": 0, "Negative": 0, "Neutral": 0}
    articles_data = []
    translator = GoogleTranslator(source='en', target='hi')

    for article in articles[:5]:  # Limit to 5 articles
        title_tag = article.select_one("a.title, a")
        title = title_tag.text.strip() if title_tag else ""  # ✅ Keep empty title instead of "No Title"
        snippet_tag = article.select_one("div.snippet, div.snpt")
        snippet = snippet_tag.text.strip() if snippet_tag else "No Content"  # ✅ Keep "No Content" for missing summaries

        sentiment = TextBlob(snippet).sentiment.polarity
        sentiment_category = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
        sentiment_scores[sentiment_category] += 1

        articles_data.append({
            "Title": title,
            "Summary": snippet,  # ✅ Keep English summary
            "Sentiment": sentiment_category
        })

    final_analysis = f"Based on recent news, the sentiment about {company} is mostly {'positive' if sentiment_scores['Positive'] > sentiment_scores['Negative'] else 'mixed'}."

    result = {
        "Company": company,
        "Articles": articles_data,
        "Sentiment Scores": sentiment_scores,
        "Final Analysis": final_analysis
    }

    return result

@app.route('/news', methods=['GET'])
def get_news():
    company = request.args.get('company', 'Tesla')
    result = fetch_news(company)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
