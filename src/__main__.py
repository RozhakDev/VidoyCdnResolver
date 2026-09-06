"""
Titik masuk alternatif proyek saat dijalankan sebagai modul Python.

Berkas ini dibuat agar perintah ``python -m src`` dapat bekerja di lingkungan
dengan resolusi path yang tidak stabil, seperti Termux
dan symlink ``/sdcard`` di Android, tanpa bergantung pada direktori
kerja saat ini.

Penggunaan::

    cd /storage/emulated/0/Download/VidoyCdnResolver
    python -m src "https://streamrizz.com/e/vpd5xiq31hlf" -v
"""
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from main import app

if __name__ == "__main__":
    app()