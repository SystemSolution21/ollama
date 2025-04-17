"""The code uses a RAG approach to:
-Break documents into chunks
-Find relevant chunks using embeddings
-Use those chunks to generate focused answers using an LLM
-Save results to individual text files
"""

from pathlib import Path
import re
import numpy as np
import pandas as pd
import ollama
from sentence_transformers import SentenceTransformer
import PyPDF2

file_path: Path = Path(__file__)


def read_file(file_path) -> str:
    """
    Read file content from .txt or .pdf.
    """
    if file_path.suffix.lower() == ".txt":
        return file_path.read_text(encoding="utf-8")

    elif file_path.suffix.lower() == ".pdf":
        text = ""
        with file_path.open(mode="rb") as f:
            reader = PyPDF2.PdfReader(stream=f)

            for page in reader.pages:
                page_text: str = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    else:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")


def clean_text(text: str) -> str:
    """
    Remove sections like 'Bibliography' or 'References' if present.
    """
    match: re.Match[str] | None = re.search(
        pattern=r"(Bibliography|References)", string=text, flags=re.IGNORECASE
    )
    return text[: match.start()] if match else text


def chunk_text(text: str, max_chunk_length: int = 2500) -> list:
    """
    Split text into smaller chunks; for RAG, shorter chunks are easier to retrieve.
    """
    paragraphs: list[str] = text.split(sep="\n")
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) + 1 > max_chunk_length:
            chunks.append(current_chunk.strip())
            current_chunk: str = para + "\n"
        else:
            current_chunk += para + "\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def embed_chunks(chunks: list, embedder) -> np.ndarray:
    """
    Compute embedding for each chunk.
    """
    return np.array(object=[embedder.encode(chunk) for chunk in chunks])


def retrieve_relevant_chunks(
    query: str, chunks: list, chunk_embeddings: np.ndarray, embedder, top_k: int = 3
) -> list:
    """
    Retrieve top_k chunks that are most similar to the query.
    """
    query_embedding = embedder.encode(query)
    norms = np.linalg.norm(x=chunk_embeddings, axis=1) * np.linalg.norm(
        x=query_embedding
    )
    similarities = np.dot(a=chunk_embeddings, b=query_embedding) / (norms + 1e-10)
    top_indices = np.argsort(a=similarities)[-top_k:][::-1]
    return [chunks[i] for i in top_indices]


def rag_summarize(document_text: str, query: str) -> str:
    """
    Given a document and a query, retrieve top relevant chunks and use them to prompt the LLM.
    """
    cleaned_text: str = clean_text(text=document_text)
    chunks = chunk_text(text=cleaned_text)
    print(f"Document split into {len(chunks)} chunks.")

    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embed_chunks(chunks=chunks, embedder=embedder)
    relevant_chunks = retrieve_relevant_chunks(
        query=query,
        chunks=chunks,
        chunk_embeddings=embeddings,
        embedder=embedder,
        top_k=3,
    )

    context = "\n".join(relevant_chunks)

    prompt = (
        f"Question: {query}\n\nContext:\n{context}\n\n"
        "Answer concisely based on the context:"
    )

    response = ollama.generate(model="gemma3:4b", prompt=prompt)
    return response.get("response", "").strip()


def process_file(
    file_path: Path, output_folder: Path, query: str
) -> None | tuple[str, str]:
    """
    Process a file using RAG: read the file, summarize it,
    save the summary as a .txt file, and return (filename, summary).
    """
    try:
        text: str = read_file(file_path=file_path)

    except Exception as e:
        print(f"Error reading {file_path.name}: {e}")
        return None

    try:
        answer: str = rag_summarize(document_text=text, query=query)
        output_file: Path = output_folder / f"{file_path.stem}_rag_answer.txt"
        output_file.write_text(data=answer, encoding="utf-8")

        print(f"RAG answer for {file_path.name} saved to {output_file}")
        return file_path.name, answer

    except Exception as e:
        print(f"Error summarizing {file_path.name}: {e}")
        return None


def main() -> None:
    input_folder = Path("input")
    output_folder = Path("output_rag")
    output_folder.mkdir(exist_ok=True)

    query = "Summarize the key points of this document or the main argument."

    files: list[Path] = (
        list(input_folder.glob(pattern="*.txt"))
        + list(input_folder.glob(pattern="*.pdf"))
        + list(input_folder.glob(pattern="*.PDF"))
    )

    if not files:
        print("No supported files found in the input folder.")
        return

    results = []

    for file in files:
        print(f"\nProcessing file: {file.name} with RAG.")
        result: None | tuple[str, str] = process_file(
            file_path=file, output_folder=output_folder, query=query
        )
    #     if result:
    #         results.append(result)

    # if results:
    #     df = pd.DataFrame(results, columns=["Filename", "Summary"])
    #     excel_path = output_folder / "summaries.xlsx"
    #     df.to_excel(excel_path, index=False)
    #     print(f"\nAll summaries saved to {excel_path}")


if __name__ == "__main__":
    main()
