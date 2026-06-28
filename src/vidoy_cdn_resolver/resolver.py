import logging
from dataclasses import dataclass
from typing import Optional
from . import client, patterns

logger = logging.getLogger(__name__)

@dataclass
class VideoDetails:
    """
    Menyimpan informasi lengkap tentang video Vidoy.
    Berisi ID video dan metadata opsional seperti judul, thumbnail, dan URL CDN.
    """
    video_id: str
    host_name: str
    title: Optional[str] = None
    thumbnail_url: Optional[str] = None
    cdn_url: Optional[str] = None

def _extract_host_and_id(pattern, text: str) -> tuple[Optional[str], Optional[str]]:
    """
    Mengambil host name dan ID video dari teks.
    """
    match = pattern.search(text)
    if match:
        return match.group(1), match.group(2)
    return None, None

def _extract_match(pattern, text: str) -> Optional[str]:
    """
    Mengambil teks yang cocok dari hasil pencarian pola regex.
    Fungsi ini mencari kecocokan pertama dalam teks dan mengembalikan
    kelompok pertama jika ditemukan.

    Args:
        pattern (re.Pattern): Pola regex yang telah dikompilasi.
        text (str): Teks yang akan dicari kecocokannya.

    Returns:
        Optional[str]: Hasil ekstraksi jika ditemukan, None jika tidak.
    """
    match = pattern.search(text)
    return match.group(1) if match else None

def resolve(page_url: str) -> VideoDetails:
    """
    Menyelesaikan URL Vidoy menjadi detail video lengkap.
    Fungsi ini mengambil halaman awal, mengekstrak ID video, lalu mengambil
    informasi tambahan seperti judul, thumbnail, dan URL CDN dari halaman embed.

    Args:
        page_url (str): URL halaman video asli yang akan di-resolve.

    Returns:
        VideoDetails: Objek berisi ID video dan informasi terkait lainnya.

    Raises:
        ValueError: Jika ID video tidak ditemukan di halaman.
        requests.exceptions.RequestException: Jika terjadi error jaringan.
    """
    logger.info("Memulai proses resolve untuk URL...")
    page_content = client.fetch_page_content(page_url)
    
    logger.info("Mencari ID video di dalam halaman...")
    host_name, video_id = _extract_host_and_id(patterns.VIDEO_ID_PATTERN, page_content)

    if not video_id or not host_name:
        logger.error("Ekstraksi ID video atau Host Name gagal.")
        raise ValueError("Tidak dapat menemukan ID video atau Host Name di URL yang diberikan. "
                         "Pastikan URL valid dan halaman berisi video.")
    
    logger.info(f"ID video ditemukan: {video_id} pada host {host_name}")

    details = VideoDetails(video_id=video_id, host_name=host_name)

    logger.info("Mengambil detail embed...")
    embed_content = client.fetch_embed_details(video_id, host_name)

    logger.info("Mengekstrak judul, thumbnail, dan URL CDN...")
    details.title = _extract_match(patterns.TITLE_PATTERN, embed_content)
    details.thumbnail_url = _extract_match(patterns.POSTER_PATTERN, embed_content)
    details.cdn_url = _extract_match(patterns.SOURCE_PATTERN, embed_content).replace('amp;', '')

    logger.debug(f"Judul: {details.title}")
    logger.debug(f"Thumbnail: {details.thumbnail_url}")
    logger.debug(f"CDN URL: {details.cdn_url}")
    logger.info("Proses resolve selesai.")

    return details