import os

import yaml
from crewai import Agent, Crew, Task
from crewai.llm import LLM
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv


@CrewBase
class news_agent_crew:
    "News Reporting Agent using Crew AI Agents"

    def __init__(self) -> None:
        agents_config_path = "config/agents.yaml"
        tasks_config_path = "config/tasks.yaml"

        with open(agents_config_path, "r") as f:
            self.agents_config = yaml.safe_load(f)
        with open(tasks_config_path, "r") as f:
            self.tasks_config = yaml.safe_load(f)

        load_dotenv()
        self.llm_config = LLM(
            model="groq/gemma2-9b-it", api_key=os.getenv("GROQ_API_KEY")
        )

    @agent
    def explainer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["explainer_agent"],
            llm=self.llm_config,
        )

    @task
    def explainer_task(self) -> Task:
        return Task(
            config=self.tasks_config["explainer_task"],
            llm=self.llm_config,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.explainer_agent()],
            tasks=[self.explainer_task()],
            verbose=False,
        )
