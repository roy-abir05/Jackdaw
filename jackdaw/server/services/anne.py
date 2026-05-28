import json
from openai import OpenAI
from jackdaw.config import ConfigManager

class AnneEngine:
    @staticmethod
    def generate_captains_log(dashboard_data: dict) -> dict:
        """
        Takes the raw JSON data from Coral and asks Anne to analyze it 
        using the LLM provider designated in the local configuration.
        """
        # Load user configurations dynamically
        config = ConfigManager.load_config()
        ai_config = config.get("ai", {})
        
        # Spin up our flexible OpenAI-compatible client
        client = OpenAI(
            api_key=ai_config.get("api_key", "dummy-key"),
            base_url=ai_config.get("base_url", "https://api.groq.com/openai/v1")
        )

        prompt = f"""
        You are 'Anne', the data analyst and chief strategist for a solo developer product.
        Review the following JSON data pulled from their SaaS infrastructure.
        
        DATA:
        {json.dumps(dashboard_data, indent=2)}
        
        Provide a short, punchy 'Captain's Log' summarizing the state of the SaaS.
        Do NOT use cheesy pirate gimmicks or over-the-top puns. Be highly professional, concise, and analytical.
        
        Return the result as a raw JSON object with two keys exactly:
        - "summary": A 2-sentence overview.
        - "insight": One specific operational recommendation based on the data.
        """

        try:
            response = client.chat.completions.create(
                model=ai_config.get("model", "llama3-8b-8192"),
                messages=[
                    {"role": "system", "content": "You output strictly valid JSON. No markdown formatting, no preamble."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
            )
            
            ai_text = response.choices[0].message.content
            return json.loads(ai_text)
            
        except Exception as e:
            print(f"Anne Generation Failed: {e}")
            return {
                "summary": "Anne is offline resting at Nassau. Log unavailable.",
                "insight": f"Check your configuration keys or local LLM engine status. Details: {str(e)}"
            }
        
    @staticmethod
    def write_sql(user_question: str, schema_data: list) -> str:
        """
        Translates a natural language question into Coral SQL using Schema Injection.
        """
        config = ConfigManager.load_config()
        ai_config = config.get("ai", {})
        
        # Pull the user's active GitHub target so the AI knows what to query
        gh_config = config.get("sources", {}).get("github", {})
        gh_owner = gh_config.get("owner", "withcoral")
        gh_repo = gh_config.get("repo", "coral")
        
        client = OpenAI(
            api_key=ai_config.get("api_key", "dummy-key"),
            base_url=ai_config.get("base_url", "https://api.groq.com/openai/v1")
        )

        prompt = f"""
        You are 'Anne', an expert SQL data analyst.
        Translate the user's question into a single, valid Coral SQL query.
        
        CRITICAL SCHEMA KNOWLEDGE (USE ONLY THESE COLUMNS):
        1. `stripe.charges`
           - Columns: `id`, `amount` (in cents), `customer` (customer ID, e.g., cus_123), `created` (unix timestamp), `description`.
           - Note: Divide amount by 100.0 to get USD.
        
        2. `stripe.customers`
           - Columns: `id`, `name`, `email`, `created`.
           - Note: Join with stripe.charges ON stripe.charges.customer = stripe.customers.id
           
        3. `github.commits`
           - Columns: `sha` (commit hash), `commit__author__name`, `commit__author__date`, `commit__message`.
           - CRITICAL RULE: Every query to github.commits MUST include exactly: 
             WHERE owner = '{gh_owner}' AND repo = '{gh_repo}'
        
        USER QUESTION: "{user_question}"
        
        RULES:
        1. Output ONLY the raw SQL query. No explanations, no greetings.
        2. Do NOT wrap the output in markdown (do NOT use ```sql).
        3. Always use LIMIT 15 to prevent terminal overflow.
        """

        try:
            response = client.chat.completions.create(
                model=ai_config.get("model", "llama-3.3-70b-versatile"),
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0, # 0.0 is critical for code generation!
            )
            
            sql = response.choices[0].message.content.strip()
            # Failsafe cleanup just in case the LLM ignores the markdown rule
            sql = sql.replace("```sql", "").replace("```", "").strip()
            return sql
            
        except Exception as e:
            return f"-- Error generating SQL: {str(e)}"