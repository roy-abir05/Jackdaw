import os
import json
from openai import OpenAI

# The beauty of this setup: 
# If a user wants Groq, base_url="https://api.groq.com/openai/v1"
# If a user wants local Ollama, base_url="http://localhost:11434/v1"
# We will pull these from config.toml later, but we will hardcode Groq for today.

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY", "dummy-key-for-local"),
    base_url="https://api.groq.com/openai/v1" 
)

class FirstMate:
    @staticmethod
    def generate_captains_log(dashboard_data: dict) -> dict:
        prompt = f"""
        You are 'Adéwalé', the First Mate and data analyst for a solo developer.
        Review the following JSON data pulled from their SaaS infrastructure.
        
        DATA:
        {json.dumps(dashboard_data, indent=2)}
        
        Provide a short, punchy 'Captain's Log' summarizing the state of the ship (the SaaS).
        Do NOT use cheesy pirate gimmicks or puns. Be highly professional, concise, and analytical.
        
        Return the result as a raw JSON object with two keys exactly:
        - "summary": A 2-sentence overview.
        - "insight": One specific operational recommendation based on the data.
        """

        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192", # Extremely fast, free Groq model
                messages=[
                    {"role": "system", "content": "You output strictly valid JSON. No markdown formatting, no preamble."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}, # Forces guaranteed JSON output
                temperature=0.2,
            )
            
            ai_text = response.choices[0].message.content
            return json.loads(ai_text)
            
        except Exception as e:
            print(f"AI Generation Failed: {e}")
            return {
                "summary": "AI systems offline. Captain's log unavailable.",
                "insight": "Check API keys and network connection."
            }