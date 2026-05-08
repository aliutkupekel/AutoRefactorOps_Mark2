from crewai import Agent
from src.core.crew_tools import read_target_file, write_refactored_code

def get_refactoring_agent(config: dict, llm_model: any) -> Agent:
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        verbose=True,
        allow_delegation=False,
        llm=llm_model,
        tools=[read_target_file, write_refactored_code]
    )