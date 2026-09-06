import logging
import re
from dataclasses import dataclass
from typing import Optional
from . import client

logger = logging.getLogger(__name__)

@dataclass
class VideoDetails:
    """
    Menyimpan ringkasan informasi video.

    Struktur ini memuat ID, host, judul, thumbnail, dan URL CDN
    agar hasil resolusi mudah dipakai kembali.
    """
    video_id: str
    host_name: str
    actual_host: Optional[str] = None
    title: Optional[str] = None
    thumbnail_url: Optional[str] = None
    cdn_url: Optional[str] = None

def resolve(page_url: str) -> VideoDetails:
    """
    Menjalankan alur resolusi dari URL video.

    Fungsi ini membaca halaman target, mengambil detail penting,
    lalu menyusun hasil akhirnya dalam bentuk yang rapi.

    Args:
        page_url (str): Tautan halaman video yang dituju.

    Returns:
        VideoDetails: Data video yang sudah dirangkum.

    Raises:
        ValueError: Jika URL tidak valid atau proses penemuan data gagal.
        Exception: Jika terjadi kesalahan teknis yang tidak terduga.
    """
    logger.info("Memulai resolusi URL...")
    
    host_name_match = re.search(r'https?://([^/]+)/', page_url)
    if not host_name_match:
        raise ValueError("Nama host terdeteksi tidak valid pada URL yang diberikan.")
    host_name = host_name_match.group(1)
    
    video_id_match = re.search(r'/[ed]/([a-zA-Z0-9_-]+)', page_url)
    video_id = video_id_match.group(1) if video_id_match else "unknown"

    logger.debug(f"Host Target: {host_name} | ID Target: {video_id}")
    
    details = VideoDetails(video_id=video_id, host_name=host_name)
    
    try:
        vidoy_client = client.VidoyClient()
        
        iframe_src, iframeid, embedToken, page_url, host_name = vidoy_client.fetch_initial_details(page_url, host_name)
        details.actual_host = host_name  # host setelah mengikuti redirect JS
        playerPath, iframe_url = vidoy_client.fetch_player_path(iframe_src, iframeid, embedToken, page_url, host_name)
        embed_url = vidoy_client.fetch_embed_url(playerPath, iframe_url)
        
        details.cdn_url = embed_url
        logger.info("Resolusi URL berhasil.")
        
    except Exception as e:
        logger.error(f"Resolusi URL gagal: {e}")
        raise

    return details