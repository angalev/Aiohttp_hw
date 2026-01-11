from pydantic import BaseModel, field_validator

class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    owner: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str):
        if len(v.strip()) == 0:
            raise ValueError("title cannot be empty")
        if len(v) > 100:
            raise ValueError("title is too long")
        return v.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str):
        if len(v.strip()) == 0:
            raise ValueError("description cannot be empty")
        return v.strip()

    @field_validator("owner")
    @classmethod
    def validate_owner(cls, v: str):
        if len(v.strip()) == 0:
            raise ValueError("owner cannot be empty")
        if len(v) > 50:
            raise ValueError("owner name is too long")
        return v.strip()


def validate(schema, json_data: dict):
    try:
        schema_instance = schema(**json_data)
        return schema_instance.model_dump()
    except Exception as e:
        raise HttpError(400, e.errors())