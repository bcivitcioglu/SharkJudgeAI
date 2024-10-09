import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Mistral API configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

def judge_project(description):
    prompt = f"""
    You are SharkJudgeAI, an AI judge for evaluating student project ideas. Your task is to:
    1. Roast the project idea humorously but constructively.
    2. Provide a score out of 10.
    3. Give brief suggestions for improvement.

    Here's the project description to evaluate:

    {description}

    Please provide your judgment.
    """

    data = {
        "model": "mistral-tiny",  # You can change this to other available models
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }

    response = requests.post(MISTRAL_API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    print("Welcome to SharkJudgeAI!")
    print("Please enter the student's project description (type 'END' on a new line when finished):")
    
    description_lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        description_lines.append(line)
    
    description = "\n".join(description_lines)
    
    judgment = judge_project(description)
    print("\nSharkJudgeAI's Judgment:")
    print(judgment)

if __name__ == "__main__":
    main()
