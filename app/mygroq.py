from groq import Groq
import os
from dotenv import load_dotenv

class MyGroq:

    @staticmethod
    def review(change, file_text):
        load_dotenv()

        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        prompt = f"""
PATCH
-----
{change}

FULL_FILE_CONTEXT
-----------------
{file_text}
"""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are a senior engineer reviewing a code PATCH.

                                  Input contains:
                                  LANGUAGE
                                  PATCH (changed lines)
                                  FULL_FILE_CONTEXT (context only)

                                  Review ONLY PATCH.

                                  Check for:
                                  - syntax errors
                                  - bugs
                                  - security issues
                                  - small improvements

                                  Do NOT review code outside PATCH.

                                  Output format:

                                  Line <line_number>: <issue>
                                  Fix: <corrected line>

                                  Corrected Patch:
                                  ```<language>
                                  <fixed patch>

                                  If no issues:
                                  No issues found in the patch changes.
                                  """
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_completion_tokens=512,
            stream=True
        )

        review = ""
        for chunk in completion:
            part = chunk.choices[0].delta.content or ""
            review += part

        return review