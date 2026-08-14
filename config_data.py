
md5_path = "./md5.text"

# Chroma
collection_name = "rag"
persist_directory = "./chroma_db"

# spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", "。", "！", "?"]
max_spliter_char_number = 1000          # 文本分割的阈值

#
top_k = 2            # 检索访问匹配的文档数量
