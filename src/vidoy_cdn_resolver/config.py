USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
)

def get_initial_headers(host_name: str) -> dict:
    """
    Menyiapkan header awal untuk permintaan halaman video.

    Fungsi ini menyusun header dasar agar permintaan ke server
    terlihat wajar dan dapat diproses dengan baik.

    Args:
        host_name (str): Nama domain target untuk disematkan di header.

    Returns:
        dict: Header awal yang siap dipakai.
    """
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "dnt": "1",
        "Host": host_name,
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": USER_AGENT,
    }

def get_download_headers(host_name: str, referer_host: str) -> dict:
    """
    Menyiapkan header untuk proses pengunduhan media.

    Fungsi ini menambahkan referer dan pengaturan lain yang dibutuhkan
    agar server CDN menerima permintaan unduhan.

    Args:
        host_name (str): Nama domain target dari CDN.
        referer_host (str): Nama domain referer asal.

    Returns:
        dict: Header unduhan yang siap digunakan.
    """
    return {
        "Accept": "*/*",
        "Accept-Language": "id,id-ID;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "identity;q=1, *;q=0",
        "Referer": f"https://{referer_host}/",
        "Connection": "keep-alive",
        "Host": host_name,
        "Range": "bytes=0-",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Dest": "video",
        "Sec-Fetch-Mode": "no-cors",
        "User-Agent": USER_AGENT,
        "Sec-Fetch-Storage-Access": "active",
    }