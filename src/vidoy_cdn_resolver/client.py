import logging
import requests
from . import config

logger = logging.getLogger(__name__)

def fetch_page_content(url: str) -> str:
    """
    Mengambil konten halaman dari URL Vidoy.
    Fungsi ini digunakan untuk mengunduh konten awal halaman video yang diberikan.

    Args:
        url (str): URL halaman yang akan diambil.

    Returns:
        str: Konten teks dari halaman tersebut.

    Raises:
        requests.exceptions.RequestException: Jika terjadi error jaringan.
    """
    logger.debug(f"Mengambil konten dari URL: {url}")
    try:
        response = requests.get(url, headers=config.BASE_HEADERS, timeout=30)
        response.raise_for_status()
        logger.info(f"Berhasil mengambil halaman dari: {url}")

        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Gagal mengambil halaman dari {url}: {e}")
        raise requests.exceptions.RequestException(f"Gagal mengambil halaman dari {url}: {e}") from e

def fetch_embed_details(video_id: str) -> str:
    """
    Mengambil konten halaman embed berdasarkan ID video.
    Fungsi ini mengakses endpoint internal Vidoy untuk mendapatkan metadata video.

    Args:
        video_id (str): ID unik dari video yang diminta.

    Returns:
        str: Konten teks dari halaman embed.

    Raises:
        requests.exceptions.RequestException: Jika terjadi error jaringan.
    """
    params = {'id': video_id, 'bucket': 'temporary'}
    logger.debug(f"Mengambil detail embed untuk ID video: {video_id}")
    try:
        response = requests.get(
            config.EMBED_URL,
            params=params,
            headers=config.EMBED_HEADERS,
            timeout=30
        )
        response.raise_for_status()
        logger.info(f"Berhasil mengambil detail embed untuk ID: {video_id}")

        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Gagal mengambil detail embed untuk ID {video_id}: {e}")
        raise requests.exceptions.RequestException(f"Gagal mengambil detail embed untuk ID {video_id}: {e}") from e