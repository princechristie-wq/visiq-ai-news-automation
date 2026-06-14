import os
from groq import Groq

client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)

print("Starting...")

topic_response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "Give one trending AI news topic. Return only the topic."
        }
    ]
)

topic = topic_response.choices[0].message.content.strip()

with open(
    "topic.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(topic)

print("Topic:", topic)
print("SUCCESS")
