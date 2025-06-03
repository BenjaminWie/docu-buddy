from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import json

@CrewBase
class CodeExplainBuddy:
    """CodeExplainBuddy crew with code segmentation and two perspectives (Developer & Business) explanations."""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def code_segmenter(self) -> Agent:
        return Agent(
            config=self.agents_config['code_segmenter'],
            verbose=True
        )

    @agent
    def developer_explainer(self) -> Agent:
        return Agent(
            config=self.agents_config['developer_explainer'],
            verbose=True
        )

    @agent
    def business_explainer(self) -> Agent:
        return Agent(
            config=self.agents_config['business_explainer'],
            verbose=True
        )

    @task
    def analyze_code_task(self) -> Task:
        """Task 1: Analyze code into components"""
        return Task(
            config=self.tasks_config['task1'],
        )

    @task
    def explain_code_developer_task(self) -> Task:
        """Task 2: Developer-focused code explanation"""
        return Task(
            config=self.tasks_config['task2'],
        )

    @task
    def explain_code_business_task(self) -> Task:
        """Task 3: Business-focused code explanation"""
        return Task(
            config=self.tasks_config['task3'],
        )

    def format_segmented_code(self, segments):
        """Format list output from code_segmenter into a readable string."""
        if isinstance(segments, list):
            formatted_parts = []
            for segment in segments:
                segment_type = segment.get('type', 'Unknown').capitalize()
                name = segment.get('name', 'Unnamed')
                code_block = segment.get('code', '')
                header = f"### {segment_type}: {name}\n"
                formatted_parts.append(f"{header}{code_block}\n")
            return "\n".join(formatted_parts)
        # If already a string, return as is
        return segments

    @crew
    def crew(self) -> Crew:
        """Create the crew with agents and tasks."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            post_process=self._post_process_outputs  # Added post-process hook
        )

    def _post_process_outputs(self, outputs):
        """
        This method is called after each task execution.
        It ensures that segmented_code is a properly formatted string before passing to next tasks.
        """
        if 'segmented_code' in outputs:
            outputs['segmented_code'] = self.format_segmented_code(outputs['segmented_code'])
        return outputs
