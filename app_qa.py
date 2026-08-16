import streamlit as st
import time
from RAG import RagService
import config_data as config

# 标题
st.title("智能客服")
st.divider()                # 分隔符

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "你好！有什么可以帮助你的吗？"}]

if "RAG" not in st.session_state:
    st.session_state["RAG"] = RagService()

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# 在页面最下方提供用户输入框
prompt = st.chat_input()

if prompt:

    # 在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    ai_res_list = []
    with st.spinner("AI思考中..."):
        res_stream = st.session_state["RAG"].chain.stream({"input": prompt}, config.session_config)
        # yield

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))
        st.session_state["messages"].append({"role": "assistant", "content": "".join(ai_res_list)})


