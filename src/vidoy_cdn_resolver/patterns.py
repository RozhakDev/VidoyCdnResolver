import re

# Pola untuk mengekstrak ID video dari dalam tag <script>.
VIDEO_ID_PATTERN = re.compile(r'var id = ["\'](.*?)["\'];')

# Pola untuk mengekstrak judul halaman dari tag <title>.
TITLE_PATTERN = re.compile(r'<title>(.*?)</title>')

# Pola untuk mengekstrak URL sumber video dari tag <source>.
SOURCE_PATTERN = re.compile(r'<source src="([^"]+)"')

# Pola untuk mengekstrak URL thumbnail/poster dari atribut 'poster'.
POSTER_PATTERN = re.compile(r'poster="([^"]+)"')