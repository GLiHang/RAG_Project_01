# 智能客服 RAG 系统

基于 **LangChain + Chroma + 阿里云 DashScope 向量模型 + Streamlit** 构建的检索增强生成（RAG）知识库系统。系统面向智能客服场景，支持将客服知识文档（TXT）上传入库、自动去重、文本分割、向量化存储与相似度检索，为后续接入大模型问答链路提供知识底座。

## ✨ 功能特性

- 📤 **网页上传入库**：基于 Streamlit 提供 Web 上传界面，一键将 TXT 客服知识文档写入向量库
- 🔁 **MD5 内容去重**：对上传内容计算 MD5 指纹并记录到本地文件，重复内容自动跳过，避免知识库冗余
- ✂️ **中文智能分割**：使用 `RecursiveCharacterTextSplitter`，按中英文标点（`。！?`）与换行符切分文本，`chunk_size=1000`、`chunk_overlap=100`，短文本（≤1000 字）不分割直接入库
- 🧠 **向量化存储**：调用阿里云百炼 `text-embedding-v4` 嵌入模型，将文本转为向量存入 Chroma（collection 名 `rag`，本地持久化）
- 📝 **元数据管理**：每个文档块记录来源文件名、创建时间、操作人等元数据，便于溯源
- 🔍 **向量检索器**：封装 Chroma 检索器（默认 `top_k=2`），为 RAG 问答链路提供标准接口

## 🛠 技术栈

| 分类 | 技术 |
| ---- | ---- |
| 语言 | Python 3.14（虚拟环境 `.venv`） |
| Web 界面 | Streamlit |
| 向量数据库 | Chroma（本地持久化 `./chroma_db`） |
| 嵌入模型 | 阿里云 DashScope `text-embedding-v4` |
| 文本分割 | LangChain `RecursiveCharacterTextSplitter` |
| 去重机制 | `hashlib` MD5 + 本地记录文件 |

## 📂 项目结构

```
RAG_Project_01/
├── app_file_uploader.py   # Streamlit 网页上传服务（入口）
├── knowledge_base.py      # 知识库服务：MD5 去重 + 文本分割 + 向量化入库
├── vector_stores.py       # 向量检索服务：封装 Chroma 检索器
├── config_data.py         # 全局配置（分割参数、检索参数、路径等）
├── data/                  # 客服知识文档（TXT）
│   ├── 尺码推荐.txt
│   ├── 洗涤养护.txt
│   └── 颜色选择.txt
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

## 🚀 快速开始

### 1. 环境准备

```bash
# 进入项目目录，激活虚拟环境
.venv\Scripts\activate

# 安装依赖（如尚未安装）
pip install streamlit langchain-chroma langchain-community langchain-text-splitters
```

### 2. 配置 API Key

`DashScopeEmbeddings` 需要阿里云百炼的 API Key，请配置环境变量：

```bash
# Windows PowerShell
$env:DASHSCOPE_API_KEY = "sk-你的密钥"
```

### 3. 启动网页服务

```bash
streamlit run app_file_uploader.py
```

浏览器访问 `http://localhost:8501`，在页面中上传 TXT 文件即可完成知识入库，页面会反馈 `[成功]内容已上传至知识库` 或 `[跳过]内容已经存在在知识库中`。

### 4. 测试向量检索（可选）

```bash
python vector_stores.py
```

会以示例问题 `"我的体重是75kg，身高181cm，尺码推荐"` 检索知识库中最相似的文档块。

## 🧩 核心模块

### `knowledge_base.py` — 知识库服务（核心）

- `get_string_md5(input_str)`：计算字符串的 MD5 十六进制指纹
- `check_md5(md5_str)` / `save_md5(md5_str)`：查询 / 追加 MD5 记录，实现内容级去重
- `KnowledgeBaseService`：
  - `__init__`：初始化 Chroma 向量库与中文文本分割器
  - `upload_by_str(data, filename)`：入库主流程 —— 计算 MD5 → 去重检查 → 文本分割 → 向量化写入 Chroma（携带 source / create_time / operator 元数据）→ 记录 MD5

### `vector_stores.py` — 向量检索服务

- `VectorStoreService(embedding)`：传入嵌入模型，连接现有 Chroma 集合
- `get_retriever()`：返回配置好 `top_k` 的检索器，可直接接入 LangChain 问答链（如 `RetrievalQA`）

### `app_file_uploader.py` — Streamlit 网页

- 上传框限制为单个 TXT 文件（`accept_multiple_files=False`）
- 展示文件名、格式、大小（KB）
- 通过 `st.session_state` 复用知识库服务实例，避免重复初始化

## 📚 已入库示例知识

当前 `data/` 目录下已包含 3 份服装类客服文档（均已成功入库，`md5.text` 中有 3 条记录）：

- **尺码推荐.txt**：按身高体重推荐 S~XXL 码
- **洗涤养护.txt**：水温控制、洗涤剂选择、晾晒熨烫建议
- **颜色选择.txt**：主打色推荐、肤色搭配、场景穿搭建议

## 🗺 后续规划

- [ ] **问答链路**：接入大模型（如通义千问）与 `RetrievalQA` 链，实现"检索 + 生成"完整问答
- [ ] **聊天界面**：在 Streamlit 中增加对话式客服问答页面
- [ ] **支持更多格式**：PDF / Word / Markdown 等文档解析入库
- [ ] **批量上传**：支持多文件同时上传

## ⚠️ 注意事项

- 首次运行需要有效的 `DASHSCOPE_API_KEY`，否则嵌入调用会失败
- 上传内容需为 UTF-8 编码的 TXT 文件
- 向量库为本地持久化，删除 `chroma_db/` 目录即清空知识库；如需重新入库，请同步清理 `md5.text`，否则会被去重逻辑跳过
