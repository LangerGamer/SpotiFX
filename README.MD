# 🎧 SpotiFX

<div align="center">

<img src="https://via.placeholder.com/200x200.png?text=SpotiFX" alt="SpotiFX Logo" width="200"/>

### Your Ultimate Spotify Music Downloader

[![Version](https://img.shields.io/badge/version-3.2.1-00BFFF?style=for-the-badge&logo=github)](https://github.com/AmirVoid12/SpotiFX)
[![Python](https://img.shields.io/badge/python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-22B573?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/AmirVoid12/SpotiFX?style=for-the-badge&color=yellow&logo=github)](https://github.com/AmirVoid12/SpotiFX/stargazers)

*Transform how you enjoy music with SpotiFX - Download your favorite tracks, albums, and playlists in premium quality*

[✨ Features](#-features) • [🚀 Installation](#-installation) • [🎮 Usage](#-usage) • [📸 Screenshots](#-screenshots) • [⚙️ Config](#%EF%B8%8F-configuration) • [❓ FAQ](#-faq)

</div>

---

## ✨ Features

<div align="center">

<table>
<tr>
<td align="center" width="33%">
<h3>🎵 Full Music Library</h3>
Download tracks, albums and entire playlists from Spotify
</td>
<td align="center" width="33%">
<h3>🔊 Premium Quality</h3>
Get your music in high-definition 320kbps MP3 format
</td>
<td align="center" width="33%">
<h3>📊 Visual Tracking</h3>
Real-time progress bars with estimated completion time
</td>
</tr>
<tr>
<td align="center" width="33%">
<h3>🖼️ Rich Metadata</h3>
Complete with album artwork, artist info, and lyrics
</td>
<td align="center" width="33%">
<h3>⚡ Parallel Processing</h3>
Download multiple tracks simultaneously
</td>
<td align="center" width="33%">
<h3>📱 CLI Support</h3>
Powerful command-line options for automation
</td>
</tr>
</table>

</div>

## 🌟 More Highlights

- **📂 Smart Organization** - Files automatically sorted by artist and album
- **🔍 Spotify Search** - Find and download music without leaving the app
- **📝 Track History** - Complete log of all downloaded music
- **⚙️ Full Customization** - Configure every aspect of your downloads
- **💨 Cache System** - Blazing fast operation with smart caching
- **📦 Batch Processing** - Handle multiple downloads with a single command

## 🚀 Installation

### Prerequisites

- 🐍 Python 3.6 or higher
- 🔑 Spotify Developer API credentials
- 🎬 FFmpeg (for audio conversion)

### One-Line Setup

```bash
git clone https://github.com/AmirVoid12/SpotiFX.git && cd SpotiFX && pip install -r requirements.txt
```

<details>
<summary><b>🔐 Getting Spotify API Credentials</b></summary>

1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Sign in with your Spotify account
3. Create a new app (any name works)
4. Copy your Client ID and Client Secret
5. Enter these when SpotiFX prompts you on first run

</details>

## 🎮 Usage

### Quick Start

```bash
# Launch the interactive interface
python spotifx.py
```

### Command-Line Magic

```bash
# Download a specific track
python spotifx.py -t https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT

# Grab an entire album
python spotifx.py -a https://open.spotify.com/album/0JGOiO34nwfUdDrD612dOp

# Download a playlist
python spotifx.py -p https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M

# Specify where to save files
python spotifx.py -t spotify:track:4cOdK2wGLETKBW3PvgPWqT -d ~/Music/SpotiFX
```

### Batch Processing

Create a file containing URLs (one per line):

```
https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT
https://open.spotify.com/album/0JGOiO34nwfUdDrD612dOp
spotify:playlist:37i9dQZF1DXcBWIGoYBM5M
```

Then use the interactive batch downloader or:

```bash
# Process the file through the menu system
python spotifx.py
# Then select "Batch Download" → "Download from file"
```

## 📸 Screenshots

<div align="center">

<!-- Main screenshot -->
<img src="https://via.placeholder.com/1000x600.png?text=SpotiFX+Main+Interface" width="90%" alt="SpotiFX Main Interface"/>
<p><i>Modern interactive interface with color-coded menus</i></p>

<table>
<tr>
<td width="50%">
<img src="https://via.placeholder.com/600x350.png?text=Download+Progress" width="100%" alt="Download Progress"/>
<p align="center"><i>Real-time download tracking</i></p>
</td>
<td width="50%">
<img src="https://via.placeholder.com/600x350.png?text=Music+Library" width="100%" alt="Music Library View"/>
<p align="center"><i>Organized music collection</i></p>
</td>
</tr>
</table>

</div>

## ⚙️ Configuration

SpotiFX automatically creates a config file at `~/.spotifx/config.ini` with these customizable settings:

| Category | Setting | Description | Default |
|:--------:|:--------|:------------|:-------:|
| 📁 **General** | `download_dir` | Where to save your music | `~/SpotiFX_Downloads` |
| | `concurrent_downloads` | Simultaneous downloads | `3` |
| | `auto_update_check` | Check for new versions | `true` |
| 🔊 **Audio** | `audio_quality` | Bitrate (kbps) | `320` |
| | `audio_format` | File format | `mp3` |
| | `normalize_audio` | Consistent volume | `true` |
| | `embed_cover_art` | Add album covers | `true` |
| 🎵 **Spotify** | `create_playlist_folders` | Separate playlist directories | `true` |
| | `region` | Content region | `US` |
| 🎞️ **YouTube** | `prefer_official_audio` | Prioritize official sources | `true` |
| | `force_ipv4` | Use IPv4 for connections | `true` |

## 🔮 Roadmap

- [x] Core downloading engine
- [x] Album & playlist support
- [x] Metadata embedding
- [x] Concurrent downloads
- [ ] Web interface
- [ ] Mobile companion app
- [ ] Audio fingerprinting
- [ ] Podcast support
- [ ] Music library management

## ❓ FAQ

<details>
<summary><b>Is SpotiFX legal?</b></summary>

SpotiFX is developed for educational and personal use only. The app doesn't store or distribute copyrighted content directly. Users should respect copyright laws and support artists by purchasing music or using paid streaming services.
</details>

<details>
<summary><b>How does SpotiFX work?</b></summary>

SpotiFX uses the Spotify API to gather track information and metadata, then finds matching audio from publicly available sources on YouTube. The downloaded content is processed, tagged with the original metadata, and saved to your device.
</details>

<details>
<summary><b>Why are my downloads failing?</b></summary>

Common issues include network problems, outdated dependencies, or incorrect API credentials. Try using the built-in troubleshooting menu or check your internet connection. Make sure your Spotify API credentials are correct and that you have FFmpeg installed.
</details>

<details>
<summary><b>Can I contribute to SpotiFX?</b></summary>

Absolutely! Contributions are welcome - from code improvements to documentation updates. See our [Contributing Guidelines](https://github.com/AmirVoid12/SpotiFX/wiki/Contributing) for more information.
</details>

## 📜 License

SpotiFX is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙌 Acknowledgements

- [Spotipy](https://spotipy.readthedocs.io/) - Spotify Web API client library
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube download library
- [Mutagen](https://mutagen.readthedocs.io/) - Audio metadata handling
- [Colorama](https://pypi.org/project/colorama/) - Terminal text styling

## 👨‍💻 Author

**Amir.Void** - [GitHub](https://github.com/AmirVoid12)

---

<div align="center">

<img src="https://via.placeholder.com/800x100.png?text=SpotiFX" width="60%" alt="SpotiFX Banner"/>

If you enjoy SpotiFX, please consider giving it a ⭐ star on GitHub!

</div>