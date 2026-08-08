from pydantic import BaseModel,Field

class RAGQueryRequest(BaseModel):
    question:str=Field(
        ...,
        min_length=1,
        max_length=4000
    )


class RAGQueryResponse(BaseModel):
    answer:str
    sources:list[RAGSource]


class RAGSource(BaseModel):
    document_id:int
    filename:str
    page:int | None=None