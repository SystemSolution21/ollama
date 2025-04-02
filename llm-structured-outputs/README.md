Example shows how to:

1. Fetch real-time news headlines about stocks (NVDA) using GNews
2. Process each headline through an LLM to analyze two key aspects:
   - Financial sentiment (positive/negative/neutral)
   - Future outlook indicator (True/False)
3. Use structured output with Pydantic models to ensure consistent formatting:
   ```python
   class FinancialSentimentAnalysis(BaseModel):
       sentiment: str
       future_looking: bool
   ```
4. LLM makes decisions based on predefined criteria:
   - Sentiment analysis looks for bullish/bearish indicators
   - Future-looking detection checks for predictions, forecasts, and forward-looking statements
5. Results are organized into a pandas DataFrame for further analysis

This demonstrates how to combine LLMs with structured data processing for automated financial news analysis.

# Different models available:

model: str = "llama3.2:3b" # Smaller, faster, but less accurate
model: str = "openthinker:7b" # Medium size, balanced
model: str = "deepseek-r1:14b"# Larger, slower but more accurate
model: str = "gemma3:4b" # Google's model, good for specific tasks
