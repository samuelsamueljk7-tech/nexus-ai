from ollama import chat

MODEL = "gemma3:1b"

SYSTEM_PROMPT = """
You are Spark, a personal AI assistant running locally on Windows.

Your job is to help the user with their computer and answer questions.
Be friendly, concise, and practical.

For now, you cannot directly control the computer.
Do not pretend that you performed an action when you have not.
"""

print("=" * 40)
print("        SPARK IS ONLINE")
print("        LOCAL AI MODE")
print("=" * 40)

while True:
    try:
        command = input("\nYou: ").strip()

        if not command:
            continue

        if command.lower() in ["exit", "quit", "bye"]:
            print("Spark: Shutting down. 👋")
            break

        response = chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": command
                }
            ]
        )

        print("\nSpark:", response.message.content)

    except KeyboardInterrupt:
        print("\nSpark: Shutting down. 👋")
        break

    except Exception as e:
        print("\nSpark error:", e)