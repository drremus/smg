from pydantic import BaseModel, Field


class Sentence(BaseModel):
    id: int = Field(gt=0, lt=2**64)
    text: str = Field(description="text contained in the sentence")

    class Config:
        schema_extra = {
            "example": {
                "id": 10,
                "text": "super movie title",
            }
        }

class SentenceWithCypher(Sentence):
    cyphered_text: str = Field(description="cyphered text with rot13")
    
    class Config:
        schema_extra = {
            "example": {
                "id": 10,
                "text": "super movie title",
                "cyphered_text": "fhcre zbivr gvgyr",
            }
        }
