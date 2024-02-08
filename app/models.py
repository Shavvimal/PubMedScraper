from pydantic import BaseModel


class PubMedModel(BaseModel):
    pmid: str
    title: str
    abstract: str
    full_text: str
    authors: str

