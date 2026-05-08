from crewai import Agent
from src.core.crew_tools import run_ast_validation, calculate_complexity_reduction, run_unit_tests

def get_verification_agent(config: dict, llm_model: any) -> Agent:
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        verbose=True,
        allow_delegation=False,
        llm=llm_model,
        tools=[run_ast_validation, calculate_complexity_reduction, run_unit_tests]
    )