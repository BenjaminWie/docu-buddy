from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any

@CrewBase
class DocubuddyAi:
    """DocubuddyAi crew with code analysis, compliance check, and documentation generation."""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def code_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_analyzer'],  # from agents.yaml
            verbose=True
        )

    @agent
    def compliance_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['compliance_checker'],  # from agents.yaml
            verbose=True
        )

    @agent
    def doc_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['doc_writer'],  # from agents.yaml
            verbose=True
        )

    @task
    def analyze_code_task(self) -> Task:
        """Task 1: Analyze code into components"""
        return Task(
            config=self.tasks_config['task1'],  # from tasks.yaml
            # expects input: code_text, compliance_info
        )

    @task
    def compliance_check_task(self) -> Task:
        """Task 2: Check compliance of code components"""
        return Task(
            config=self.tasks_config['task2'],
            # expects input: code_components, compliance_info
        )

    @task
    def generate_docs_task(self) -> Task:
        """Task 3: Generate documentation and README"""
        return Task(
            config=self.tasks_config['task3'],
            output_file='README.md'
            # expects input: code_components, compliance_feedback
        )

    @crew
    def crew(self) -> Crew:
        """Create the crew with agents and tasks in sequential process."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  # run tasks one after another
            verbose=True,
        )
