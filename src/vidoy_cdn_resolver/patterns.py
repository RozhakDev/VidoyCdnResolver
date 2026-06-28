import re

# Pola untuk mengekstrak nama host dan ID video dari tautan (URL) embed.
VIDEO_ID_PATTERN = re.compile(r'https?://([^/]+)/[ed]/([a-zA-Z0-9_-]+)')

# Pola untuk mengekstrak judul halaman dari tag <title>.
TITLE_PATTERN = re.compile(r'<title>(.*?)</title>')

# Pola untuk mengekstrak URL sumber video dari tag <source>.
SOURCE_PATTERN = re.compile(r'<source src="([^"]+)"')

# Pola untuk mengekstrak URL thumbnail/poster dari atribut 'poster'.
POSTER_PATTERN = re.compile(r'poster="([^"]+)"')