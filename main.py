import os
from zhipuai import ZhipuAI

api_key = os.getenv("API_KEY")
client = ZhipuAI(api_key=api_key)
response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role": "user", "content": "你好！请介绍一下曹操"},
    ],
    stream=True,
)
for chunk in response:
    print(chunk.choices[0].delta)
