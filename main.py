import json
import logging
import sys
from dataclasses import asdict
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typing_extensions import Annotated

_PROJECT_ROOT = Path(__file__).absolute().parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.vidoy_cdn_resolver import downloader, resolver
from src.vidoy_cdn_resolver.logging_config import setup_logging

app = typer.Typer(
    name="vidoy-resolver",
    help="Alat CLI untuk menyelesaikan endpoint media Vidoy CDN.",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()
logger = logging.getLogger(__name__)

@app.command(
    help="Menyelesaikan URL video untuk mendapatkan tautan media CDN mentah beserta metadata."
)
def main(
    url: Annotated[
        str,
        typer.Argument(
            ...,
            help="URL halaman video target secara lengkap.",
            metavar="PAGE_URL",
        ),
    ],
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Aktifkan log awakutu (debug) jaringan secara verbose.",
        ),
    ] = False,
    raw: Annotated[
        bool,
        typer.Option(
            "--raw",
            help="Tampilkan struktur JSON mentah ke standar keluaran.",
        ),
    ] = False,
    download: Annotated[
        bool,
        typer.Option(
            "--download",
            "-d",
            help="Unduh aliran video secara otomatis setelah proses resolusi.",
        ),
    ] = False,
):
    """
    Menjadi titik masuk utama untuk menjalankan aplikasi CLI.
    
    Fungsi ini menerima masukan perintah dari pengguna, mengurai parameter,
    lalu mengarahkan proses menuju resolusi atau pengunduhan video.
    
    Args:
        url (str): URL halaman video yang akan diproses.
        verbose (bool): Menampilkan log yang lebih rinci jika bernilai True.
        raw (bool): Menampilkan keluaran data mentah (JSON) jika bernilai True.
        download (bool): Mengunduh video secara otomatis jika bernilai True.

    Raises:
        typer.Exit: Jika terjadi kegagalan fatal saat aplikasi berjalan.
    """
    setup_logging(is_verbose=verbose)

    try:
        details = resolver.resolve(url)

        if raw:
            details_dict = asdict(details)
            console.print(json.dumps(details_dict, indent=2))
        else:
            table = Table(
                title=f"[bold green]Resolusi Sukses | ID: {details.video_id}[/bold green]",
                show_header=False,
                border_style="blue",
            )
            table.add_column("Properti", style="cyan", no_wrap=True)
            table.add_column("Nilai", style="green")

            table.add_row("Judul", details.title or "N/A")
            table.add_row("Tumbnail", details.thumbnail_url or "N/A")

            display_cdn_url = details.cdn_url or "N/A"
            if display_cdn_url != "N/A" and len(display_cdn_url) > 65:
                display_cdn_url = display_cdn_url[:30] + "..." + display_cdn_url[-30:]
                
            cdn_url_text = Text(display_cdn_url, style="bold magenta")
            table.add_row("Aliran CDN", cdn_url_text)

            console.print(table)
            
        if download and details.cdn_url:
            output_filename = f"{details.video_id}.mp4"
            console.print(f"\n[bold yellow]Info: Memulai proses unduhan ke '{output_filename}'[/bold yellow]")
            referer_host = details.actual_host or details.host_name
            success = downloader.download_video(details.cdn_url, referer_host, output_filename)
            if success:
                console.print(f"[bold green]Sukses: File berhasil disimpan ke '{output_filename}'[/bold green]")
            else:
                console.print("[bold red]Error: Gagal mengunduh file. Periksa log sistem untuk detail lebih lanjut.[/bold red]")
        elif download and not details.cdn_url:
            console.print("[bold red]Dibatalkan: URL CDN tidak ditemukan, proses unduhan dihentikan.[/bold red]")
            
    except Exception as e:
        logger.exception("Terjadi sistem error saat melakukan resolusi URL target.")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()