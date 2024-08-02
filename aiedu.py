import streamlit as st
import openai
import time

# Streamlit 앱 설정
st.set_page_config(page_title="MetaGIS AI Edu Assistant 챗봇", page_icon="🤖")
st.title("MetaGIS AI Edu Assistant 챗봇")

# 사이드바에 API 키 입력 필드 추가
api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")

# Assistant ID 설정
ASSISTANT_ID = "asst_IdvaoCuoA7CrRMwaMwWbzMm8"

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# OpenAI 클라이언트 초기화 함수
def init_openai_client():
    if api_key:
        openai.api_key = api_key
        return openai.Client()
    else:
        st.sidebar.error("API 키를 입력해주세요.")
        return None

# 메시지 전송 및 응답 받기 함수
def send_message(client, thread_id, content):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )
    
    while run.status != "completed":
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
    
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return messages.data[0].content[0].text.value

# 메인 앱 로직
client = init_openai_client()

if client:
    # 스레드 생성 또는 검색
    if st.session_state.thread_id is None:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

    # 사용자 입력
    user_input = st.chat_input("메시지를 입력하세요.")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = send_message(client, st.session_state.thread_id, user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # 대화 기록 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
else:
    st.info("API 키를 입력하면 챗봇을 사용할 수 있습니다.")