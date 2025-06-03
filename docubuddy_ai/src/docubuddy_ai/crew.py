from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from typing import Any

@CrewBase
class CodeExplainBuddy:
    """CodeExplainBuddy crew with code segmentation and two perspectives (Developer & Business) explanations."""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def code_segmenter(self) -> Agent:
        return Agent(
            config=self.agents_config['code_segmenter'],  # maps to agents.yaml
            verbose=True
        )

    @agent
    def developer_explainer(self) -> Agent:
        return Agent(
            config=self.agents_config['developer_explainer'],  # maps to agents.yaml
            verbose=True
        )

    @agent
    def business_explainer(self) -> Agent:
        return Agent(
            config=self.agents_config['business_explainer'],  # maps to agents.yaml
            verbose=True
        )

    @task
    def analyze_code_task(self) -> Task:
        """Task 1: Analyze code into components"""
        return Task(
            config=self.tasks_config['task1'],
            # expects input: code_text
        )

    @task
    def explain_code_developer_task(self) -> Task:
        """Task 2: Developer-focused code explanation"""
        return Task(
            config=self.tasks_config['task2'],
            # expects input: segmented_code, user_prompt
        )

    @task
    def explain_code_business_task(self) -> Task:
        """Task 3: Business-focused code explanation"""
        return Task(
            config=self.tasks_config['task3'],
            # expects input: segmented_code, user_prompt
        )

    @crew
    def crew(self) -> Crew:
        """Create the crew with agents and tasks."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  # Run tasks in order (segment first, then explain)
            verbose=True,
        )
