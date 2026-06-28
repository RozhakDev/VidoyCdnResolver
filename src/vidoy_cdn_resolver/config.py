# User-Agent yang akan digunakan untuk semua permintaan HTTP.
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
)

# Header default untuk permintaan HTTP.
BASE_HEADERS = {
    "User-Agent": USER_AGENT,
}

def get_embed_url(host_name: str) -> str:
    """
    Menghasilkan URL lengkap untuk mengakses halaman embed berdasarkan nama host.

    Args:
        host_name (str): Nama host yang didapatkan dari URL sumber.

    Returns:
        str: URL tujuan untuk halaman embed video.
    """
    return f"https://{host_name}/embed.php"

def get_embed_headers(host_name: str) -> dict:
    """
    Merakit header HTTP khusus untuk permintaan ke halaman embed.

    Args:
        host_name (str): Nama host yang didapatkan dari URL sumber.

    Returns:
        dict: Kumpulan header HTTP yang dibutuhkan.
    """
    return {
        "User-Agent": USER_AGENT,
        "Referer": f"https://{host_name}/",
        "Host": host_name,
    }

def get_download_headers(host_name: str) -> dict:
    """
    Menyiapkan header HTTP yang diperlukan untuk mengunduh media dari CDN.

    Args:
        host_name (str): Nama host sumber untuk dijadikan sebagai referer.

    Returns:
        dict: Konfigurasi header lengkap untuk pengunduhan.
    """
    return {
        "Accept-Encoding": "identity;q=1, *;q=0",
        "Accept-Language": "en-US,en;q=0.6",
        "Connection": "keep-alive",
        "Host": "vidoycdn.b-cdn.net",
        "Range": "bytes=0-",
        "Referer": f"https://{host_name}/",
        "Sec-Fetch-Dest": "video",
        "Sec-Fetch-Mode": "no-cors",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-GPC": "1",
        "User-Agent": USER_AGENT,
        "Sec-Fetch-Storage-Access": "none",
    }