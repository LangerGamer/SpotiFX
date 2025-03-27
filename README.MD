# SpotiFX 🎵

<div align="center">
  
![SpotiFX Logo](https://via.placeholder.com/150x150.png?text=SpotiFX)

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/AmirVoid12/SpotiFX)
[![Python](https://img.shields.io/badge/python-3.6%2B-brightgreen.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/AmirVoid12/SpotiFX?style=social)](https://github.com/AmirVoid12/SpotiFX/stargazers)

**The Ultimate Spotify Music Downloader**

*SpotiFX lets you download your favorite Spotify tracks, albums, and playlists for offline listening.*

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Screenshots](#screenshots) • [Configuration](#configuration) • [FAQ](#faq) • [License](#license)

</div>

## 📋 Features

- **🎵 Comprehensive Music Download:** Download tracks, albums, and entire playlists from Spotify
- **🎚️ High-Quality Audio:** Download in up to 320kbps MP3 format
- **📑 Complete Metadata:** Automatic tagging with album art, artist info, and lyrics
- **⏱️ Concurrent Downloads:** Download multiple tracks simultaneously
- **📂 Smart Organization:** Automatically organizes music by artist and album
- **📊 Track Progress:** Visual download progress tracking with ETA
- **⚙️ Customizable Settings:** Configure download quality, location, and more
- **📜 Download History:** Keep track of all downloaded music
- **⚡ Batch Download:** Process multiple URLs at once
- **🔍 Spotify Search:** Find and download music directly from the app
- **💾 Cache System:** Efficient caching for faster repeated operations
- **📱 CLI Support:** Command-line interface for scripting and automation

## 🔧 Installation

### Prerequisites

- Python 3.6+
- Spotify Developer API credentials
- FFmpeg (for audio conversion)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/AmirVoid12/SpotiFX.git
cd SpotiFX

# Install dependencies
pip install -r requirements.txt

# Run SpotiFX
python spotifx.py
```

### Getting Spotify API Credentials

1. Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Create a new application
4. Copy your Client ID and Client Secret
5. Enter these credentials when SpotiFX prompts you

## 🚀 Usage

### Interactive Mode

Simply run the application and follow the interactive menu:

```bash
python spotifx.py
```

### Command Line Mode

Download specific content using command-line options:

```bash
# Download a track
python spotifx.py -t https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT

# Download an album
python spotifx.py -a https://open.spotify.com/album/0JGOiO34nwfUdDrD612dOp

# Download a playlist
python spotifx.py -p https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M

# Specify custom download directory
python spotifx.py -t https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT -d /path/to/downloads
```

### Batch Download

Download multiple items at once by creating a text file with URLs (one per line) and using:

```bash
# Create a file with URLs
echo "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT" > urls.txt
echo "https://open.spotify.com/album/0JGOiO34nwfUdDrD612dOp" >> urls.txt

# Use the batch download menu option
python spotifx.py
# Then select "Batch Download" from the menu
```

## 📸 Screenshots

<div align="center">
  
![Main Menu](https://via.placeholder.com/800x450.png?text=SpotiFX+Main+Menu)
*Main Menu*

![Track Download](https://via.placeholder.com/800x450.png?text=SpotiFX+Track+Download)
*Track Download Progress*

![Download History](https://via.placeholder.com/800x450.png?text=SpotiFX+Download+History)
*Download History*

</div>

## ⚙️ Configuration

SpotiFX stores configuration in `~/.spotifx/config.ini`. You can modify these settings:

| Section | Option | Description | Default |
|---------|--------|-------------|---------|
| General | download_dir | Download directory | ~/SpotiFX_Downloads |
| General | concurrent_downloads | Max simultaneous downloads | 3 |
| Audio | audio_quality | Audio quality (kbps) | 320 |
| Audio | audio_format | Audio format | mp3 |
| Spotify | create_playlist_folders | Create separate folders for playlists | true |
| YouTube | prefer_official_audio | Prefer official audio sources | true |

## 📝 Development Roadmap

- [x] Basic track download
- [x] Album and playlist support
- [x] Concurrent downloads
- [x] Metadata tagging
- [ ] Mobile app integration
- [ ] Remote control functionality
- [ ] Web interface
- [ ] Music library management

## ❓ FAQ

### Is SpotiFX legal?

SpotiFX is developed for educational purposes only. The application does not store or distribute any copyrighted content. It uses publicly available APIs and services. Users should respect copyright laws and artists' rights by supporting them through official channels.

### How does SpotiFX work?

SpotiFX uses Spotify's API to fetch track metadata, then finds corresponding audio from publicly available sources on YouTube. The downloaded content is processed, tagged with the original metadata, and saved to your device.

### My downloads are failing, what should I do?

Check our [Troubleshooting Guide](https://github.com/AmirVoid12/SpotiFX/wiki/Troubleshooting) or use the built-in troubleshooting menu in the application. Common issues include outdated dependencies, incorrect API credentials, or network problems.

### Can I contribute to SpotiFX?

Absolutely! We welcome contributions of all kinds. Please see our [Contributing Guidelines](https://github.com/AmirVoid12/SpotiFX/wiki/Contributing) for more information.

## 📄 License

SpotiFX is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Spotipy](https://spotipy.readthedocs.io/) - Lightweight Python library for the Spotify Web API
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - A youtube-dl fork with additional features
- [Mutagen](https://mutagen.readthedocs.io/) - Python module to handle audio metadata
- [Colorama](https://pypi.org/project/colorama/) - Cross-platform colored terminal text

## 🧑‍💻 Author

**Amir.Void** - [GitHub](https://github.com/AmirVoid12)

---

<div align="center">
  
If you find SpotiFX useful, please consider ⭐ starring the repository on GitHub!

</div>