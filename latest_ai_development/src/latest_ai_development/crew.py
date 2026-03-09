import os


import yaml
from dotenv import load_dotenv
from crewai import Agent, Crew, Task, Process, LLM

st.set_page_config(page_title="Appeal System AI", page_icon="🎓", layout="centered")

# Боковая панель с инструкцией
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3407/3407024.png", width=100)
    st.title("О проекте")
    st.info("Эта система использует мультиагентную сеть для беспристрастной оценки апелляций студентов.")
    st.markdown("---")
    st.write("Когнитивное ядро: **Gemini 3 Flash Preview**")

st.header("📝 Форма подачи апелляции")

col1, col2 = st.columns(2)

with col1:
    student_name = st.text_input("👤 Имя студента", placeholder="Иван Иванов")
    exam = st.text_input("📚 Дисциплина", placeholder="Программирование")

with col2:
    grade = st.number_input("💯 Текущий балл", 0, 100, step=1)
    # Можно добавить выбор типа экзамена
    type_exam = st.selectbox("Тип контроля", ["Экзамен", "РК1", "РК2", "СРС"])

reason = st.text_area("🔍 Обоснование апелляции", placeholder="Опишите, с чем вы не согласны...")


# Загружаем ключи из .env для стабильного подключения к API
load_dotenv()

# Настройка когнитивного ядра Gemini
# Использование api_key напрямую гарантирует отсутствие ошибок аутентификации в Streamlit
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
