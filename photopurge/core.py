"""Logika bez print() i input(). CLI i przyszle UI wołają tylko to."""
from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from typing import Callable, Iterable, Optional

import osxphotos


@dataclass
class Candidate:
    uuid: str
    filename: str
    size_bytes: int
    date: Optional[str]  # ISO string, latwy do JSON
    path: Optional[str]  # None gdy zdjecie tylko w iCloud

    def to_dict(self) -> dict:
        return asdict(self)


def _size(p: osxphotos.PhotoInfo) -> Optional[int]:
    if p.original_filesize:
        return p.original_filesize
    if p.path and os.path.exists(p.path):
        return os.path.getsize(p.path)
    return None


def find_small_photos(
    max_bytes: int = 100_000,
    include_videos: bool = False,
    library: Optional[str] = None,
) -> list[Candidate]:
    """Zwroc zdjecia mniejsze niz max_bytes, od najmniejszych."""
    db = osxphotos.PhotosDB(dbfile=library) if library else osxphotos.PhotosDB()
    out: list[Candidate] = []
    for p in db.photos(movies=include_videos):
        size = _size(p)
        if size is not None and size < max_bytes:
            out.append(
                Candidate(
                    uuid=p.uuid,
                    filename=p.original_filename,
                    size_bytes=size,
                    date=p.date.isoformat() if p.date else None,
                    path=p.path,
                )
            )
    out.sort(key=lambda c: c.size_bytes)
    return out


ALBUM_NAME = "DO USUNIECIA"


def delete_photos(
    uuids: Iterable[str],
    on_progress: Optional[Callable[[int, int, str], None]] = None,
) -> tuple[list[str], dict[str, str], str]:
    """Usun zdjecia po UUID.

    Zwraca (zrobione_uuid, {uuid: blad}, metoda).
    metoda = "deleted": photoscript ma delete(), zdjecia w 'Ostatnio usuniete'.
    metoda = "album":   brak delete(); zdjecia wrzucone do albumu ALBUM_NAME,
                        trzeba je skasowac recznie (Cmd+A, Cmd+Delete w albumie).
    """
    import photoscript  # import tu: core da sie testowac bez macOS

    ids = list(uuids)
    lib = photoscript.PhotosLibrary()
    done: list[str] = []
    failed: dict[str, str] = {}

    if hasattr(lib, "delete"):
        method = "deleted"
        for i, u in enumerate(ids, 1):
            try:
                lib.delete([photoscript.Photo(u)])
                done.append(u)
            except Exception as e:  # noqa: BLE001
                failed[u] = str(e)
            if on_progress:
                on_progress(i, len(ids), u)
        return done, failed, method

    method = "album"
    try:
        album = lib.album(ALBUM_NAME)
    except Exception:  # noqa: BLE001
        album = None
    if album is None:
        album = lib.create_album(ALBUM_NAME)
    for i, u in enumerate(ids, 1):
        try:
            album.add([photoscript.Photo(u)])
            done.append(u)
        except Exception as e:  # noqa: BLE001
            failed[u] = str(e)
        if on_progress:
            on_progress(i, len(ids), u)
    return done, failed, method
