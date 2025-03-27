# 🎧 SpotiFX

<div align="center">

<!-- Custom SVG logo instead of placeholder image -->
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1DB954" />
      <stop offset="100%" stop-color="#1AA34A" />
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="3" />
      <feOffset dx="0" dy="2" result="offsetblur" />
      <feComponentTransfer>
        <feFuncA type="linear" slope="0.5" />
      </feComponentTransfer>
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>
  <circle cx="100" cy="100" r="90" fill="url(#logoGradient)" filter="url(#shadow)" />
  <g fill="white" transform="translate(50, 50)">
    <!-- Musical notes -->
    <path d="M75,25 C75,25 75,75 75,75 C75,83 68,90 60,90 C52,90 45,83 45,75 C45,67 52,60 60,60 C63,60 66,61 68,62 L68,10 L30,20 L30,85 C30,93 23,100 15,100 C7,100 0,93 0,85 C0,77 7,70 15,70 C18,70 21,71 23,72 L23,5 L75,0 L75,25 Z" />
  </g>
</svg>

### Your Ultimate Spotify Music Downloader

[![Version](https://img.shields.io/badge/version-1.0.0-00BFFF?style=for-the-badge&logo=github)](https://github.com/AmirVoid12/SpotiFX)
[![Python](https://img.shields.io/badge/python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-22B573?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/AmirVoid12/SpotiFX?style=for-the-badge&color=yellow&logo=github)](https://github.com/AmirVoid12/SpotiFX/stargazers)

*Transform how you enjoy music with SpotiFX - Download your favorite tracks, albums, and playlists in premium quality*

[✨ Features](#-features) • [🚀 Installation](#-installation) • [🎮 Usage](#-usage) • [📊 Examples](#-examples) • [⚙️ Config](#%EF%B8%8F-configuration) • [❓ FAQ](#-faq)

</div>

---

## ✨ Features

<div align="center">

<table>
<tr>
<td align="center" width="33%">
<div style="text-align:center">
<svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="10" fill="#1DB954"/>
  <path d="M7,14 L7,10 C7,7.23858 9.23858,5 12,5 C14.7614,5 17,7.23858 17,10 L17,14" stroke="white" stroke-width="2" stroke-linecap="round"/>
  <path d="M5,14 L5,14 C5,14.5523 5.44772,15 6,15 L7,15 L7,19 L7,19" stroke="white" stroke-width="2" stroke-linecap="round"/>
  <path d="M19,14 L19,14 C19,14.5523 18.5523,15 18,15 L17,15 L17,19 L17,19" stroke="white" stroke-width="2" stroke-linecap="round"/>
  <circle cx="7" cy="17" r="2" fill="white"/>
  <circle cx="17" cy="17" r="2" fill="white"/>
</svg>
</div>
<h3>🎵 Full Music Library</h3>
Download tracks, albums and entire playlists from Spotify
</td>
<td align="center" width="33%">
<div style="text-align:center">
<svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="10" fill="#1DB954"/>
  <path d="M8,16 L8,8 L12,8 L16,12 L12,16 L8,16 Z" fill="white"/>
  <path d="M17,8 L17,16" stroke="white" stroke-width="2" stroke-linecap="round"/>
  <path d="M17,9 L19,7" stroke="white" stroke-width="2" stroke-linecap="round"/>
  <path d="M17,15 L19,17" stroke="white" stroke-width="2" stroke-linecap="round"/>
</svg>
</div>
<h3>🔊 Premium Quality</h3>
Get your music in high-definition 320kbps MP3 format
</td>
<td align="center" width="33%">
<div style="text-align:center">
<svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="10" fill="#1DB954"/>
  <path d="M6,12 L10,16 L18,8" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
</div>
<h3>📊 Visual Tracking</h3>
Real-time progress bars with estimated completion time
</td>
</tr>
<tr>
<td align="center" width="33%">
<div style="text-align:center">
<svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="10" fill="#1DB954"/>
  <rect x="7" y="7" width="10" height="10" rx="1" fill="white"/>
  <path d="M10,14 L14,14" stroke="#1DB954" stroke-width="1" stroke-linecap="round"/>
  <path d="M10,12 L14,12" stroke="#1DB954" stroke-width="1" stroke-linecap="round"/>
  <path d="M10,10 L12,10" stroke="#1DB954" stroke-width="1" stroke-linecap="round"/>
</svg>
</div>
<h3>🖼️ Rich Metadata</h3>
Complete with album artwork, artist info, and lyrics
</td>
<td align="center" width="33%">
<div style="text-align:center">
<svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="10" fill="#1DB954"/>
  <path d="M7,16 L7,8 M12,16 L12,12 M17,16 L17,10" stroke="white" stroke-width="2" stroke-linecap="round"/>
  <circle cx="7" cy="6" r="1" fill="white"/>
  <circle cx="12" cy="10" r="1" fill="white"/>
  <circle cx="17" cy="8" r="1" fill="white"/>
</svg>
</div>
<h3>⚡ Parallel Processing</h3>
Download multiple tracks simultaneously
</td>
<td align="center" width="33%">
<div style="text-align:center">
<svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="10" fill="#1DB954"/>
  <rect x="6" y="9" width="12" height="6" rx="1" fill="white"/>
  <path d="M9,12 L15,12" stroke="#1DB954" stroke-width="1" stroke-linecap="round"/>
  <path d="M7,15 L7,17 C7,17.5523 7.44772,18 8,18 L16,18 C16.5523,18 17,17.5523 17,17 L17,15" stroke="white" stroke-linecap="round"/>
  <path d="M7,9 L7,7 C7,6.44772 7.44772,6 8,6 L16,6 C16.5523,6 17,6.44772 17,7 L17,9" stroke="white" stroke-linecap="round"/>
</svg>
</div>
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

## 📊 Examples

<div align="center">

<!-- Main interface SVG illustration -->
<svg width="800" height="400" viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="400" rx="10" fill="#282c34"/>
  <rect x="20" y="20" width="760" height="50" rx="5" fill="#1DB954"/>
  <text x="400" y="50" font-family="Arial" font-size="24" fill="white" text-anchor="middle" dominant-baseline="middle">SpotiFX - Spotify Downloader</text>
  
  <!-- Menu section -->
  <rect x="20" y="90" width="200" height="290" rx="5" fill="#333842"/>
  <text x="120" y="120" font-family="Arial" font-size="18" fill="white" text-anchor="middle">Main Menu</text>
  <rect x="30" y="140" width="180" height="30" rx="5" fill="#1DB954"/>
  <text x="120" y="160" font-family="Arial" font-size="14" fill="white" text-anchor="middle">Download Track</text>
  <rect x="30" y="180" width="180" height="30" rx="5" fill="#444"/>
  <text x="120" y="200" font-family="Arial" font-size="14" fill="white" text-anchor="middle">Download Album</text>
  <rect x="30" y="220" width="180" height="30" rx="5" fill="#444"/>
  <text x="120" y="240" font-family="Arial" font-size="14" fill="white" text-anchor="middle">Download Playlist</text>
  <rect x="30" y="260" width="180" height="30" rx="5" fill="#444"/>
  <text x="120" y="280" font-family="Arial" font-size="14" fill="white" text-anchor="middle">View Queue</text>
  <rect x="30" y="300" width="180" height="30" rx="5" fill="#444"/>
  <text x="120" y="320" font-family="Arial" font-size="14" fill="white" text-anchor="middle">Settings</text>
  
  <!-- Content section -->
  <rect x="240" y="90" width="540" height="290" rx="5" fill="#333842"/>
  <text x="510" y="120" font-family="Arial" font-size="18" fill="white" text-anchor="middle">Track Information</text>
  
  <!-- Track info -->
  <rect x="260" y="140" width="500" height="80" rx="5" fill="#444"/>
  <text x="280" y="165" font-family="Arial" font-size="16" fill="#1DB954">Title:</text>
  <text x="350" y="165" font-family="Arial" font-size="16" fill="white">Blinding Lights</text>
  <text x="280" y="195" font-family="Arial" font-size="16" fill="#1DB954">Artist:</text>
  <text x="350" y="195" font-family="Arial" font-size="16" fill="white">The Weeknd</text>
  
  <!-- Progress bar -->
  <rect x="260" y="240" width="500" height="40" rx="5" fill="#444"/>
  <rect x="270" y="250" width="300" height="20" rx="5" fill="#1DB954"/>
  <text x="510" y="265" font-family="Arial" font-size="14" fill="white" text-anchor="middle">60% Complete - 01:20 remaining</text>
  
  <!-- Downloads list -->
  <rect x="260" y="300" width="500" height="60" rx="5" fill="#444"/>
  <text x="280" y="325" font-family="Arial" font-size="14" fill="white">Downloaded: 3 tracks</text>
  <text x="280" y="345" font-family="Arial" font-size="14" fill="white">Queue: 2 tracks remaining</text>
</svg>

<p><i>Interactive interface with color-coded menus and real-time progress tracking</i></p>

<!-- Two-panel view with SVG illustrations -->
<table>
<tr>
<td width="50%">
<svg width="400" height="250" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="250" rx="10" fill="#282c34"/>
  <rect x="20" y="20" width="360" height="40" rx="5" fill="#1DB954"/>
  <text x="200" y="45" font-family="Arial" font-size="18" fill="white" text-anchor="middle">Download Progress</text>
  
  <!-- Track 1 -->
  <rect x="20" y="80" width="360" height="40" rx="5" fill="#333842"/>
  <text x="30" y="105" font-family="Arial" font-size="14" fill="white">Blinding Lights - The Weeknd</text>
  <rect x="220" y="90" width="150" height="20" rx="5" fill="#444"/>
  <rect x="220" y="90" width="150" height="20" rx="5" fill="#444"/>
  <rect x="220" y="90" width="150" height="20" rx="5" fill="#1DB954" width="100%"/>
  <text x="295" y="105" font-family="Arial" font-size="12" fill="white" text-anchor="middle">Completed</text>
  
  <!-- Track 2 -->
  <rect x="20" y="130" width="360" height="40" rx="5" fill="#333842"/>
  <text x="30" y="155" font-family="Arial" font-size="14" fill="white">Starboy - The Weeknd</text>
  <rect x="220" y="140" width="150" height="20" rx="5" fill="#444"/>
  <rect x="220" y="140" width="90" height="20" rx="5" fill="#1DB954"/>
  <text x="295" y="155" font-family="Arial" font-size="12" fill="white" text-anchor="middle">60%</text>
  
  <!-- Track 3 -->
  <rect x="20" y="180" width="360" height="40" rx="5" fill="#333842"/>
  <text x="30" y="205" font-family="Arial" font-size="14" fill="white">Save Your Tears - The Weeknd</text>
  <rect x="220" y="190" width="150" height="20" rx="5" fill="#444"/>
  <rect x="220" y="190" width="30" height="20" rx="5" fill="#1DB954"/>
  <text x="295" y="205" font-family="Arial" font-size="12" fill="white" text-anchor="middle">20%</text>
</svg>
<p align="center"><i>Real-time download tracking</i></p>
</td>
<td width="50%">
<svg width="400" height="250" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="250" rx="10" fill="#282c34"/>
  <rect x="20" y="20" width="360" height="40" rx="5" fill="#1DB954"/>
  <text x="200" y="45" font-family="Arial" font-size="18" fill="white" text-anchor="middle">Music Library</text>
  
  <!-- Album folder -->
  <rect x="30" y="80" width="340" height="150" rx="5" fill="#333842"/>
  <rect x="40" y="90" width="320" height="30" rx="5" fill="#444"/>
  <text x="60" y="110" font-family="Arial" font-size="14" fill="#1DB954">📂 After Hours - The Weeknd</text>
  
  <!-- Album contents -->
  <rect x="60" y="130" width="300" height="20" rx="5" fill="#444"/>
  <text x="80" y="145" font-family="Arial" font-size="12" fill="white">01. Alone Again.mp3</text>
  
  <rect x="60" y="155" width="300" height="20" rx="5" fill="#444"/>
  <text x="80" y="170" font-family="Arial" font-size="12" fill="white">02. Too Late.mp3</text>
  
  <rect x="60" y="180" width="300" height="20" rx="5" fill="#444"/>
  <text x="80" y="195" font-family="Arial" font-size="12" fill="white">03. Hardest To Love.mp3</text>
  
  <rect x="60" y="205" width="300" height="20" rx="5" fill="#444"/>
  <text x="80" y="220" font-family="Arial" font-size="12" fill="white">04. Scared To Live.mp3</text>
</svg>
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

<div align="center">
<svg width="700" height="200" viewBox="0 0 700 200" xmlns="http://www.w3.org/2000/svg">
  <rect width="700" height="200" rx="10" fill="#282c34"/>
  
  <!-- Timeline line -->
  <line x1="50" y1="100" x2="650" y2="100" stroke="#666" stroke-width="4" stroke-linecap="round" stroke-dasharray="1,5"/>
  
  <!-- Completed milestones -->
  <circle cx="100" cy="100" r="20" fill="#1DB954"/>
  <text x="100" y="145" font-family="Arial" font-size="12" fill="white" text-anchor="middle">Core Engine</text>
  <text x="100" y="100" font-family="Arial" font-size="16" fill="white" text-anchor="middle">✓</text>
  
  <circle cx="200" cy="100" r="20" fill="#1DB954"/>
  <text x="200" y="145" font-family="Arial" font-size="12" fill="white" text-anchor="middle">Playlist Support</text>
  <text x="200" y="100" font-family="Arial" font-size="16" fill="white" text-anchor="middle">✓</text>
  
  <circle cx="300" cy="100" r="20" fill="#1DB954"/>
  <text x="300" y="145" font-family="Arial" font-size="12" fill="white" text-anchor="middle">Metadata</text>
  <text x="300" y="100" font-family="Arial" font-size="16" fill="white" text-anchor="middle">✓</text>
  
  <circle cx="400" cy="100" r="20" fill="#1DB954"/>
  <text x="400" y="145" font-family="Arial" font-size="12" fill="white" text-anchor="middle">Parallel DL</text>
  <text x="400" y="100" font-family="Arial" font-size="16" fill="white" text-anchor="middle">✓</text>
  
  <!-- Future milestones -->
  <circle cx="500" cy="100" r="20" fill="#666"/>
  <text x="500" y="145" font-family="Arial" font-size="12" fill="white" text-anchor="middle">Web Interface</text>
  
  <circle cx="600" cy="100" r="20" fill="#666"/>
  <text x="600" y="145" font-family="Arial" font-size="12" fill="white" text-anchor="middle">Mobile App</text>
  
  <!-- Version indicator -->
  <text x="350" y="50" font-family="Arial" font-size="18" fill="#1DB954" text-anchor="middle">Development Roadmap</text>
  <text x="350" y="70" font-family="Arial" font-size="14" fill="white" text-anchor="middle">Current Version: 1.0.0</text>
</svg>
</div>

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

```
MIT License

Copyright (c) 2025 Amir.Void

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙌 Acknowledgements

- [Spotipy](https://spotipy.readthedocs.io/) - Spotify Web API client library
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube download library
- [Mutagen](https://mutagen.readthedocs.io/) - Audio metadata handling
- [Colorama](https://pypi.org/project/colorama/) - Terminal text styling

## 👨‍💻 Author

**Amir.Void** - [GitHub](https://github.com/AmirVoid12)

---

<div align="center">

<!-- Footer SVG -->
<svg width="700" height="100" viewBox="0 0 700 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="footerGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1DB954" />
      <stop offset="100%" stop-color="#0D8F3C" />
    </linearGradient>
  </defs>
  <rect width="700" height="100" rx="10" fill="url(#footerGradient)"/>
  <text x="350" y="40" font-family="Arial" font-size="24" fill="white" text-anchor="middle" font-weight="bold">SpotiFX</text>
  <text x="350" y="70" font-family="Arial" font-size="16" fill="white" text-anchor="middle">If you enjoy SpotiFX, please consider giving it a ⭐ star on GitHub!</text>
</svg>

</div>