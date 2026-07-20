import requests
import logging
import os
from urllib.parse import urlparse
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from . import config

logger = logging.getLogger(__name__)

def download_video(url: str, host_name: str, output_path: str = "video.mp4") -> bool:
    """
    Mengunduh video ke penyimpanan lokal.

    Fungsi ini mengambil aliran media dari CDN lalu menuliskannya
    ke berkas sambil menampilkan progress yang sederhana.

    Args:
        url (str): Tautan media sumber dari server CDN.
        host_name (str): Nama host referer asal.
        output_path (str): Lokasi dan nama berkas tujuan.

    Returns:
        bool: True jika unduhan selesai dengan baik.
    """
    logger.info(f"Mempersiapkan pengunduhan aliran media menuju: {output_path}")
    try:
        cdn_host = urlparse(url).netloc
        download_headers = config.get_download_headers(host_name=cdn_host, referer_host=host_name)
        
        with requests.get(url, headers=download_headers, stream=True, timeout=30) as response:
            response.raise_for_status()
            
            total_size = int(response.headers.get("content-length", 0))
            
            if total_size == 0:
                logger.warning("Content-Length tidak ditemukan; akurasi progres mungkin menurun.")
            
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
                
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
                        progress.update(task, advance=len(chunk))
                        
        logger.info(f"Urutan pengunduhan selesai dengan sukses: {output_path}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Kesalahan jaringan selama urutan pengunduhan: {e}")
        return False
    except IOError as e:
        logger.error(f"Kegagalan IO saat menyimpan berkas media: {e}")
        return False