"""The code uses a RAG approach to:
-Break documents into chunks
-Find relevant chunks using embeddings
-Use those chunks to generate focused answers using an LLM
-Save results to individual text files
"""

from typing import Any
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
        text: str = ""
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


def chunk_text(text: str, max_chunk_length: int = 2500) -> list[str]:
    """
    Split text into smaller chunks; for RAG, shorter chunks are easier to retrieve.
    """
    paragraphs: list[str] = text.split(sep="\n")
    chunks: list[str] = []
    current_chunk: str = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) + 1 > max_chunk_length:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n"
        else:
            current_chunk += para + "\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def embed_chunks(chunks: list, embedder: SentenceTransformer) -> np.ndarray:
    """
    Compute embedding for each chunk.
    """
    return np.array(object=[embedder.encode(chunk) for chunk in chunks])


def retrieve_relevant_chunks(
    query: str,
    chunks: list,
    chunk_embeddings: np.ndarray,
    embedder: SentenceTransformer,
    top_k: int = 3,
) -> list:
    """
    Retrieve top_k chunks that are most similar to the query.
    """
    query_embedding = embedder.encode(sentences=query)
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

    # Remove sections like 'Bibliography' or 'References' if present.
    cleaned_text: str = clean_text(text=document_text)

    # Split the cleaned text into smaller chunks.
    chunks: list[str] = chunk_text(text=cleaned_text)
    print(f"Document split into {len(chunks)} chunks.")

    # Compute embeddings for each chunk.
    embedder = SentenceTransformer(model_name_or_path="all-MiniLM-L6-v2")
    embeddings: np.ndarray = embed_chunks(chunks=chunks, embedder=embedder)

    # Retrieve top relevant chunks.
    relevant_chunks: list[str] = retrieve_relevant_chunks(
        query=query,
        chunks=chunks,
        chunk_embeddings=embeddings,
        embedder=embedder,
        top_k=3,
    )

    # Combine the relevant chunks into a context.
    context: str = "\n".join(relevant_chunks)

    # Prompt the LLM with the context and the query.
    prompt: str = (
        f"Question: {query}\n\nContext:\n{context}\n\n"
        "Answer concisely based on the context:"
    )
    response: ollama.GenerateResponse = ollama.generate(
        model="gemma3:4b", prompt=prompt
    )
    return response.get(key="response", default="").strip()


def process_file(
    file_path: Path, output_folder: Path, query: str
) -> None | tuple[str, str]:
    """
    Process a file using RAG: read the file, summarize it,
    save the summary as a .txt file, and return (filename, summary).
    """
    try:
        # Read the file content
        text: str = read_file(file_path=file_path)

    except Exception as e:
        print(f"Error reading {file_path.name}: {e}")
        return None

    try:
        # Summarize the text using RAG
        answer: str = rag_summarize(document_text=text, query=query)

        # Save the summary to a .txt file
        output_file: Path = output_folder / f"{file_path.stem}_rag_answer.txt"
        with open(file=output_file, mode="w", encoding="utf-8") as f:
            f.write(answer)

        print(f"RAG answer for {file_path.name} saved to {output_file}")
        return file_path.name, answer

    except Exception as e:
        print(f"Error summarizing {file_path.name}: {e}")
        return None


def main() -> None:

    # Set input and output folders
    input_folder = Path("input")
    output_folder = Path("output_rag")
    output_folder.mkdir(exist_ok=True)

    # Get all supported files in the input folder
    files: list[Path] = list(input_folder.glob(pattern="*.txt")) + list(
        input_folder.glob(pattern="*.pdf")
    )

    # Check if there are any files to process
    if not files:
        print("No supported files found in the input folder.")
        return

    # Set query for llm
    query = "Summarize the key points of this document or the main argument."

    # Initialize results list
    results: list[tuple[str, str]] = []

    # Process each file
    for file in files:
        print(f"\nProcessing file: {file.name} with RAG.")
        result: None | tuple[str, str] = process_file(
            file_path=file, output_folder=output_folder, query=query
        )
        if result:
            results.append(result)

    # Save summaries to an Excel file
    if results:
        df = pd.DataFrame(data=results, columns=["Filename", "Summary"])
        excel_path: Path = output_folder / "summaries.xlsx"
        df.to_excel(excel_writer=excel_path, index=False)
        print(f"\nAll summaries saved to {excel_path}")


if __name__ == "__main__":
    main()
