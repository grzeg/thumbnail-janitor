# thumbnail-janitor 🧹📸

> Bo kolejne 400 zdjęć cioci Krysi z wesela kuzyna samo się nie usunie.
> *Because 400 more photos of Aunt Krysia from your cousin's wedding won't delete themselves.*

Skrypt (osxphotos) do masowego usuwania **małych zdjęć** (domyślnie < 100 kB) z Apple Photos:
miniatury, screenshoty, memy z WhatsAppa, przesłane „w jakości Messengera" fotki z imprez.
Zamiast klikać je po jednym w Photos, odpalasz jedną komendę.

Zbudowane z Claude Code. Tak, serio używam go do porządków w rodzinnych zdjęciach.

## Użycie

```bash
pip install -r requirements.txt

python -m photopurge                 # dry-run: tylko lista, nic nie kasuje
python -m photopurge --delete        # usuwa po potwierdzeniu ("tak")
python -m photopurge --max-kb 50 --include-videos
```

- Usunięte trafiają do **„Ostatnio usunięte"** (30 dni na ratunek).
- Przy iCloud Photos usunięcie zniknie też z innych urządzeń.
- Przy pierwszym uruchomieniu macOS zapyta o zgodę na sterowanie Photos (AppleScript).
- Domyślnie dry-run. Przejrzyj listę, zanim dasz `--delete`.

## Architektura (furtka pod UI)

```
photopurge/
  core.py   # find_small_photos(), delete_photos() - zero print/input, zwraca dataclass
  cli.py    # cienka warstwa terminalowa
```

`core.py` nie wie nic o terminalu. `Candidate.to_dict()` daje JSON, a `delete_photos()`
przyjmuje `on_progress`, więc UI można dopiąć bez ruszania logiki.

## Roadmap

- [ ] UI: lokalny serwer (FastAPI) + siatka miniatur z checkboxami i suwakiem progu kB
- [ ] Podgląd zdjęcia przed usunięciem, „zachowaj to" jako wyjątek
- [ ] Filtry: album, rok, osoba („wesele Kasi 2019")
- [ ] Eksport listy do CSV przed usunięciem
- [ ] Testy `core` na zamockowanym `osxphotos`

## Licencja

MIT
