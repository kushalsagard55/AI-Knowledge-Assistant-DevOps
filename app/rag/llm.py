from google import genai

from app.core.settings import settings


print("=" * 60)
print("Gemini Model :", repr(settings.gemini_model))
print("API Key      :", settings.gemini_api_key[:10] + "...")
print("=" * 60)


client = genai.Client(
    api_key=settings.gemini_api_key
)


def ask_llm(question: str, context: str):

    prompt = f"""
You are an AI Knowledge Assistant.

Answer ONLY from the provided context.

If the answer is not available in the context, reply with:
"I don't know based on the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="models/gemini-3.5-flash",
        contents=prompt,
    )

    if response.text:
        return response.text

    return "No response received from Gemini."