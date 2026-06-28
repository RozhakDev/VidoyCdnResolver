import requests
import logging
import os
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from . import config

logger = logging.getLogger(__name__)

def download_video(url: str, host_name: str, output_path: str = "video.mp4") -> bool:
    """
    Mengeksekusi proses pengunduhan media dari URL CDN ke penyimpanan lokal.

    Fungsi ini melakukan unduhan secara bertahap (streaming) untuk menjaga
    efisiensi penggunaan memori, serta menerapkan header standar pengunduhan.

    Args:
        url (str): URL sumber CDN langsung.
        host_name (str): Nama host sumber referer video.
        output_path (str): Lokasi dan nama file tujuan penyimpanan.

    Returns:
        bool: True jika berhasil diunduh secara penuh, False jika gagal.
    """
    logger.info(f"Memulai proses unduhan video ke: {output_path}")
    try:
        with requests.get(url, headers=config.get_download_headers(host_name), stream=True, timeout=30) as response:
            response.raise_for_status()
            
            total_size = int(response.headers.get("content-length", 0))
            
            if total_size == 0:
                logger.warning("Ukuran file (Content-Length) tidak diketahui, progress bar tidak dapat ditampilkan dengan akurat.")
            
            with open(output_path, "wb") as f, Progress(
                "[progress.description]{task.description}",
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.1f}%",
                "•",
                DownloadColumn(),
                "•",
                TransferSpeedColumn(),
                "•",
                TimeRemainingColumn(),
            ) as progress:
                
                task = progress.add_task(f"Mengunduh [cyan]{os.path.basename(output_path)}", total=total_size)
                
                for chunk in response.iter_content(chunk_size=1024 * 1024): # Chunk 1MB
                    if chunk:
                        f.write(chunk)
                        progress.update(task, advance=len(chunk))
                        
        logger.info(f"Video berhasil diunduh dan disimpan di: {output_path}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Gagal mengunduh video: {e}")
        return False
    except IOError as e:
        logger.error(f"Gagal menulis atau menyimpan file video: {e}")
        return False