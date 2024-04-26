"""Load html from files, clean up, split, ingest into Weaviate."""
import logging
import os
import re
from parser import langchain_docs_extractor # type: ignore

from bs4 import BeautifulSoup, SoupStrainer
from langchain_community.document_loaders import RecursiveUrlLoader, SitemapLoader
from langchain.indexes import SQLRecordManager, index
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.utils.html import PREFIXES_TO_IGNORE_REGEX, SUFFIXES_TO_IGNORE_REGEX
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import OllamaEmbeddings
from chromadb.config import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from constants import  EMBEDDING_MODEL, COLLECTION_NAME , VECTORESTORE_DIRECTORY 

def get_embeddings_model():
    return OllamaEmbeddings(model=EMBEDDING_MODEL)


def get_vectorestore():
    embedding = get_embeddings_model()


    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding,
        persist_directory=VECTORESTORE_DIRECTORY,
        client_settings=Settings(
            anonymized_telemetry=False, is_persistent=True, )
    )

def metadata_extractor(meta: dict, soup: BeautifulSoup) -> dict:
    title = soup.find("title")
    description = soup.find("meta", attrs={"name": "description"})
    html = soup.find("html")
    return {
        "source": meta["loc"],
        "title": title.get_text() if title else "",
        "description": description.get("content", "") if description else "",
        "language": html.get("lang", "") if html else "",
        **meta,
    }


def load_langchain_docs():
    return SitemapLoader(
        "https://python.langchain.com/sitemap.xml",
        filter_urls=["https://python.langchain.com/"],
        parsing_function=langchain_docs_extractor,
        default_parser="lxml",
        bs_kwargs={
            "parse_only": SoupStrainer(
                name=("article", "title", "html", "lang", "content")
            ),
        },
        meta_function=metadata_extractor,
    ).load()


def load_langsmith_docs():
    return RecursiveUrlLoader(
        url="https://docs.smith.langchain.com/",
        max_depth=8,
        extractor=simple_extractor,
        prevent_outside=True,
        use_async=True,
        timeout=600,
        # Drop trailing / to avoid duplicate pages.
        link_regex=(
            f"href=[\"']{PREFIXES_TO_IGNORE_REGEX}((?:{SUFFIXES_TO_IGNORE_REGEX}.)*?)"
            r"(?:[\#'\"]|\/[\#'\"])"
        ),
        check_response_status=True,
    ).load()


def simple_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()


def load_api_docs():
    return RecursiveUrlLoader(
        url="https://api.python.langchain.com/en/latest/",
        max_depth=8,
        extractor=simple_extractor,
        prevent_outside=True,
        use_async=True,
        timeout=600,
        # Drop trailing / to avoid duplicate pages.
        link_regex=(
            f"href=[\"']{PREFIXES_TO_IGNORE_REGEX}((?:{SUFFIXES_TO_IGNORE_REGEX}.)*?)"
            r"(?:[\#'\"]|\/[\#'\"])"
        ),
        check_response_status=True,
        exclude_dirs=(
            "https://api.python.langchain.com/en/latest/_sources",
            "https://api.python.langchain.com/en/latest/_modules",
        ),
    ).load()


def ingest_docs():
  
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)

    vectorstore = get_vectorestore()
    namespace = f"chromadb/{COLLECTION_NAME}"

    db_url = f"sqlite:///{VECTORESTORE_DIRECTORY}/record_manager_cache.sql"
    record_manager = SQLRecordManager(
        namespace, db_url=db_url
    )
    record_manager.create_schema()

    logger.info(f"Loading docs from documentation...")
    docs_from_documentation = load_langchain_docs()
    logger.info(f"Loaded {len(docs_from_documentation)} docs from documentation")
    # logger.info(f"Loading docs from API...")
    # docs_from_api = load_api_docs()
    # logger.info(f"Loaded {len(docs_from_api)} docs from API")
    # logger.info(f"Loading docs from langsmith...")
    # docs_from_langsmith = load_langsmith_docs()
    # logger.info(f"Loaded {len(docs_from_langsmith)} docs from Langsmith")

    docs_transformed = text_splitter.split_documents(
        docs_from_documentation  #+ docs_from_api + docs_from_langsmith
    )
    docs_transformed = [doc for doc in docs_transformed if len(doc.page_content) > 10]

    # We try to return 'source' and 'title' metadata when querying vector store and
    # Weaviate will error at query time if one of the attributes is missing from a
    # retrieved document.
    for doc in docs_transformed:
        if "source" not in doc.metadata:
            doc.metadata["source"] = ""
        if "title" not in doc.metadata:
            doc.metadata["title"] = ""

    logger.info(f"Indexing documents..")
    indexing_stats = index(
        docs_transformed,
        record_manager,
        vectorstore,
        cleanup="full",
        source_id_key="source",
        force_update=True,
    )

    logger.info(f"Indexing Done. Stats: {indexing_stats}")
    num_vecs = len(vectorstore.get())
    logger.info(
        f"The vectorestore now has this many vectors: {num_vecs}",
    )


if __name__ == "__main__":
    ingest_docs()
