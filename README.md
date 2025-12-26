# VidoyCdnResolver

A lightweight Python CLI tool to resolve CDN and embed video URLs from Vidoy pages, with clean architecture and Rich-powered output.

## ✨ Features

- Resolve **video ID**, **title**, **thumbnail**, and **direct CDN URL**
- Clean CLI powered by **Typer**
- Beautiful terminal output using **Rich**
- Optional **debug logging** and **raw JSON output**

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🚀 Usage

| Command | Description |
|--------|------------|
| `python main.py <PAGE_URL>` | Resolve video page dan tampilkan hasil dengan Rich table |
| `python main.py <PAGE_URL> -v` | Tampilkan verbose debug logs |
| `python main.py <PAGE_URL> --raw` | Output mentah dalam format JSON |

## 🖥 Example Output

With debug enabled:

```bash
python main.py https://videym.pro/e/z40jeu954mk5 -v
```

Result:

* Title
* Thumbnail URL
* Direct CDN URL (ready to use)

See `/screenshot/successful-resolve-with-debug-logs.png` for a full example.

## 📁 Project Structure

```text
VidoyCdnResolver/
├── main.py
├── README.md
├── requirements.txt
├── screenshot/
└── src/
    └── vidoy_cdn_resolver/
```

## ⚠️ Disclaimer

This project is for **educational and research purposes only**. Use responsibly and respect the terms of service of the platform.

## 📄 License

MIT License