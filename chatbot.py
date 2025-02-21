import openai
import os
from dotenv import load_dotenv

# Load OpenAI API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def generate_questions(tech_stack):
    """
    Generates interview questions based on the candidate's tech stack.

    Args:
        tech_stack (list): A list of technologies (e.g., ['Python', 'Django']).

    Returns:
        str: Cleaned interview questions as plain text with a single dash notation.
    """
    if not tech_stack:
        return "Please enter a tech stack to generate questions."
    
    try:
        prompt = f"Generate 3-5 interview questions for a candidate skilled in {', '.join(tech_stack)}. Do not include numbering, bullets, or special formatting."

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )

        raw_text = response["choices"][0]["message"]["content"]
        
        # Format each line with a dash "-" before it
        cleaned_text = "\n\n".join([f"- {line.lstrip('1234567890.- ')}" for line in raw_text.split("\n") if line.strip()])

        return cleaned_text
    
    except Exception as e:
        return f"Error generating questions: {str(e)}"
