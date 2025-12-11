"""
Configuration module for the URL Shortener.
Loads environment variables from .env located in the project root.
"""

import os
import string
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables from the project root `.env`
_env_path = Path(__file__).resolve().parents[2] / ".env"
if _env_path.exists():
    load_dotenv(dotenv_path=_env_path)
else:
    load_dotenv()


@dataclass(frozen=True)
class Config:
    """
    Immutable configuration values for the URL Shortener.

    Attributes:
        SHORT_CODE_LENGTH (int): Length of the generated short code.
        APP_TTL_HOURS (int): Lifetime (in hours) assigned to shortened URLs.
    """

    SHORT_CODE_LENGTH: int = int(os.getenv("SHORT_CODE_LENGTH", "6"))
    SHORT_CODE_MAX_ATTEMPTS: int = int(os.getenv("SHORT_CODE_MAX_ATTEMPTS", "10"))
    APP_TTL_HOURS: int = int(os.getenv("APP_TTL_HOURS", "24"))

    @property
    def short_code_alphabet(self) -> str:
        """
        Returns the Base62 alphabet used for generating short codes.

        Returns:
            str: Alphabet containing a-zA-Z0-9 characters.
        """
        return string.ascii_letters + string.digits


config = Config()


