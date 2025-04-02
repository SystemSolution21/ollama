from typing import Any
from ollama import chat, ChatResponse
from pydantic import BaseModel
import pandas as pd
from gnews import GNews


# Fetch news articles
google_news: GNews = GNews()
news: Any | list[dict[str, Any]] | list[Any] = google_news.get_news(key="NVDA")

# Extract top 10 news titles
news_titles: list[str] = [article["title"] for article in news[:10]]
for title in news_titles:
    print(title)


# Define BaseModel for financial sentiment analysis as Structured Output
class FinancialSentimentAnalysis(BaseModel):
    sentiment: str
    future_looking: bool


# Initialize response store result
results: list[dict[str, Any]] = []

# Create llm to analyze news articles
# model: str = "llama3.2:3b"
# model: str = "openthinker:7b"
# model: str = "deepseek-r1:14b"
model: str = "gemma3:4b"

for title in news_titles:
    response: ChatResponse = chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": """You are a financial analyst expert. When analyzing headlines:
                - For future_looking, mark True if the headline:
                  * Makes predictions about future performance
                  * Discusses upcoming events or releases
                  * Contains words like 'will', 'expected', 'forecast', 'outlook', 'guidance'
                  * Mentions price targets or future valuations
                  * Discusses future market trends or opportunities
                - For sentiment, analyze based on:
                  * positive: bullish indicators, growth, achievements, upgrades
                  * negative: bearish indicators, declines, risks, downgrades
                  * neutral: factual reporting without clear positive/negative bias""",
            },
            {
                "role": "user",
                "content": f"""Analyze this financial headline: "{title}"
                
                Consider:
                1. Sentiment: Is it positive, negative, or neutral?
                2. Future-looking: Does it contain predictions, forecasts, or forward-looking statements about the stock's performance, company plans, or market outlook?
                
                Respond in JSON format matching the FinancialSentimentAnalysis schema.""",
            },
        ],
        format=FinancialSentimentAnalysis.model_json_schema(),
    )

    # Parse the response into financial sentiment analysis model
    financial_sentiment_analysis: FinancialSentimentAnalysis = (
        FinancialSentimentAnalysis.model_validate_json(
            json_data=response["message"]["content"]
        )
    )

    # Store the results
    results.append(
        {
            "title": title,
            "sentiment": financial_sentiment_analysis.sentiment,
            "future_looking": financial_sentiment_analysis.future_looking,
        }
    )

# Converts the results to DataFrame
df: pd.DataFrame = pd.DataFrame(data=results)
print(df)
