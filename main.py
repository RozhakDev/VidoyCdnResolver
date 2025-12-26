import logging
import typer
import json
from dataclasses import asdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing_extensions import Annotated

from src.vidoy_cdn_resolver import resolver
from src.vidoy_cdn_resolver.logging_config import setup_logging

# Inisialisasi objek Typer dan Rich Console
app = typer.Typer(
    name="vidoy-resolver",
    help="Sebuah CLI untuk me-resolve URL CDN dari halaman video Vidoy.",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()
logger = logging.getLogger(__name__)

@app.command(
    help="Resolve URL video untuk mendapatkan judul, thumbnail, dan URL CDN direct."
)
def main(
    url: Annotated[
        str,
        typer.Argument(
            ...,
            help="URL lengkap halaman video yang ingin di-resolve.",
            metavar="PAGE_URL",
        ),
    ],
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Tampilkan output debug yang lebih detail.",
        ),
    ] = False,
    raw: Annotated[
        bool,
        typer.Option(
            "--raw",
            help="Tampilkan output mentah dalam format JSON.",
        ),
    ] = False,
):
    """
    Menjalankan resolver Vidoy melalui antarmuka CLI.
    Fungsi ini menjadi titik masuk utama aplikasi dan mengatur alur ekstraksi
    serta tampilan hasil kepada pengguna.

    Args:
        url (str): URL halaman video yang ingin di-resolve.
        verbose (bool): Jika True, tampilkan log level DEBUG.
        raw (bool): Jika True, tampilkan hasil dalam format JSON mentah.
    """
    setup_logging(is_verbose=verbose)

    try:
        details = resolver.resolve(url)

        if raw:
            details_dict = asdict(details)
            console.print(json.dumps(details_dict, indent=2))
        else:
            table = Table(
                title=f"[bold green]Hasil untuk ID Video: {details.video_id}[/bold green]",
                show_header=False,
                border_style="blue",
            )
            table.add_column("Field", style="cyan", no_wrap=True)
            table.add_column("Value", style="green")

            table.add_row("Judul", details.title or "Tidak ditemukan")
            table.add_row("Thumbnail", details.thumbnail_url or "Tidak ditemukan")

            cdn_url_text = Text(details.cdn_url or "Tidak ditemukan", style="bold magenta")
            table.add_row("URL CDN", cdn_url_text)

            console.print(table)
    except Exception as e:
        logger.exception("Terjadi kesalahan saat menjalankan proses resolve.")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()