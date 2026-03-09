import os
import yaml
from dotenv import load_dotenv
from crewai import Agent, Crew, Task, Process, LLM

load_dotenv()

llm = LLM(
    model="gemini/gemini-3-flash-preview",
    temperature=0.4,
    api_key=os.getenv("GOOGLE_API_KEY")
)


def load_yaml(path):
    """Загрузка конфигурации с соблюдением структуры проекта"""
    # Используем абсолютный путь, чтобы Streamlit не терял файлы
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, path)
    with open(full_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class AppealCrew:
    def __init__(self):
        # Структурированный подход к данным
        self.agents_config = load_yaml("config/agents.yaml")
        self.tasks_config = load_yaml("config/tasks.yaml")

    def crew(self) -> Crew:
        """Создание команды с последовательным взаимодействием (Sequential)"""

        # Агенты с четкими ролями для эффективного принятия решений
        student_agent = Agent(
            config=self.agents_config['student_agent'],
            llm=llm,
            verbose=True
        )

        reviewer_agent = Agent(
            config=self.agents_config['reviewer_agent'],
            llm=llm,
            verbose=True
        )

        decision_agent = Agent(
            config=self.agents_config['decision_agent'],
            llm=llm,
            verbose=True
        )

        # Последовательные задачи обеспечивают стабильный обмен данными
        tasks = [
            Task(config=self.tasks_config['create_appeal'], agent=student_agent),
            Task(config=self.tasks_config['review_appeal'], agent=reviewer_agent),
            Task(config=self.tasks_config['make_decision'], agent=decision_agent)
        ]

        return Crew(
            agents=[student_agent, reviewer_agent, decision_agent],
            tasks=tasks,
            process=Process.sequential,  # Гарантирует передачу контекста между агентами
            verbose=True
        )
