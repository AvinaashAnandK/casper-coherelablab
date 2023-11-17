import tiktoken

# Importing code library from git
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import Language
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Importing read the docs 
from langchain.document_loaders import ReadTheDocsLoader


# Creating embeddings
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores import Chroma
from langchain.vectorstores import Weaviate

def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding('cl100k_base')
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)

def load_codebase(repo_path,url):
    loader = GenericLoader.from_filesystem(
    repo_path + "/libs/langchain/langchain",
    glob="**/*",
    suffixes=[".py",".ipynb"],
    parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
    )

    documents = loader.load()

    python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
    )

    texts = python_splitter.split_documents(documents)

    for text in texts: 
        text.metadata['githublink'] = url

    return texts

def load_docs(docs_path,url):
    rtd_loader = ReadTheDocsLoader(docs_path)
    rtd_docs = rtd_loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=20,  # number of tokens overlap between chunks
    length_function=tiktoken_len,
    separators=['\n\n', '\n', ' ', '']
    )


    rtd_texts = text_splitter.split_documents(rtd_docs)

    for _text in rtd_texts:
        _text.metadata['githublink'] = url
        _text.metadata['language'] = 'english'


