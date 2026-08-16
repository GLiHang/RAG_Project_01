# 智能客服 RAG 系统

基于 **LangChain + Chroma + 阿里云 DashScope（通义千问 / 向量模型）+ Streamlit** 构建的检索增强生成（RAG）智能客服系统。系统覆盖知识库管理（文档上传、MD5 去重、文本分割、向量化入库）与智能问答（向量检索、大模型生成、多轮对话历史）完整链路，开箱即用。

## ✨ 功能特性

### 📚 知识库管理
- 📤 **网页上传入库**：Streamlit Web 界面一键上传 TXT 客服知识文档并写入向量库
- 🔁 **MD5 内容去重**：对上传内容计算 MD5 指纹并记录到本地文件，重复内容自动跳过，避免知识库冗余
- ✂️ **中文智能分割**：`RecursiveCharacterTextSplitter` 按中文标点（`。！?`）与换行符切分，`chunk_size=1000`、`chunk_overlap=100`，短文本（≤1000 字）不分割直接入库
- 🧠 **向量化存储**：阿里云百炼 `text-embedding-v4` 嵌入模型，向量存入 Chroma（collection 名 `rag`，本地持久化）
- 📝 **元数据管理**：每个文档块记录来源文件名、创建时间、操作人等元数据，便于溯源

### 🤖 智能问答
- 🔍 **向量检索器**：Chroma 检索器（默认 `top_k=2`）召回最相关文档片段作为回答依据
- 🧩 **RAG 问答链路**：LangChain LCEL 表达式组装"检索 → 组装上下文 → 大模型生成"完整链路
- 💬 **聊天界面**：Streamlit 对话式客服页面，支持流式输出（打字机效果）
- 🕘 **多轮对话记忆**：基于 `RunnableWithMessageHistory` + JSON 文件持久化，按会话（session_id）保存历史，支持上下文连续问答

## 🛠 技术栈

| 分类 | 技术 |
| ---- | ---- |
| 语言 | Python 3.14（虚拟环境 `.venv`） |
| Web 界面 | Streamlit（上传页 + 聊天页） |
| 向量数据库 | Chroma（本地持久化 `./chroma_db`） |
| 嵌入模型 | 阿里云 DashScope `text-embedding-v4` |
| 对话模型 | 阿里云通义千问 `qwen3-max`（流式输出） |
| 框架 | LangChain（LCEL 链路、`RunnableWithMessageHistory`） |
| 文本分割 | `RecursiveCharacterTextSplitter` |
| 去重机制 | `hashlib` MD5 + 本地记录文件 |
| 历史存储 | JSON 文件（`chat_history/`） |

## 📂 项目结构

```
RAG_Project_01/
├── app_file_uploader.py   # Streamlit 网页上传服务（知识入库入口）
├── app_qa.py              # Streamlit 智能客服聊天界面（问答入口）
├── RAG.py                 # RAG 问答链路核心（检索 + 生成 + 多轮对话）
├── knowledge_base.py      # 知识库服务：MD5 去重 + 文本分割 + 向量化入库
├── vector_stores.py       # 向量检索服务：封装 Chroma 检索器
├── file_history_store.py  # 对话历史持久化：按 session_id 存 JSON 文件
├── config_data.py         # 全局配置（分割、检索、模型、会话参数）
├── data/                  # 客服知识文档（TXT）
│   ├── 尺码推荐.txt
│   ├── 洗涤养护.txt
│   └── 颜色选择.txt
├── chat_history/          # 多轮对话历史记录（JSON，按会话分文件）
├── chroma_db/             # Chroma 向量库持久化目录
├── md5.text               # 已入库内容的 MD5 记录（去重依据）
└── .venv/                 # Python 虚拟环境
```

## ⚙️ 配置说明（`config_data.py`）

| 配置项 | 默认值 | 说明 |
| ------ | ------ | ---- |
| `md5_path` | `md5.text` | MD5 去重记录文件路径 |
| `collection_name` | `rag` | Chroma 向量库集合（表）名 |
| `persist_directory` | `./chroma_db` | 向量库本地存储目录 |
| `chunk_size` | `1000` | 分割后文本块最大长度 |
| `chunk_overlap` | `100` | 相邻文本块重叠长度 |
| `separators` | `["\n\n", "\n", "。", "！", "?"]` | 中文文本切分符号优先级 |
| `max_spliter_char_number` | `1000` | 超过该长度才进行分割的阈值 |
| `top_k` | `2` | 检索时返回的匹配文档数量 |
| `embedding_model_name` | `text-embedding-v4` | 向量嵌入模型 |
| `chat_model_name` | `qwen3-max` | 对话大模型 |
| `session_config` | `session_id = "user_01"` | 默认会话 ID 配置 |

## 🚀 快速开始

### 1. 环境准备

```bash
# 进入项目目录，激活虚拟环境
.venv\Scripts\activate

# 安装依赖（如尚未安装）
pip install streamlit langchain-chroma langchain-community langchain-text-splitters langchain-core
```

### 2. 配置 API Key

嵌入模型与对话模型均使用阿里云百炼（DashScope），请配置环境变量：

```bash
# Windows PowerShell
$env:DASHSCOPE_API_KEY = "sk-你的密钥"
```

### 3. 启动服务

**知识库更新页**（上传文档入库）：

```bash
streamlit run app_file_uploader.py
```

**智能客服问答页**（聊天问答）：

```bash
streamlit run app_qa.py
```

浏览器访问 `http://localhost:8501`。首次问答前请先在上传页完成知识入库（或使用 `data/` 下已入库的示例文档）。

### 4. 命令行测试（可选）

```bash
# 测试知识检索
python vector_stores.py

# 测试 RAG 问答链路（默认会话 user_01）
python RAG.py
```

## 🧩 核心模块

### `knowledge_base.py` — 知识库服务（入库）

- `get_string_md5(input_str)`：计算字符串的 MD5 十六进制指纹
- `check_md5(md5_str)` / `save_md5(md5_str)`：查询 / 追加 MD5 记录，实现内容级去重
- `KnowledgeBaseService`：
  - `__init__`：初始化 Chroma 向量库与中文文本分割器
  - `upload_by_str(data, filename)`：入库主流程 —— 计算 MD5 → 去重检查 → 文本分割 → 向量化写入 Chroma（携带 source / create_time / operator 元数据）→ 记录 MD5

### `vector_stores.py` — 向量检索服务

- `VectorStoreService(embedding)`：传入嵌入模型，连接现有 Chroma 集合
- `get_retriever()`：返回配置好 `top_k` 的检索器，供问答链路接入

### `RAG.py` — RAG 问答链路（核心）

- `RagService`：
  - `__init__`：初始化向量检索器、Prompt 模板（系统提示 + 参考资料 context + 对话历史 history + 用户问题）、通义千问流式对话模型，并组装最终执行链
  - `_get_chain()`：LCEL 组装"检索 → 格式化文档 → 填充 Prompt → 模型生成 → 字符串输出"的链路，外层用 `RunnableWithMessageHistory` 接入多轮对话历史
  - 检索无结果时返回"无相关参考资料"兜底

### `file_history_store.py` — 对话历史存储

- `FileChatMessageHistory`：继承 `BaseChatMessageHistory`，按 `session_id` 将消息序列化为 JSON 存到 `chat_history/` 目录
- `get_history(session_id)`：按会话 ID 获取历史记录对象，供 `RunnableWithMessageHistory` 使用

### `app_file_uploader.py` — 知识上传网页

- 上传框限制为单个 TXT 文件（`accept_multiple_files=False`）
- 展示文件名、格式、大小（KB）
- 通过 `st.session_state` 复用知识库服务实例，避免重复初始化

### `app_qa.py` — 智能客服聊天网页

- 标题 + 分隔符，初始化欢迎语与 `RagService` 实例（存于 `st.session_state`）
- 渲染历史消息（`st.chat_message`），底部提供输入框（`st.chat_input`）
- 流式输出：包装链的流式生成器，`st.write_stream` 实时展示，同时拼接完整回答存入会话消息列表，保证刷新后历史不丢失

## 📚 已入库示例知识

当前 `data/` 目录下已包含 3 份服装类客服文档（均已成功入库，`md5.text` 中有 3 条记录）：

- **尺码推荐.txt**：按身高体重推荐 S~XXL 码
- **洗涤养护.txt**：水温控制、洗涤剂选择、晾晒熨烫建议
- **颜色选择.txt**：主打色推荐、肤色搭配、场景穿搭建议

可在问答页直接咨询，例如："我的体重是75kg，身高181cm，尺码推荐"、"毛衣如何保养"。

## 🗺 后续规划

- [ ] **支持更多文档格式**：PDF / Word / Markdown 等解析入库
- [ ] **批量上传**：支持多文件同时上传
- [ ] **会话管理界面**：在聊天页切换 / 新建 / 清空多会话
- [ ] **知识库管理**：查看、删除向量库中的文档

## ⚠️ 注意事项

- 首次运行需要有效的 `DASHSCOPE_API_KEY`（嵌入与对话模型均依赖），否则调用会失败
- 上传内容需为 UTF-8 编码的 TXT 文件
- 向量库为本地持久化，删除 `chroma_db/` 目录即清空知识库；如需重新入库，请同步清理 `md5.text`，否则会被去重逻辑跳过
- 对话历史按 `session_id` 保存在 `chat_history/`，删除对应文件即可清空该会话记忆
