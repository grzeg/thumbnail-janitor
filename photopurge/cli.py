import argparse
import sys

from .core import ALBUM_NAME, find_small_photos, delete_photos


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="photopurge", description=__doc__)
    ap.add_argument("--max-kb", type=float, default=100, help="prog w kB (1 kB = 1000 B)")
    ap.add_argument("--delete", action="store_true", help="naprawde usun (bez tego dry-run)")
    ap.add_argument("--include-videos", action="store_true")
    ap.add_argument("--library", default=None, help="sciezka do .photoslibrary")
    args = ap.parse_args(argv)

    found = find_small_photos(int(args.max_kb * 1000), args.include_videos, args.library)
    total = sum(c.size_bytes for c in found)
    print(f"Do usuniecia (<{args.max_kb:g} kB): {len(found)} | razem {total / 1e6:.1f} MB")
    for c in found[:50]:
        print(f"  {c.size_bytes / 1000:7.1f} kB  {(c.date or '?')[:10]}  {c.filename}  {c.uuid}")
    if len(found) > 50:
        print(f"  ... i {len(found) - 50} wiecej")

    if not found:
        return 0
    if not args.delete:
        print("\nDRY-RUN. Dodaj --delete zeby usunac.")
        return 0
    if input(f"\nUsunac {len(found)} elementow? Wpisz 'tak': ").strip().lower() != "tak":
        print("Przerwano.")
        return 1

    done, failed, method = delete_photos(c.uuid for c in found)
    for u, err in failed.items():
        print(f"  blad {u}: {err}")
    if method == "deleted":
        print(f"Gotowe. Usunieto: {len(done)}, bledy: {len(failed)}. Zobacz 'Ostatnio usuniete'.")
    else:
        print(f"Wrzucono do albumu '{ALBUM_NAME}': {len(done)}, bledy: {len(failed)}.")
        print("W Photos otworz ten album, Cmd+A, potem Cmd+Delete i potwierdz.")
    return 0 if not failed else 2


if __name__ == "__main__":
    sys.exit(main())
