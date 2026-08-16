"""
基于Streamlit完成WEB网页上传服务

pip install streamlit

Streamlit: 当WEB页面发生变化，则代码重新执行一遍
"""

import streamlit as st
from knowledge_base import KnowledgeBaseService
import time

# 添加网页标题
st.title("知识库更新服务")

# file_uploader 文件上传框
uploaded_file = st.file_uploader(
    "请上传TXT文件",
    type=["txt"],
    accept_multiple_files=False,        # False表示仅接受一个文件的上传
)

service = KnowledgeBaseService()
# session_state是一个字典
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if uploaded_file is not None:
    # 提取文件的名称、类型和大小
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size / 1024   # 文件大小单位为KB

    st.subheader(f"文件名：{file_name}")      # 子标题
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")     # 正常大小文本

    # get_value -> bytes -> decode('utf-8')
    text = uploaded_file.getvalue().decode('utf-8')

    with st.spinner("正在处理文件..."):       # 在sping内的代码执行过程中，会有一个转圈动画
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)
