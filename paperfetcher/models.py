from typing import List, Optional, TypedDict

class AuthorAffiliation(TypedDict):
    name: str
    affiliation: str
    is_non_academic: bool
    company: Optional[str]

class PaperRecord(TypedDict):
    pubmed_id: str
    title: str
    publication_date: str
    authors: List[AuthorAffiliation]
    corresponding_author_email: Optional[str]