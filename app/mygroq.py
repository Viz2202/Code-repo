from groq import Groq
import os
from dotenv import load_dotenv

class MyGroq(Groq):
  def review(change,file_text):
    load_dotenv()
    client = Groq(api_key= os.environ.get("GROQ_API_KEY"))
    completion = client.chat.completions.create(
        model="mistral-saba-24b",
        messages=[
          {
              "role": "system",
              "content": '''You are a senior software engineer performing a code review.
              The input contains two parts separated by "!@#$%^&*()":
              1. The patch (showing only the lines added, removed, or modified).
              2. The full file content for context.
              Please review only the lines present in the patch. Ignore issues which are not present in patch. Your review should include:
              1. Bug Detection: Identify logical, runtime, or syntax bugs in the changed lines.
              2. Improvements: Suggest improvements in performance or code quality within the changed lines.
              3. Security Concerns: Highlight security risks in the patch if any.
              4. Best Practices: Recommend improvements based on language-specific standards for only the changed lines.
              5. Overall Feedback: Keep it concise and focused strictly on the patch.
              Provide line numbers or function names if applicable. Keep the review professional and under 50 words if possible.
              review ONLY the lines PRESENT in the PATCH.'''
          },
          {
            "role": "user",
            "content": change + "!@#$%^&*()" + file_text
          }
        ],
        temperature=0.1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    reviews=""
    for chunk in completion:
        reviewing=chunk.choices[0].delta.content or ""
        reviews+=reviewing
    return reviews