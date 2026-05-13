import os
import yaml
from pathlib import Path
# Sadece CrewAI'ın kendi yerleşik özelliklerini kullanıyoruz
from crewai import Task, Crew, Process, LLM
from dotenv import load_dotenv

from src.agents.discovery import get_discovery_agent
from src.agents.refactor import get_refactoring_agent
from src.agents.verification import get_verification_agent
from src.agents.rollback import get_rollback_agent

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    print("CRITICAL WARNING: GROQ_API_KEY is not set in your .env file.")

def load_yaml(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def main():
    print("Initializing AutoRefactorOps Multi-Agent System...")
    
    # Doğrudan Groq bağlantısı (LangChain veya OpenAI aracıları olmadan)
    groq_llm = LLM(
        model="groq/llama3-70b-8192",
        temperature=0.1,
        api_key=os.getenv("GROQ_API_KEY")
    )

    config_dir = Path(__file__).parent / "config"
    agents_config = load_yaml(config_dir / "agents.yaml")
    tasks_config = load_yaml(config_dir / "tasks.yaml")

    discovery_agent = get_discovery_agent(agents_config['discovery_agent'], groq_llm)
    refactoring_agent = get_refactoring_agent(agents_config['refactoring_agent'], groq_llm)
    verification_agent = get_verification_agent(agents_config['verification_agent'], groq_llm)
    rollback_agent = get_rollback_agent(agents_config['rollback_agent'], groq_llm)

    task_discover = Task(
        description=tasks_config['discovery_task']['description'] + "\nTarget Directory: evaluation/synthetic_repo",
        expected_output=tasks_config['discovery_task']['expected_output'],
        agent=discovery_agent
    )
    task_save_state = Task(
        description="Before any modifications happen, trigger the execute_git_state_save tool.",
        expected_output="Confirmation that the git state is saved.",
        agent=rollback_agent
    )
    task_refactor = Task(
        description=tasks_config['refactoring_task']['description'],
        expected_output=tasks_config['refactoring_task']['expected_output'],
        agent=refactoring_agent
    )
    task_verify = Task(
        description=tasks_config['verification_task']['description'] + "\nThe test suite path is: evaluation/synthetic_repo/test_target.py",
        expected_output=tasks_config['verification_task']['expected_output'],
        agent=verification_agent
    )
    task_finalize = Task(
        description=tasks_config['rollback_task']['description'],
        expected_output=tasks_config['rollback_task']['expected_output'],
        agent=rollback_agent
    )

    autorefactor_crew = Crew(
        agents=[discovery_agent, rollback_agent, refactoring_agent, verification_agent, rollback_agent],
        tasks=[task_discover, task_save_state, task_refactor, task_verify, task_finalize],
        process=Process.sequential,
        verbose=True
    )

    print("\nStarting the Refactoring Pipeline...")
    result = autorefactor_crew.kickoff()
    
    print("\n================================================")
    print("FINAL OPERATION REPORT")
    print("================================================")
    print(result)

if __name__ == "__main__":
    main()