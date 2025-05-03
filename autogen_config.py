from autogen import AssistantAgent, UserProxyAgent

# 1. Code Analyzer Agent (uses LLM)
code_analyzer = AssistantAgent(
    name="code_analyzer",
    llm_config={
        "config_list": [{"model": "gpt-4", "api_key": "your-api-key"}],
        "cache_seed": 42,
    },
    system_message="You are a Python documentation generator. For a given code block, generate detailed, clear markdown documentation describing its purpose, parameters, and return values."
)

# 2. Code Reviewer Agent (optional different LLM)
code_reviewer = AssistantAgent(
    name="code_reviewer",
    llm_config={
        "config_list": [{"model": "gpt-4", "api_key": "your-api-key"}],
        "cache_seed": 43,
    },
    system_message="You are a documentation reviewer. Review the function code and its markdown documentation. Fix errors, hallucinations, or style inconsistencies. Be precise and concise."
)

# 3. Documentation Composer Agent (non-LLM, acts on Python logic)
composer_agent = UserProxyAgent(
    name="doc_composer",
    code_execution_config={"use_docker": False},
    human_input_mode="NEVER",
    system_message="You are a Markdown documentation composer. Group documentation by top-level functions and class methods and write to a single file named <filename>_documentation.md."
)

# 4. Orchestrator Agent (drives the whole process)
orchestrator_agent = UserProxyAgent(
    name="orchestrator",
    code_execution_config={"use_docker": False},
    human_input_mode="NEVER",
    system_message="You are the orchestrator. For each Python file, use the AST utility to extract functions and methods. For each, pass the code to code_analyzer, then to code_reviewer, then to doc_composer."
)
