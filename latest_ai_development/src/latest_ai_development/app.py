import streamlit as st
import os
import sys

st.set_page_config(page_title="Appeal System AI", page_icon="🎓", layout="centered")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from crew import AppealCrew

# --- БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3407/3407024.png", width=100)
    st.title("О проекте")
    st.info("Мультиагентная система для анализа академических апелляций.")
    st.markdown("---")
    st.write("Ядро: **Gemini 3 Flash Preview**")

# --- ГЛАВНЫЙ ИНТЕРФЕЙС ---
st.title("🎓 Система апелляций")
st.markdown("Заполните форму ниже для автоматического разбора вашего случая комиссией ИИ-агентов.")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("👤 Имя студента", placeholder="Аскар Карасай")
        exam = st.text_input("📚 Дисциплина", placeholder="Программирование")
    with col2:
        grade = st.number_input("💯 Текущий балл", 0, 100, value=50)
        type_exam = st.selectbox("Тип контроля", ["Экзамен", "РК1", "РК2", "СРС"])

    reason = st.text_area("🔍 Обоснование апелляции", placeholder="Опишите ваши аргументы...")

if st.button("🚀 Отправить на рассмотрение", use_container_width=True):
    if not reason or not student_name or not exam:
        st.error("Ошибка: Заполните все обязательные поля!")
    else:
        # Статус-бар работы агентов
        with st.status("🤖 Агенты анализируют данные...", expanded=True) as status:
            try:
                crew_instance = AppealCrew()
                # Запуск процесса
                result = crew_instance.crew().kickoff(
                    inputs={
                        "student_name": student_name,
                        "exam": f"{exam} ({type_exam})",
                        "grade": grade,
                        "appeal_reason": reason
                    }
                )
                status.update(label="✅ Анализ завершен!", state="complete", expanded=False)
                
                # Вывод результата
                st.subheader("🏁 Итоговое решение комиссии")
                st.success(result)
                
            except Exception as e:
                status.update(label="❌ Произошла ошибка", state="error")
                st.error(f"Ошибка при работе агентов: {e}")
