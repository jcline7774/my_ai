import openai

openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = "<OPENROUTER_API_KEY>"

response = openai.ChatCompletion.create(
    model="openai/gpt-4o", messages=[...], max_tokens=512, temperature=0.7, top_p=1, n=1
)

reply = response.choices[0].message
