from crewai import Agent
from src.core.crew_tools import execute_git_state_save, execute_git_rollback

def get_rollback_agent(config: dict, llm_model: any) -> Agent:
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        verbose=True,
        allow_delegation=False,
        llm=llm_model,
        tools=[execute_git_state_save, execute_git_rollback]
    )