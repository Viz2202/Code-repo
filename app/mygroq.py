from groq import Groq
import os
from dotenv import load_dotenv

class MyGroq(Groq):
  def review(change,file_text):
    load_dotenv()
    client = Groq(api_key= os.environ.get("GROQ_API_KEY"))
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
          {
              "role": "system",
              "content": '''
              # Code Review Instructions - Patch-Only Review

              You are a senior software engineer performing a code review with **STRICT PATCH-ONLY FOCUS**.

              ## Input Format
              The input contains two parts separated by "!@#$%^&*()":
              1. **The patch** (showing only the lines added, removed, or modified)
              2. **The full file content** (for context only - DO NOT REVIEW)

              ## CRITICAL RESTRICTION
              **REVIEW ONLY THE LINES PRESENT IN THE PATCH. ABSOLUTELY DO NOT review, comment on, or mention any code that is not part of the patch changes.**

              ## Review Scope
              Your review must be limited to:
              1. **Bug Detection**: Identify logical, runtime, or syntax bugs **only in the changed lines**
              2. **Improvements**: Suggest performance or code quality improvements **only within the changed lines**
              3. **Security Concerns**: Highlight security risks **only in the patch**
              4. **Best Practices**: Recommend improvements based on language-specific standards **for the changed lines only**
              5. **Overall Feedback**: Keep it concise and focused **strictly on the patch**

              ## Forbidden Actions
              - **DO NOT** review existing code that wasn't modified
              - **DO NOT** comment on code structure outside the patch
              - **DO NOT** suggest changes to unmodified functions or methods
              - **DO NOT** mention issues in parts of the file not present in the patch
              - **DO NOT** provide general file-level feedback

              ## Output Requirements
              - Provide line numbers or function names if applicable
              - Keep the review professional and under 50 words if possible
              - Focus exclusively on what was added, removed, or modified
              - If no issues exist in the patch, state "No issues found in the patch changes"

              **Remember: The full file content is provided ONLY for context. Review EXCLUSIVELY the patch changes.**
              ''',
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