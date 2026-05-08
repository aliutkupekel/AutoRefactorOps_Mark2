from crewai import Agent
from src.core.crew_tools import scan_directory

def get_discovery_agent(config: dict, llm_model: any) -> Agent:
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        verbose=True,
        allow_delegation=False,
        llm=llm_model,
        tools=[scan_directory]
    )