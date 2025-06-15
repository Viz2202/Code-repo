from groq import Groq
import os
from dotenv import load_dotenv

class MyGroq(Groq):
  def review(file_text):
    load_dotenv()
    client = Groq(api_key= os.environ.get("GROQ_API_KEY"))
    completion = client.chat.completions.create(
        model="mistral-saba-24b",
        messages=[
          {
              "role": "system",
              "content": '''You are a senior software engineer performing a code review.
              Please review the following code and provide:
              1. Bug Detection: Identify potential logical or runtime bugs and look for syntax errors.
              2. Improvements: Suggest code quality or performance improvements.
              3. Security Concerns: Highlight any security vulnerabilities.
              4. Best Practices: Recommend changes based on language-specific best practices.
              5. Overall Feedback: General comments on design, style, and readability.
              Include line numbers or function names in your feedback when applicable.
              Respond in a structured and professional tone and make it concise(if possible 50 words or less).
              '''
          },
          {
            "role": "user",
            "content": file_text
          }
        ],
        temperature=0.6,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    reviews=[]
    for chunk in completion:
        reviewing=chunk.choices[0].delta.content or ""
        reviews.append(reviewing)
    return reviews