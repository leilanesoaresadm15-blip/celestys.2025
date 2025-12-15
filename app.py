import streamlit as st
import google.generativeai as genai

# Configuração da página (título que aparece na aba)
st.set_page_config(page_title="Meu Projeto Escolar")

# Título do site
st.title("🤖 Teste meu Projeto de IA!")

# Pega a senha e o prompt do "cofre" do Streamlit
api_key = st.secrets["GOOGLE_API_KEY"]
meu_prompt_secreto = st.secrets["PROMPT_SECRETO"]

# Configura o Google Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# Cria a caixa de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra as mensagens antigas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Onde seu amigo digita
if user_input := st.chat_input("Digite sua mensagem aqui..."):
    # Mostra o que o amigo digitou
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # A MÁGICA: Junta o prompt secreto com o que o amigo digitou
    # O amigo NÃO vê essa parte
    prompt_completo = f"{meu_prompt_secreto}\n\nO usuário disse: {user_input}"

    # Envia pro Google e pega a resposta
    response = model.generate_content(prompt_completo)
    
    # Mostra a resposta da IA
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
