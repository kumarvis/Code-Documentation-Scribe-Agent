from pydantic import BaseModel
from ollama import chat


# Step 1: Define the Pydantic model for structured response
class CodeReview(BaseModel):
    code_review: str

# Step 2: Build a reusable class to handle structured chat interactions
class CodeReviewer:
    def __init__(self, model_name: str, temperature: float = 0):
        self.model_name = model_name
        self.temperature = temperature

    def get_user_prompt(self, code_txt):
        pass 

    def review_code(self, code_txt: str, code_documentation: str) -> dict:
        # Interact with the LLM using OLLAMA
        response = chat(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Principal Software Engineer with over 15 years of experience in software engineering and AI. Your task is to review the given code snippet and code documentation review it and provide updated code documentation. While updating documentation strictly following the guidelines and tone of the official Python documentation (PEP-8, Python Docs style guide). Return explanation JSON format with key code_review"
                    ),
                },
                {
                    "role": "user",
                    "content": f"code snippet = {code_txt} and code documentation = {code_documentation}",
                },
            ],
            
           format=CodeReview.model_json_schema(),
            options={'temperature': self.temperature}
        )

        # Step 3: Validate and convert response to dictionary
        structured_response = CodeReview.model_validate_json(response.message.content)
        response_dct = structured_response.model_dump()
        ans = response_dct['code_review']
        return ans 


# Example usage
if __name__ == "__main__":
    model_name = 'qwen3:1.7b'
    code_txt = """
        def subtract(a, b):
        return a - b'
    """
    from agents.code_analyzer_agent import CodeAnalyzer
    explainer = CodeAnalyzer(model_name)
    code_documentation = explainer.explain_code(code_txt)
    reviewer_obj = CodeReviewer(model_name)
    updated_code_documentation = reviewer_obj.review_code(code_txt, code_documentation)
    print(updated_code_documentation)
