# VidoyCdnResolver

A smart, terminal-based downloader for Vidoy pages. Resolves CDN links dynamically and streams MP4 videos directly to your disk with a beautiful, distraction-free UI.

## ✨ Features

- **Auto-Download** (`-d` / `--download`) videos to `.mp4` with a beautiful streaming progress bar
- Resolve **video ID**, **title**, **thumbnail**, and **direct CDN URL**
- **Smart & Dynamic Host Resolving** (automatically adapts to domain changes)
- Clean CLI powered by **Typer**
- Beautiful terminal output using **Rich** (automatically crops excessively long URLs)
- Optional **debug logging** and **raw JSON output**

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🚀 Usage

| Command | Description |
|--------|------------|
| `python main.py <PAGE_URL>` | Resolve video page dan tampilkan hasil dengan Rich table |
| `python main.py <PAGE_URL> -d` | **Unduh** video CDN secara otomatis dan simpan sebagai `.mp4` |
| `python main.py <PAGE_URL> -v` | Tampilkan verbose debug logs |
| `python main.py <PAGE_URL> --raw` | Output mentah dalam format JSON |

## 🖥 Example Output

With debug enabled:

```bash
python main.py https://vdko.cc/d/ziw0rdt1h0hh -v
```

Result:

* Title
* Thumbnail URL
* Direct CDN URL (ready to use)
* Automatic `.mp4` download with progress indicator (if `-d` flag is used)

See [`/screenshot/successful-resolve-with-debug-logs.png`](/screenshot/successful-resolve-with-debug-logs.png) for a full example.

## 📁 Project Structure

```text
VidoyCdnResolver/
├── main.py
├── README.md
├── requirements.txt
├── screenshot/
└── src/
```

## ⚠️ Disclaimer

This project is for **educational and research purposes only**. Use responsibly and respect the terms of service of the platform.

## 📄 License

MIT License