from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RoundingValue: int = 2
    DigitGroup: bool = True
    AppTheme: str = "Auto"
