from pydantic import BaseModel
from ollama import chat

# Step 1: Define the Pydantic model for structured response
class CodeExplanation(BaseModel):
    code_explanation: str

# Step 2: Build a reusable class to handle structured chat interactions
class CodeAnalyzer:
    def __init__(self, model_name: str, temperature: float = 0):
        self.model_name = model_name
        self.temperature = temperature

    def get_user_prompt(self, code_txt):
        pass 

    def explain_code(self, code_txt: str) -> dict:
        # Interact with the LLM using OLLAMA
        response = chat(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Principal Software Engineer with over 15 years of experience in software engineering and AI. Your task is to review and explain the following Python code snippet strictly following the guidelines and tone of the official Python documentation (PEP-8, Python Docs style guide). Return explanation JSON format with key code_explanation"
                    ),
                },
                {
                    "role": "user",
                    "content": f"{code_txt}",
                },
            ],
            
           format=CodeExplanation.model_json_schema(),
            options={'temperature': self.temperature}
        )

        # Step 3: Validate and convert response to dictionary
        structured_response = CodeExplanation.model_validate_json(response.message.content)
        response_dct = structured_response.model_dump()
        ans = response_dct['code_explanation']
        return ans 


# Example usage
if __name__ == "__main__":
    model_name = 'qwen3:0.6b'
    code_txt = """
        def subtract(a, b):
        return a - b'
    """
    
    explainer = CodeAnalyzer(model_name)
    result = explainer.explain_code(code_txt)
    print(result)
