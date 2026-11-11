"""photopurge - znajdz i usun male zdjecia z Photos Library (macOS)."""
from .core import Candidate, find_small_photos, delete_photos

__all__ = ["Candidate", "find_small_photos", "delete_photos"]
