import streamlit as st
#IT CANT BE RUN ON NORMAL JUPYER NB
st.title("Register youself")
st.write("Hellllooo")
name = st.text_input("Enter you name")
name1 = st.chat_input("This is chat input")

st.success("This is a success message")

age = st.number_input(
    "Student age",
    min_value=1,
    max_value=100,
    value=18
)

course = st.selectbox(
    "Slecet a course",
    ["ENG","MARATHI","HINDI"]
)

if st.button("Show Details"):
    st.subheader("Student Details")
    st.write("Name",name)
    st.write("Age",age)
    st.write("Course",course)
    st.write(name1)

    if name:
        st.success(f"{name} is enrolled in {course}")
    else:
        st.warning("Please enter the student's name.")
