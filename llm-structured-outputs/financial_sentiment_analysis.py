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
model: str = "llama3.2:3b"
model: str = "openthinker:7b"
model: str = "gemma3:4b"
model: str = "deepseek-r1:14b"

for title in news_titles:
    response: ChatResponse = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": f"""Analyze the following title for sentiment (positive, negative or neutral)
                            and whether it provides future-looking financial insight, predictions or 
                            guidance on whether to buy/sell/hold the stock (True or False): {title}) 
                                """,
            }
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
df: pd.DataFrame = pd.DataFrame(results)
print(df)
