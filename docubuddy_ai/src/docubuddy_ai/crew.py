from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class DocubuddyAi:
    """Crew that segments code and explains it from developer and business perspectives."""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def code_segmenter(self) -> Agent:
        return Agent(config=self.agents_config['code_segmenter'], verbose=True)

    @agent
    def developer_explainer(self) -> Agent:
        return Agent(config=self.agents_config['developer_explainer'], verbose=True)

    @agent
    def business_explainer(self) -> Agent:
        return Agent(config=self.agents_config['business_explainer'], verbose=True)

    @task
    def analyze_code_task(self) -> Task:
        """Task 1: Segment the code."""
        return Task(config=self.tasks_config['task1'])

    @task
    def explain_code_developer_task(self) -> Task:
        """Task 2: Developer-focused code explanation."""
        return Task(config=self.tasks_config['task2'])

    @task
    def explain_code_business_task(self) -> Task:
        """Task 3: Business-focused code explanation."""
        return Task(config=self.tasks_config['task3'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
