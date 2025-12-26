import logging
import sys
from rich.logging import RichHandler

def setup_logging(is_verbose: bool = False):
    """
    Menginisialisasi sistem logging terpusat menggunakan RichHandler.
    Konfigurasi ini menghasilkan output log yang rapi di konsol dan menekan
    log berlebihan dari pustaka pihak ketiga seperti requests dan urllib3.

    Args:
        is_verbose (bool): Jika True, level log diatur ke DEBUG.
                           Jika False (bawaan), level log diatur ke INFO.
    """
    log_level = "DEBUG" if is_verbose else "INFO"

    logging.basicConfig(
        level=log_level,
        format="%(message)s",  # Format sederhana, RichHandler akan memperindahnya
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                tracebacks_suppress=[sys.modules['typer']], # Menyembunyikan traceback dari Typer
            )
        ],
    )

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    logging.debug("Logging diinisialisasi dengan level DEBUG.")