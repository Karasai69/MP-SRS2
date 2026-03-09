import streamlit as st
from crew import AppealCrew
import sys
import os

# Добавляем текущую директорию в пути поиска модулей
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