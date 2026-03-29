from openai import OpenAI

# 🔴 Replace with your OpenRouter API key
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


class Chatbot:
    def __init__(self):
        self.chat_history = []

    def build_prompt(self, user_input):
        system_prompt = """
You are a helpful AI assistant.

Rules:
- Use previous conversation for context
- Do NOT repeat the same answer
- If unsure, ask clarification
- Give clear and simple answers
"""

        messages = [{"role": "system", "content": system_prompt}]

        # Last 5 messages for context
        for msg in self.chat_history[-5:]:
            messages.append(msg)

        messages.append({"role": "user", "content": user_input})

        return messages

    def get_response(self, user_input):
        messages = self.build_prompt(user_input)

        response = client.chat.completions.create(
            model="openrouter/free",  # ✅ FREE WORKING MODEL
            messages=messages,
            temperature=0.7
        )

        reply = response.choices[0].message.content

        # 🔁 Avoid repetition
        if len(self.chat_history) > 1:
            last_reply = self.chat_history[-1]["content"]
            if reply == last_reply:
                reply = "Let me explain it differently: " + reply

        # 💾 Save memory
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append({"role": "assistant", "content": reply})

        # ✂️ Token optimization (keep last 10 messages)
        self.chat_history = self.chat_history[-10:]

        return reply