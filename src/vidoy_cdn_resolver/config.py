# Host utama layanan Vidoy.
# Silakan sesuaikan nilai ini jika Anda menggunakan host/domain Vidoy yang berbeda.
HOST_NAME = ""

# User-Agent yang akan digunakan untuk semua permintaan HTTP.
USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 13; 21091116AG) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36"
)

# URL dasar untuk layanan embed Vidoy.
EMBED_URL = f"https://{HOST_NAME}/embed.php"

# Header default untuk permintaan HTTP.
BASE_HEADERS = {
    "User-Agent": USER_AGENT,
}

# Header yang diperlukan khusus untuk mengambil detail embed.
EMBED_HEADERS = {
    "User-Agent": USER_AGENT,
    "Referer": f"https://{HOST_NAME}/",
    "Host": HOST_NAME,
}