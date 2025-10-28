# AI-Powered RAG Application for Automated Dividend Data Extraction

This project is an end-to-end **RAG (Retrieval-Augmented Generation)** based application designed to automate the extraction of **dividend-related information** from large Business Development Company (BDC) PDF reports.  

Financial analysts previously had to manually read through lengthy documents to extract dividend data — a time-consuming and error-prone process. This solution automates the workflow, enabling instant access to structured insights with high accuracy.

---

## Project Overview

The system ingests PDF reports, processes and indexes the content, and enables users to query dividend-related information using natural language. The application uses a hybrid RAG architecture with vector search + LLM reasoning to extract precise and context-aware responses.

### **Key Outcomes**
- Fully automated extraction of dividend information from BDC PDF reports
- Reduced manual effort and analyst workload to near-zero
- Faster data access with higher accuracy and consistency
- Converts unstructured PDFs into structured, query-ready data

---

## System Architecture

```mermaid
flowchart LR
A[PDF Upload] --> B[PyMuPDF Text Extraction]
B --> C[Embeddings via Google text-embedding-004]
C --> D[Chroma DB Vector Store]
D --> E[LangChain Retrieval Pipeline]
E --> F[LLM Response Generation Gemini 2.0 Flash]
F --> G[FastAPI Endpoint]

