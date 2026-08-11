import logging
import requests
import re
import codecs
from urllib.parse import urlparse
from typing import Tuple

from . import config

logger = logging.getLogger(__name__)

class VidoyClient:
    """
    Menangani pengambilan data dari halaman Vidoy.
    """
    def __init__(self):
        """
        Mempersiapkan sesi HTTP untuk klien baru.

        Sesi ini dipakai ulang agar header dan kuki tetap konsisten
        selama alur resolusi berjalan.
        """
        self.session = requests.Session()

    def fetch_initial_details(self, video_url: str, host_name: str) -> Tuple[str, str, str, str, str]:
        """
        Mengambil detail awal dari halaman video.

        Fungsi ini memuat halaman utama untuk membaca sumber iframe,
        ID iframe, dan token embed yang dibutuhkan tahap berikutnya.
        Jika halaman awal adalah redirect JS, URL dan host yang diperbarui
        juga ikut dikembalikan.

        Args:
            video_url (str): Tautan video target.
            host_name (str): Nama domain dari tautan.

        Returns:
            Tuple[str, str, str, str, str]: Sumber iframe, ID iframe, token embed,
                URL video aktual (setelah redirect), dan host aktual.

        Raises:
            ValueError: Jika detail gagal ditemukan di halaman.
            requests.exceptions.RequestException: Jika koneksi internet terputus.
        """
        logger.info(f"Membangun sesi kuki untuk host {host_name}...")
        self.session.headers.update(config.get_initial_headers(host_name))
        response = self.session.get(video_url, timeout=30)
        response.raise_for_status()

        response, video_url, host_name = self._follow_js_redirect(response, host_name)

        logger.debug(f"Kuki terkumpul: {self.session.cookies.get_dict()}")

        iframe_src_match = re.search(r"iframe\.src\s*=\s*'/([^']+)\?id='", response.text)
        iframe_src = iframe_src_match.group(1) if iframe_src_match else None
        
        match_id = re.search(r"var\s+iframeId\s*=\s*'(.*?)';", response.text)
        iframeid = match_id.group(1) if match_id else None
        
        embedToken_match = re.search(r"var\s+embedToken\s*=\s*'([^']+)';", response.text)
        embedToken = embedToken_match.group(1) if embedToken_match else None

        if not iframe_src or not iframeid or not embedToken:
            raise ValueError("Gagal mengekstraksi detail iframe dari halaman inisial.")

        return iframe_src, iframeid, embedToken, video_url, host_name

    def _follow_js_redirect(self, response, host_name: str, max_hops: int = 5):
        """
        Mengikuti rantai redirect berbasis JavaScript (setTimeout / window.location.href).

        Beberapa halaman video tidak langsung mengembalikan konten, melainkan
        menampilkan halaman loading dengan JS yang mengalihkan ke URL asli.
        Karena `requests` tidak mengeksekusi JS, kita ekstrak URL tujuan
        secara manual dari pola yang umum digunakan.

        Args:
            response: Objek respons HTTP awal.
            host_name (str): Nama host saat ini.
            max_hops (int): Batas maksimum langkah redirect agar tidak loop.

        Returns:
            Tuple: (response, video_url, host_name) setelah semua redirect diikuti.
        """
        for hop in range(max_hops):
            js_redirect_match = re.search(
                r'window\.location\.href\s*=\s*["\']([^"\']+)["\']',
                response.text
            )
            if not js_redirect_match:
                js_redirect_match = re.search(
                    r'<meta[^>]+http-equiv=["\']refresh["\'][^>]+content=["\']\d+;url=([^"\']+)["\']',
                    response.text,
                    re.IGNORECASE
                )

            if not js_redirect_match:
                break

            redirect_url = js_redirect_match.group(1)
            new_host = urlparse(redirect_url).netloc
            logger.debug(f"Redirect JS terdeteksi (hop {hop + 1}): {redirect_url}")

            self.session.headers.update(config.get_initial_headers(new_host))
            response = self.session.get(redirect_url, timeout=30)
            response.raise_for_status()
            host_name = new_host
            
            video_url = redirect_url
        else:
            logger.warning("Batas maksimum redirect JS tercapai. Melanjutkan dengan respons terakhir.")

        return response, video_url, host_name

    def fetch_player_path(self, iframe_src: str, iframeid: str, embedToken: str, video_url: str, host_name: str) -> Tuple[str, str]:
        """
        Mengambil path pemutar dari halaman iframe.

        Fungsi ini memakai sesi yang sudah terbentuk untuk membaca
        jalur internal yang mengarah ke pemutar video.

        Args:
            iframe_src (str): Endpoint sumber iframe.
            iframeid (str): Pengidentifikasi unik iframe.
            embedToken (str): Token otorisasi.
            video_url (str): URL video asli.
            host_name (str): Nama domain.

        Returns:
            Tuple[str, str]: Path pemutar dan URL iframe lengkap.

        Raises:
            ValueError: Jika path pemutar tidak ditemukan.
            requests.exceptions.RequestException: Jika koneksi internet terputus.
        """
        logger.info("Mengambil metadata iframe melalui sesi terotorisasi...")
        cookie_string = "; ".join([f"{k}={v}" for k, v in self.session.cookies.get_dict().items()])
        self.session.headers.update({
            "Cookie": cookie_string,
            "Sec-Fetch-Site": "same-origin",
            "Referer": video_url,
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "iframe",
        })
        iframe_url = f"https://{host_name}/{iframe_src}?id={iframeid}&t={embedToken}"
        response = self.session.get(iframe_url, timeout=30)
        response.raise_for_status()

        playerPath_match = re.search(r'playerPath\s*=\s*"(.*?)";', response.text)
        if not playerPath_match:
            raise ValueError("Gagal mengekstraksi playerPath dari respons iframe.")
        
        playerPath = codecs.decode(playerPath_match.group(1), 'unicode_escape')
        return playerPath, iframe_url

    def fetch_embed_url(self, playerPath: str, iframe_url: str) -> str:
        """
        Mengambil URL CDN dari pemutar video.

        Fungsi ini membaca respons pemutar untuk menemukan tautan
        media asli yang bisa diproses lebih lanjut.

        Args:
            playerPath (str): Endpoint skrip pemutar internal.
            iframe_url (str): URL referer iframe.

        Returns:
            str: URL CDN mentah yang siap diunduh.

        Raises:
            ValueError: Jika tautan tidak berhasil ditemukan.
            requests.exceptions.RequestException: Jika koneksi internet terputus.
        """
        logger.info("Mengekstraksi aliran media CDN mentah...")
        self.session.headers.update({
            "Referer": iframe_url,
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Dest": "empty",
        })
        response = self.session.get(playerPath, timeout=30)
        response.raise_for_status()

        match = re.search(r'src="(https://[^"]+)"', response.text)
        if not match:
            raise ValueError("URL Embed tidak ditemukan dalam muatan pemutar.")
        
        return match.group(1)