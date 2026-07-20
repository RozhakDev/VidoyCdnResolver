import logging
import sys
from rich.logging import RichHandler

def setup_logging(is_verbose: bool = False):
    """
    Menyiapkan pengaturan logging aplikasi.

    Fungsi ini mengatur level log dan tampilan konsol agar pesan
    yang muncul tetap rapi dan mudah dibaca.

    Args:
        is_verbose (bool): Aktifkan level DEBUG jika True, atau INFO jika False.
    """
    log_level = "DEBUG" if is_verbose else "INFO"

    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                tracebacks_suppress=[sys.modules.get('typer')],
            )
        ],
    )

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    logging.debug("Sistem logging terpusat berhasil diinisialisasi.")