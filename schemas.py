from pydantic import BaseModel, Field, validator


class UserCreate(BaseModel):
    name: str
    surname: str
    email: str
    eth_address: str
    password: str = Field(min_length=8)

    @validator("password")
    def validate_password_format(cls, value):
        if not (
            any(char.isdigit() for char in value)
            and any(char.isupper() for char in value)
        ):
            raise ValueError(
                "Password must contain at least one digit and one uppercase letter"
            )
        return value


class UserSignIn(BaseModel):
    email: str
    password: str
