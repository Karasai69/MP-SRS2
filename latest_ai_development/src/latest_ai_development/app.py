import streamlit as st
from crew import AppealCrew
import sys
import os

st.set_page_config(page_title="Appeal System AI", page_icon="🎓", layout="centered")

# Исправляем импорт crew
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from crew import AppealCrew

# --- ИНТЕРФЕЙС ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3407/3407024.png", width=100)
    st.title("О проекте")
    st.info("Эта система использует ИИ-агентов для анализа апелляций.")
    st.write("Когнитивное ядро: **Gemini 1.5 Flash**")

st.header("📝 Форма подачи апелляции")

col1, col2 = st.columns(2)
with col1:
    student_name = st.text_input("👤 Имя студента", placeholder="Иван Иванов")
    exam = st.text_input("📚 Дисциплина", placeholder="Программирование")
with col2:
    grade = st.number_input("💯 Текущий балл", 0, 100, value=50)
    type_exam = st.selectbox("Тип контроля", ["Экзамен", "РК1", "РК2", "СРС"])

reason = st.text_area("🔍 Обоснование апелляции")

if st.button("🚀 Отправить на рассмотрение", use_container_width=True):
    if not reason or not student_name:
        st.warning("Пожалуйста, заполните все поля!")
    else:
        with st.status("🤖 Агенты обсуждают ваше решение...", expanded=True) as status:
            crew_instance = AppealCrew()
            result = crew_instance.crew().kickoff(
                inputs={
                    "student_name": student_name,
                    "exam": exam,
                    "grade": grade,
                    "appeal_reason": reason
                }
            )
            status.update(label="✅ Решение принято!", state="complete")

        st.subheader("🏁 Итоговое решение комиссии")
        st.success(result)
sys.path.append(os.path.dirname(__file__))

st.title("Система апелляций экзамена")

student_name = st.text_input("Имя студента")
exam = st.text_input("Экзамен")
grade = st.number_input("Оценка", 0, 100)
reason = st.text_area("Причина апелляции")

if st.button("Отправить апелляцию"):

    crew_instance = AppealCrew()
    crew = crew_instance.crew()

    result = crew.kickoff(
        inputs={
            "student_name": student_name,
            "exam": exam,
            "grade": grade,
            "appeal_reason": reason
        }
    )

    st.subheader("Решение комиссии")
    st.write(result)
