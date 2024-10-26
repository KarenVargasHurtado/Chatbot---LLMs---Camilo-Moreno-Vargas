import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain.sql_database import SQLDatabase

# conexión a la base de datos
with open('C:/ProyectoChatOpenAI/Scripts/password_sql.txt') as f:
    pass_sql = f.read()

config = {
    'user': 'root',
    'password': pass_sql,
    'host': '127.0.0.1',
    'database': 'mundo'
}

# Iniciar OpenAI
with open('C:/ProyectoChatOpenAI/Scripts/Api_key.txt') as f:
    api_key = f.read()
llm = ChatOpenAI(openai_api_key=api_key, temperature=0)

# Cadena de conexión a la base de datos MySQL
connection_string = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}"

# Instancia de la base de datos SQL
db = SQLDatabase.from_uri(connection_string)

# Agente SQL
agent = create_sql_agent(
    llm,
    db=db,
    verbose=True  # Muestra los pasos del agente para depuración
)

# Interfaz de usuario en Streamlit
st.title("Chatbot de Consulta a Base de Datos")

# Entrada del usuario
user_input = st.text_input("Escribe tu consulta sobre la base de datos:")

# Procesar consulta
if st.button("Enviar"):
    if user_input:
        try:
            response = agent.run(user_input)
            st.write(f"Respuesta: {response}")
        except Exception as e:
            st.error(f"Error al procesar la consulta: {e}")
    else:
        st.write("Por favor ingresa una consulta.")