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
        config = ConfigManager.get_full_context()
        
        user_config = config.get("user", {})
        ai_config = user_config.get("ai", {})
        
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
    def write_sql(user_question: str, active_schema: list) -> str:
        """
        Translates a natural language question into Coral SQL dynamically using the config dotfiles.
        """
        config = ConfigManager.get_full_context()
        
        user_config = config.get("user", {})
        ai_config = user_config.get("ai", {})
        gh_config = user_config.get("workspaces", {}).get(user_config.get("jackdaw", {}).get("active_workspace", "default"), {})
        
        system_sql_prompt = config.get("prompts", {}).get("system", "Output only valid SQL.")
        
        # FIX 1: "schemas" must be plural to match ConfigManager
        schema_rules = config.get("schemas", {})
        injected_schema = ""
        
        for source, tables in schema_rules.items():
            for table, rules in tables.items():
                formatted_rules = rules.format(
                    gh_owner=gh_config.get("owner", "withcoral"),
                    gh_repo=gh_config.get("repo", "coral")
                )
                injected_schema += f"- {source}.{table}: {formatted_rules}\n"

        client = OpenAI(
            api_key=ai_config.get("api_key", "dummy-key"),
            # FIX 2: Stripped the markdown link formatting
            base_url=ai_config.get("base_url", "https://api.groq.com/openai/v1")
        )

        final_prompt = f"""
        {system_sql_prompt}
        
        CRITICAL SCHEMA KNOWLEDGE:
        {injected_schema}
        
        USER QUESTION: "{user_question}"
        """

        try:
            response = client.chat.completions.create(
                model=ai_config.get("model", "llama-3.3-70b-versatile"),
                messages=[{"role": "user", "content": final_prompt}],
                temperature=0.0, 
            )
            
            sql = response.choices[0].message.content.strip()
            sql = sql.replace("```sql", "").replace("```", "").strip()
            return sql
            
        except Exception as e:
            return f"-- Error generating SQL: {str(e)}"