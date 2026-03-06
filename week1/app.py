import streamlit as st
import ollama
from openai import OpenAI
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# initialize OpenAI client
openai_client = OpenAI()

MODEL_GPT = 'gpt-4o-mini'
MODEL_LLAMA = 'llama3.2'

# Constants
SYSTEM_PROMPT = "Eres un tutor técnico útil que responde preguntas sobre código Python, ingeniería de software, ciencia de datos y LLM"

st.title("Tutor Técnico LLM 🤖")
st.markdown("Haz una pregunta técnica y selecciona el modelo con el que quieres obtener tu respuesta.")

# Create the layout
model_choice = st.selectbox(
    "Selecciona el modelo:",
    (MODEL_GPT, MODEL_LLAMA)
)

question = st.text_area("Ingresa tu pregunta técnica aquí:", height=150)

if st.button("Enviar"):
    if not question.strip():
        st.warning("Por favor, ingresa una pregunta antes de enviar.")
    else:
        user_prompt = "Por favor, da una explicación detallada de la siguiente pregunta: " + question
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        
        st.subheader("Respuesta:")
        
        if model_choice == MODEL_GPT:
            # We use an empty placeholder to stream the response
            response_placeholder = st.empty()
            full_response = ""
            
            with st.spinner("Esperando respuesta de GPT-4o-mini..."):
                try:
                    stream = openai_client.chat.completions.create(
                        model=MODEL_GPT, 
                        messages=messages,
                        stream=True
                    )
                    
                    for chunk in stream:
                        content = chunk.choices[0].delta.content or ''
                        full_response += content
                        # We progressively write the response markdown
                        response_placeholder.markdown(full_response + "▌")
                    
                    # Remove the cursor at the end
                    response_placeholder.markdown(full_response)
                except Exception as e:
                    st.error(f"Error al llamar a OpenAI: {e}")
                    
        elif model_choice == MODEL_LLAMA:
            with st.spinner("Esperando respuesta de Llama 3.2..."):
                try:
                    response = ollama.chat(model=MODEL_LLAMA, messages=messages)
                    reply = response['message']['content']
                    st.markdown(reply)
                except Exception as e:
                    st.error(f"Error al llamar a Ollama: {e}")
