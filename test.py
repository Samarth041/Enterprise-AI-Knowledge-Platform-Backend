from app.ai.ingest import ingest_document

count=ingest_document(
    r"uploads\documents\AI Engineering.pdf"
)

print(count)