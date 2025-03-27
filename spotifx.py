# -- STARTED WRITING CODE -- 

"""
SpotiFX - Spotify Music Downloader and Manager
Created by Amir.Void (GitHub: AmirVoid12)
Version 3.2.1 - 2025
"""

import os
import re
import sys
import time
import json
import uuid
import mutagen
import platform
import hashlib
import logging
import threading
import subprocess
import webbrowser
import configparser
import colorama
from queue import Queue, Empty
from datetime import datetime

try:
    import requests
    import requests.exceptions
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
    import requests.exceptions

try:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import spotipy.exceptions
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "spotipy"])
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import spotipy.exceptions

try:
    import yt_dlp
    import yt_dlp.utils
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp
    import yt_dlp.utils

try:
    from colorama import init, Fore, Back, Style
    init()
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore, Style
    init()

try:
    from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC, TRCK, TCON, USLT
    from mutagen.mp3 import MP3
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mutagen"])
    from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC, TRCK, TCON, USLT
    from mutagen.mp3 import MP3

VERSION = "1.0.0"
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".spotifx")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, "credentials.json")
DATABASE_FILE = os.path.join(CONFIG_DIR, "database.json")
CACHE_DIR = os.path.join(CONFIG_DIR, "cache")
DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "SpotiFX_Downloads")
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30

LOGO_ASCII = """
▒█▀▀▀█ █▀▀█ █▀▀█ ▀▀█▀▀ ░▀░ █▀▀ ▀▄▒▄▀
░▀▀▀▄▄ █░░█ █░░█ ░░█░░ ▀█▀ █▀▀ ░▒█░░
▒█▄▄▄█ █▀▀▀ ▀▀▀▀ ░░▀░░ ▀▀▀ ▀░░ ▄▀▒▀▄
"""

class Logger:
    def __init__(self):
        self.logger = logging.getLogger("SpotiFX")
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            f"{Fore.CYAN}%(asctime)s{Style.RESET_ALL} - %(levelname)s - %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        os.makedirs(CONFIG_DIR, exist_ok=True)
        try:
            file_handler = logging.FileHandler(os.path.join(CONFIG_DIR, "spotifx.log"))
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(file_handler)
        except Exception:
            pass
            
    def info(self, message):
        self.logger.info(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
        
    def warning(self, message):
        self.logger.warning(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
        
    def error(self, message):
        self.logger.error(f"{Fore.RED}{message}{Style.RESET_ALL}")
        
    def debug(self, message):
        self.logger.debug(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

logger = Logger()

def create_directories():
    directories = [CONFIG_DIR, CACHE_DIR, DEFAULT_DOWNLOAD_DIR]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def sanitize_filename(filename):
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    if not sanitized:
        sanitized = "unnamed_file"
    return sanitized[:200]  

def generate_unique_id():
    return str(uuid.uuid4())

class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_file = CONFIG_FILE
        self.load_config()
        
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                self.config.read(self.config_file, encoding='utf-8')
            except Exception as e:
                logger.error(f"Failed to load configuration: {e}")
                self._create_default_config()
        else:
            self._create_default_config()
            
    def _create_default_config(self):
        logger.info("Creating default configuration")
        
        self.config['General'] = {
            'download_dir': DEFAULT_DOWNLOAD_DIR,
            'concurrent_downloads': '3',
            'auto_update_check': 'true',
            'language': 'en',
            'save_log': 'true'
        }
        
        self.config['Audio'] = {
            'audio_quality': '320',
            'audio_format': 'mp3',
            'normalize_audio': 'true',
            'embed_cover_art': 'true',
            'embed_lyrics': 'true'
        }
        
        self.config['Spotify'] = {
            'region': 'US',
            'create_playlist_folders': 'true',
            'download_liked_songs': 'false',
            'include_podcasts': 'false'
        }
        
        self.config['YouTube'] = {
            'max_search_results': '5',
            'prefer_official_audio': 'true',
            'force_ipv4': 'true',
            'use_proxy': 'false',
            'proxy': ''
        }
        
        self.save_config()
            
    def save_config(self):
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            
    def get(self, section, option, fallback=None):
        try:
            return self.config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
            
    def getint(self, section, option, fallback=0):
        try:
            return self.config.getint(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
            
    def getfloat(self, section, option, fallback=0.0):
        try:
            return self.config.getfloat(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
            
    def getboolean(self, section, option, fallback=False):
        try:
            return self.config.getboolean(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
            
    def set(self, section, option, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
            
        self.config.set(section, option, str(value))
        self.save_config()

class CredentialsManager:
    def __init__(self):
        self.credentials_file = CREDENTIALS_FILE
        self.credentials = self._load_credentials()
        
    def _load_credentials(self):
        if os.path.exists(self.credentials_file):
            try:
                with open(self.credentials_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load credentials: {e}")
        
        return {
            'spotify': {
                'client_id': '',
                'client_secret': ''
            }
        }
        
    def save_credentials(self):
        try:
            os.makedirs(os.path.dirname(self.credentials_file), exist_ok=True)
            with open(self.credentials_file, 'w', encoding='utf-8') as f:
                json.dump(self.credentials, f, indent=2)
            
            if os.name != 'nt':  # Not Windows
                os.chmod(self.credentials_file, 0o600)
        except Exception as e:
            logger.error(f"Failed to save credentials: {e}")
            
    def get_spotify_credentials(self):
        if 'spotify' not in self.credentials:
            self.credentials['spotify'] = {'client_id': '', 'client_secret': ''}
            
        return (
            self.credentials['spotify'].get('client_id', ''),
            self.credentials['spotify'].get('client_secret', '')
        )
        
    def set_spotify_credentials(self, client_id, client_secret):
        if 'spotify' not in self.credentials:
            self.credentials['spotify'] = {}
            
        self.credentials['spotify']['client_id'] = client_id
        self.credentials['spotify']['client_secret'] = client_secret
        self.save_credentials()
        
    def has_spotify_credentials(self):
        client_id, client_secret = self.get_spotify_credentials()
        return bool(client_id and client_secret)

class DatabaseManager:
    def __init__(self):
        self.db_file = DATABASE_FILE
        self.db = self._load_database()
        
    def _load_database(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load database: {e}")
        
        return {
            'downloads': [],
            'favorites': [],
            'playlists': [],
            'queue': [],
            'stats': {
                'total_tracks': 0,
                'total_playlists': 0,
                'total_bytes_downloaded': 0,
                'first_download_date': None,
                'last_download_date': None
            }
        }
        
    def save_database(self):
        try:
            os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.db, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save database: {e}")
            
    def add_download_record(self, record):
        if 'downloads' not in self.db:
            self.db['downloads'] = []
            
        if 'id' not in record:
            record['id'] = generate_unique_id()
            
        if 'timestamp' not in record:
            record['timestamp'] = datetime.now().isoformat()
            
        self.db['downloads'].append(record)
        
        self._update_stats(record)
        
        self.save_database()
        
    def _update_stats(self, record):
        if 'stats' not in self.db:
            self.db['stats'] = {
                'total_tracks': 0,
                'total_playlists': 0,
                'total_bytes_downloaded': 0,
                'first_download_date': None,
                'last_download_date': None
            }
            
        stats = self.db['stats']
        
        if record.get('type') == 'track':
            stats['total_tracks'] += 1
            
        elif record.get('type') == 'playlist':
            stats['total_playlists'] += 1
            tracks_count = len(record.get('tracks', []))
            stats['total_tracks'] += tracks_count
            
        if 'file_size' in record:
            stats['total_bytes_downloaded'] += record['file_size']
            
        now = datetime.now().isoformat()
        if not stats['first_download_date']:
            stats['first_download_date'] = now
        stats['last_download_date'] = now
        
    def get_download_history(self, limit=0, offset=0):
        if 'downloads' not in self.db:
            return []
            
        sorted_downloads = sorted(
            self.db['downloads'], 
            key=lambda x: x.get('timestamp', ''), 
            reverse=True
        )
        
        if limit > 0:
            return sorted_downloads[offset:offset+limit]
        else:
            return sorted_downloads[offset:]
            
    def add_to_favorites(self, item):
        if 'favorites' not in self.db:
            self.db['favorites'] = []
            
        for fav in self.db['favorites']:
            if fav.get('spotify_id') == item.get('spotify_id'):
                return
                
        if 'id' not in item:
            item['id'] = generate_unique_id()
            
        if 'added_at' not in item:
            item['added_at'] = datetime.now().isoformat()
            
        self.db['favorites'].append(item)
        self.save_database()
        
    def remove_from_favorites(self, item_id):
        if 'favorites' not in self.db:
            return False
            
        original_count = len(self.db['favorites'])
        
        self.db['favorites'] = [
            fav for fav in self.db['favorites'] 
            if fav.get('id') != item_id and fav.get('spotify_id') != item_id
        ]
        
        if len(self.db['favorites']) < original_count:
            self.save_database()
            return True
        
        return False
        
    def get_favorites(self):
        if 'favorites' not in self.db:
            return []
            
        return sorted(
            self.db['favorites'], 
            key=lambda x: x.get('added_at', ''), 
            reverse=True
        )
        
    def add_to_queue(self, item):
        if 'queue' not in self.db:
            self.db['queue'] = []
            
        if 'id' not in item:
            item['id'] = generate_unique_id()
            
        if 'added_at' not in item:
            item['added_at'] = datetime.now().isoformat()
            
        if 'status' not in item:
            item['status'] = 'pending'
            
        self.db['queue'].append(item)
        self.save_database()
        
        return item['id']
        
    def update_queue_item(self, item_id, updates):
        if 'queue' not in self.db:
            return False
            
        for i, item in enumerate(self.db['queue']):
            if item.get('id') == item_id:
                self.db['queue'][i].update(updates)
                self.save_database()
                return True
                
        return False
        
    def remove_from_queue(self, item_id):
        if 'queue' not in self.db:
            return False
            
        original_count = len(self.db['queue'])
        
        self.db['queue'] = [
            item for item in self.db['queue'] 
            if item.get('id') != item_id
        ]
        
        if len(self.db['queue']) < original_count:
            self.save_database()
            return True
        
        return False
        
    def get_queue(self, status=None):
        if 'queue' not in self.db:
            return []
            
        if status:
            return [item for item in self.db['queue'] if item.get('status') == status]
        else:
            return self.db['queue']
            
    def get_stats(self):
        if 'stats' not in self.db:
            self.db['stats'] = {
                'total_tracks': 0,
                'total_playlists': 0,
                'total_bytes_downloaded': 0,
                'first_download_date': None,
                'last_download_date': None
            }
            
        return self.db['stats']

class CacheManager:
    def __init__(self, cache_dir=CACHE_DIR):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        
        self.memory_cache = {}
        
    def _get_cache_key(self, key):
        hash_obj = hashlib.md5(key.encode('utf-8'))
        return hash_obj.hexdigest()
        
    def _get_cache_path(self, key):
        cache_key = self._get_cache_key(key)
        return os.path.join(self.cache_dir, f"{cache_key}.json")
        
    def get(self, key, max_age=None):
        cache_key = self._get_cache_key(key)
        
        if cache_key in self.memory_cache:
            cache_entry = self.memory_cache[cache_key]
            
            if max_age:
                cache_time = cache_entry.get('timestamp', 0)
                current_time = time.time()
                if current_time - cache_time > max_age:
                    return None
            
            return cache_entry.get('data')
            
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
            
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_entry = json.load(f)
                
            if max_age:
                cache_time = cache_entry.get('timestamp', 0)
                current_time = time.time()
                if current_time - cache_time > max_age:
                    return None
                    
            self.memory_cache[cache_key] = cache_entry
            
            return cache_entry.get('data')
        except Exception as e:
            logger.debug(f"Cache read error for {key}: {e}")
            return None
            
    def set(self, key, data):
        cache_key = self._get_cache_key(key)
        cache_path = self._get_cache_path(key)
        
        cache_entry = {
            'timestamp': time.time(),
            'data': data
        }
        
        self.memory_cache[cache_key] = cache_entry
        
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_entry, f, ensure_ascii=False)
        except Exception as e:
            logger.debug(f"Cache write error for {key}: {e}")
            
    def remove(self, key):
        cache_key = self._get_cache_key(key)
        
        if cache_key in self.memory_cache:
            del self.memory_cache[cache_key]
            
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            try:
                os.remove(cache_path)
            except Exception as e:
                logger.debug(f"Cache delete error for {key}: {e}")
                
    def clear(self, max_age=None):
        cleared_count = 0
        
        if max_age is None:
            cleared_count = len(self.memory_cache)
            self.memory_cache = {}
            
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    try:
                        os.remove(os.path.join(self.cache_dir, filename))
                    except:
                        pass
        else:
            current_time = time.time()
            
            expired_keys = []
            for cache_key, cache_entry in self.memory_cache.items():
                cache_time = cache_entry.get('timestamp', 0)
                if current_time - cache_time > max_age:
                    expired_keys.append(cache_key)
                    cleared_count += 1
                    
            for key in expired_keys:
                del self.memory_cache[key]
                
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    try:
                        filepath = os.path.join(self.cache_dir, filename)
                        file_mtime = os.path.getmtime(filepath)
                        
                        if current_time - file_mtime > max_age:
                            os.remove(filepath)
                            cleared_count += 1
                    except:
                        pass
                        
        return cleared_count

class SpotifyClient:
    def __init__(self, client_id, client_secret, cache_manager=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.cache = cache_manager or CacheManager()
        
        try:
            self.sp = spotipy.Spotify(
                client_credentials_manager=SpotifyClientCredentials(
                    client_id=client_id,
                    client_secret=client_secret
                )
            )
            self.connected = True
            logger.info("Spotify client initialized successfully")
        except Exception as e:
            self.connected = False
            logger.error(f"Failed to initialize Spotify client: {e}")
            raise
            
    def test_connection(self):
        try:
            self.sp.new_releases(limit=1)
            return True
        except Exception as e:
            logger.error(f"Spotify API connection test failed: {e}")
            return False
            
    def get_track(self, track_id):
        cache_key = f"spotify:track:{track_id}"
        
        cached_data = self.cache.get(cache_key, 86400)
        if cached_data:
            return cached_data
            
        try:
            if track_id.startswith('http'):
                track_id = self._extract_id_from_url(track_id, 'track')
                
            track = self.sp.track(track_id)
            
            self.cache.set(cache_key, track)
            
            return track
        except Exception as e:
            logger.error(f"Failed to get track {track_id}: {e}")
            return None
            
    def get_album(self, album_id):
        cache_key = f"spotify:album:{album_id}"
        
        cached_data = self.cache.get(cache_key, 86400)
        if cached_data:
            return cached_data
            
        try:
            if album_id.startswith('http'):
                album_id = self._extract_id_from_url(album_id, 'album')
                
            album = self.sp.album(album_id)
            
            if 'tracks' in album and 'items' in album['tracks']:
                results = album['tracks']
                tracks = results['items']
                
                while results['next']:
                    results = self.sp.next(results)
                    tracks.extend(results['items'])
                    
                album['tracks']['items'] = tracks
                
            self.cache.set(cache_key, album)
            
            return album
        except Exception as e:
            logger.error(f"Failed to get album {album_id}: {e}")
            return None
            
    def get_playlist(self, playlist_id):
        cache_key = f"spotify:playlist:{playlist_id}"
        
        cached_data = self.cache.get(cache_key, 3600)
        if cached_data:
            return cached_data
            
        try:
            if playlist_id.startswith('http'):
                playlist_id = self._extract_id_from_url(playlist_id, 'playlist')
                
            playlist = self.sp.playlist(playlist_id)
            
            if 'tracks' in playlist and 'items' in playlist['tracks']:
                results = playlist['tracks']
                tracks = results['items']
                
                while results['next']:
                    results = self.sp.next(results)
                    tracks.extend(results['items'])
                    
                playlist['tracks']['items'] = tracks
                
            self.cache.set(cache_key, playlist)
            
            return playlist
        except Exception as e:
            logger.error(f"Failed to get playlist {playlist_id}: {e}")
            return None
            
    def search(self, query, search_type='track', limit=10):
        cache_key = f"spotify:search:{search_type}:{query}:{limit}"
        
        cached_data = self.cache.get(cache_key, 3600)
        if cached_data:
            return cached_data
            
        try:
            results = self.sp.search(q=query, type=search_type, limit=limit)
            
            self.cache.set(cache_key, results)
            
            return results
        except Exception as e:
            logger.error(f"Failed to search for {query}: {e}")
            return None
            
    def _extract_id_from_url(self, url, resource_type):
        pattern = f"/{resource_type}/([a-zA-Z0-9]+)"
        match = re.search(pattern, url)
        
        if match:
            return match.group(1)
        
        return url

class YouTubeDownloader:
    def __init__(self, config_manager=None):
        self.config = config_manager or ConfigManager()
        self.download_dir = self.config.get('General', 'download_dir', DEFAULT_DOWNLOAD_DIR)
        self.progress_hooks = []
        self.current_download = None
        
        os.makedirs(self.download_dir, exist_ok=True)
        
    def add_progress_hook(self, hook):
        self.progress_hooks.append(hook)
        
    def _progress_hook(self, info):
        self.current_download = info
        
        for hook in self.progress_hooks:
            hook(info)
            
    def search_youtube(self, query, limit=5):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                'extract_flat': True,
                'skip_download': True,
                'format': 'bestaudio/best',
                'default_search': 'ytsearch'
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                results = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
                
                if not results or 'entries' not in results:
                    return []
                    
                entries = list(results['entries'])
                entries = [e for e in entries if e and e.get('id')]
                
                return entries
        except Exception as e:
            logger.error(f"YouTube search failed for {query}: {e}")
            return []
            
    def find_best_match(self, track_info):
        if not track_info or 'name' not in track_info or 'artists' not in track_info:
            logger.error("Invalid track info provided")
            return None
            
        try:
            artist_name = track_info['artists'][0]['name']
            track_name = track_info['name']
            album_name = track_info.get('album', {}).get('name', '')
            
            queries = [
                f"{artist_name} - {track_name} audio",
                f"{artist_name} {track_name} audio",
                f"{artist_name} {track_name} {album_name} audio",
                f"{artist_name} {track_name} official audio",
                f"{track_name} {artist_name} topic",
            ]
            
            for query in queries:
                results = self.search_youtube(query)
                
                if results:
                    track_duration_ms = track_info.get('duration_ms', 0)
                    track_duration_sec = track_duration_ms / 1000 if track_duration_ms else 0
                    
                    filtered_results = []
                    for result in results:
                        if 'official audio' in query.lower() and 'official video' in result.get('title', '').lower():
                            continue
                            
                        video_duration = result.get('duration', 0)
                        
                        if track_duration_sec > 0 and video_duration > 0:
                            duration_diff = abs(video_duration - track_duration_sec)
                            if duration_diff <= 15 or duration_diff / track_duration_sec <= 0.2:
                                filtered_results.append(result)
                    
                    if filtered_results:
                        filtered_results.sort(
                            key=lambda x: x.get('view_count', 0) if x.get('view_count') else 0,
                            reverse=True
                        )
                        return filtered_results[0]
                    
                    return results[0]
                    
            results = self.search_youtube(f"{artist_name} {track_name}")
            return results[0] if results else None
        
        except Exception as e:
            logger.error(f"Failed to find YouTube match: {e}")
            return None
            
    def download_audio(self, video_url, output_path=None, metadata=None):
        try:
            audio_quality = self.config.get('Audio', 'audio_quality', '320')
            audio_format = self.config.get('Audio', 'audio_format', 'mp3')
            
            if output_path:
                output_template = output_path
            else:
                output_template = os.path.join(self.download_dir, '%(title)s.%(ext)s')
                
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': audio_format,
                    'preferredquality': audio_quality,
                }],
                'outtmpl': output_template,
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self._progress_hook],
                'force_ipv4': self.config.getboolean('YouTube', 'force_ipv4', True)
            }
            
            if self.config.getboolean('YouTube', 'use_proxy', False):
                proxy = self.config.get('YouTube', 'proxy', '')
                if proxy:
                    ydl_opts['proxy'] = proxy
                    
            # Handle metadata properly - avoid passing it directly to FFmpegMetadataPP
            # Instead, apply it after download using mutagen
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                
                if not info:
                    return None
                    
                if 'requested_downloads' in info:
                    filename = info['requested_downloads'][0]['filepath']
                else:
                    filename = ydl.prepare_filename(info)
                    basename, _ = os.path.splitext(filename)
                    filename = f"{basename}.{audio_format}"
                
                if metadata and os.path.exists(filename):
                    self._apply_metadata(filename, metadata)
                    
                return filename
        except Exception as e:
            logger.error(f"YouTube download failed: {e}")
            return None
            
    def _apply_metadata(self, file_path, metadata):
        try:
            if not os.path.exists(file_path):
                return
                
            if file_path.lower().endswith('.mp3'):
                audio = MP3(file_path)
                
                if not audio.tags:
                    audio.tags = ID3()
                
                if 'title' in metadata:
                    audio.tags.add(TIT2(encoding=3, text=metadata['title']))
                
                if 'artist' in metadata:
                    audio.tags.add(TPE1(encoding=3, text=metadata['artist']))
                
                if 'album' in metadata:
                    audio.tags.add(TALB(encoding=3, text=metadata['album']))
                
                if 'date' in metadata:
                    audio.tags.add(TDRC(encoding=3, text=metadata['date']))
                
                if 'track_number' in metadata:
                    audio.tags.add(TRCK(encoding=3, text=str(metadata['track_number'])))
                
                if 'genre' in metadata:
                    audio.tags.add(TCON(encoding=3, text=metadata['genre']))
                
                if 'cover_url' in metadata and metadata['cover_url']:
                    try:
                        response = requests.get(metadata['cover_url'])
                        if response.status_code == 200:
                            audio.tags.add(APIC(
                                encoding=3,
                                mime='image/jpeg',
                                type=3,  # Cover image
                                desc='Cover',
                                data=response.content
                            ))
                    except Exception as e:
                        logger.debug(f"Failed to add cover art: {e}")
                
                if 'lyrics' in metadata and metadata['lyrics']:
                    audio.tags.add(USLT(
                        encoding=3,
                        lang='eng',
                        desc='',
                        text=metadata['lyrics']
                    ))
                
                audio.save()
                
        except Exception as e:
            logger.error(f"Failed to apply metadata to {file_path}: {e}")

class DownloadManager:
    def __init__(self, spotify_client, youtube_downloader, database, config):
        self.spotify = spotify_client
        self.youtube = youtube_downloader
        self.db = database
        self.config = config
        
        self.max_concurrent = self.config.getint('General', 'concurrent_downloads', 3)
        self.download_dir = self.config.get('General', 'download_dir', DEFAULT_DOWNLOAD_DIR)
        
        self.download_queue = Queue()
        self.active_downloads = []
        self.download_threads = []
        self.shutdown_flag = threading.Event()
        
        for i in range(self.max_concurrent):
            t = threading.Thread(target=self._download_worker, daemon=True)
            self.download_threads.append(t)
            t.start()
            
        os.makedirs(self.download_dir, exist_ok=True)
        
    def _download_worker(self):
        while not self.shutdown_flag.is_set():
            try:
                task = self.download_queue.get(timeout=1)
                if task is None:
                    self.download_queue.task_done()
                    continue
                    
                item_id, task_type, task_data = task
                
                self.db.update_queue_item(item_id, {'status': 'downloading'})
                
                try:
                    if task_type == 'track':
                        self._download_track(item_id, task_data)
                    elif task_type == 'album':
                        self._download_album(item_id, task_data)
                    elif task_type == 'playlist':
                        self._download_playlist(item_id, task_data)
                    else:
                        logger.error(f"Unknown task type: {task_type}")
                        self.db.update_queue_item(item_id, {'status': 'failed', 'error': 'Unknown task type'})
                        
                except Exception as e:
                    logger.error(f"Download failed for {task_type} {item_id}: {e}")
                    self.db.update_queue_item(item_id, {
                        'status': 'failed',
                        'error': str(e),
                        'completed_at': datetime.now().isoformat()
                    })
                
                self.download_queue.task_done()
                
            except Empty:
                continue
            except Exception as e:
                logger.error(f"Download worker error: {e}")
                time.sleep(1)
                
    def _download_track(self, item_id, track_data):
        try:
            track_id = track_data.get('spotify_id')
            if not track_id:
                raise ValueError("No Spotify track ID provided")
                
            track_info = self.spotify.get_track(track_id)
            if not track_info:
                raise ValueError(f"Could not get track info for {track_id}")
                
            self.db.update_queue_item(item_id, {
                'track_name': track_info['name'],
                'artist_name': track_info['artists'][0]['name'],
                'album_name': track_info['album']['name'],
                'progress': 10
            })
            
            best_match = self.youtube.find_best_match(track_info)
            if not best_match:
                raise ValueError(f"Could not find YouTube match for {track_info['name']}")
                
            self.db.update_queue_item(item_id, {
                'youtube_id': best_match['id'],
                'youtube_title': best_match['title'],
                'progress': 20
            })
            
            album_art_url = None
            if track_info.get('album', {}).get('images'):
                album_art_url = track_info['album']['images'][0]['url']
                
            artist_name = sanitize_filename(track_info['artists'][0]['name'])
            album_name = sanitize_filename(track_info['album']['name'])
            track_name = sanitize_filename(track_info['name'])
            
            artist_dir = os.path.join(self.download_dir, artist_name)
            album_dir = os.path.join(artist_dir, album_name)
            os.makedirs(album_dir, exist_ok=True)
            
            track_number = str(track_info.get('track_number', 0)).zfill(2)
            filename = f"{track_number}. {track_name}.mp3"
            output_path = os.path.join(album_dir, filename)
            
            if os.path.exists(output_path):
                self.db.update_queue_item(item_id, {
                    'status': 'completed',
                    'progress': 100,
                    'file_path': output_path,
                    'completed_at': datetime.now().isoformat(),
                    'note': 'File already exists'
                })
                
                self.db.add_download_record({
                    'type': 'track',
                    'spotify_id': track_id,
                    'youtube_id': best_match['id'],
                    'track_name': track_info['name'],
                    'artist_name': track_info['artists'][0]['name'],
                    'album_name': track_info['album']['name'],
                    'file_path': output_path,
                    'file_size': os.path.getsize(output_path),
                    'source': 'spotify',
                    'status': 'existing'
                })
                
                return
                
            release_date = track_info.get('album', {}).get('release_date', '')
            track_number = track_info.get('track_number', 0)
            disc_number = track_info.get('disc_number', 1)
            
            metadata = {
                'title': track_info['name'],
                'artist': track_info['artists'][0]['name'],
                'album': track_info['album']['name'],
                'date': release_date,
                'track_number': f"{track_number}/{track_info['album']['total_tracks']}",
                'disc_number': disc_number,
                'cover_url': album_art_url
            }
            
            def progress_hook(info):
                if info['status'] == 'downloading':
                    downloaded = info.get('downloaded_bytes', 0)
                    total = info.get('total_bytes') or info.get('total_bytes_estimate', 0)
                    
                    if total > 0:
                        progress = int(30 + (downloaded / total) * 50)
                        self.db.update_queue_item(item_id, {'progress': progress})
                        
                elif info['status'] == 'finished':
                    self.db.update_queue_item(item_id, {'progress': 80})
                    
            self.youtube.add_progress_hook(progress_hook)
            
            downloaded_file = self.youtube.download_audio(
                best_match['id'], 
                output_path, 
                metadata
            )
            
            self.youtube.progress_hooks.remove(progress_hook)
            
            if not downloaded_file or not os.path.exists(downloaded_file):
                raise ValueError(f"Download failed for {track_info['name']}")
                
            file_size = os.path.getsize(downloaded_file)
            
            self.db.update_queue_item(item_id, {
                'status': 'completed',
                'progress': 100,
                'file_path': downloaded_file,
                'file_size': file_size,
                'completed_at': datetime.now().isoformat()
            })
            
            self.db.add_download_record({
                'type': 'track',
                'spotify_id': track_id,
                'youtube_id': best_match['id'],
                'track_name': track_info['name'],
                'artist_name': track_info['artists'][0]['name'],
                'album_name': track_info['album']['name'],
                'file_path': downloaded_file,
                'file_size': file_size,
                'source': 'spotify'
            })
            
            logger.info(f"Track downloaded: {track_info['name']}")
            
        except Exception as e:
            logger.error(f"Track download failed: {e}")
            self.db.update_queue_item(item_id, {
                'status': 'failed',
                'error': str(e),
                'completed_at': datetime.now().isoformat()
            })
            raise
            
    def _download_album(self, item_id, album_data):
        try:
            album_id = album_data.get('spotify_id')
            if not album_id:
                raise ValueError("No Spotify album ID provided")
                
            album_info = self.spotify.get_album(album_id)
            if not album_info:
                raise ValueError(f"Could not get album info for {album_id}")
                
            self.db.update_queue_item(item_id, {
                'album_name': album_info['name'],
                'artist_name': album_info['artists'][0]['name'],
                'track_count': len(album_info['tracks']['items']),
                'progress': 5
            })
            
            tracks = album_info['tracks']['items']
            total_tracks = len(tracks)
            completed_tracks = 0
            failed_tracks = 0
            track_results = []
            
            artist_name = sanitize_filename(album_info['artists'][0]['name'])
            album_name = sanitize_filename(album_info['name'])
            artist_dir = os.path.join(self.download_dir, artist_name)
            album_dir = os.path.join(artist_dir, album_name)
            os.makedirs(album_dir, exist_ok=True)
            
            for i, track in enumerate(tracks):
                track_progress = 5 + int((i / total_tracks) * 90)
                self.db.update_queue_item(item_id, {
                    'progress': track_progress,
                    'note': f"Downloading track {i+1}/{total_tracks}: {track['name']}"
                })
                
                try:
                    track_info = self.spotify.get_track(track['id'])
                    if not track_info:
                        logger.warning(f"Could not get details for track {track['id']}")
                        continue
                        
                    best_match = self.youtube.find_best_match(track_info)
                    if not best_match:
                        logger.warning(f"Could not find YouTube match for {track_info['name']}")
                        failed_tracks += 1
                        continue
                        
                    track_number = str(track_info.get('track_number', i+1)).zfill(2)
                    track_name = sanitize_filename(track_info['name'])
                    filename = f"{track_number}. {track_name}.mp3"
                    output_path = os.path.join(album_dir, filename)
                    
                    if os.path.exists(output_path):
                        completed_tracks += 1
                        track_results.append({
                            'spotify_id': track['id'],
                            'track_name': track['name'],
                            'file_path': output_path,
                            'status': 'existing'
                        })
                        continue
                        
                    album_art_url = None
                    if album_info.get('images'):
                        album_art_url = album_info['images'][0]['url']
                        
                    release_date = album_info.get('release_date', '')
                    metadata = {
                        'title': track_info['name'],
                        'artist': track_info['artists'][0]['name'],
                        'album': album_info['name'],
                        'date': release_date,
                        'track_number': f"{track_info['track_number']}/{album_info['total_tracks']}",
                        'disc_number': track_info.get('disc_number', 1),
                        'cover_url': album_art_url
                    }
                    
                    downloaded_file = self.youtube.download_audio(
                        best_match['id'], 
                        output_path, 
                        metadata
                    )
                    
                    if not downloaded_file or not os.path.exists(downloaded_file):
                        logger.warning(f"Download failed for {track_info['name']}")
                        failed_tracks += 1
                        continue
                        
                    completed_tracks += 1
                    track_results.append({
                        'spotify_id': track['id'],
                        'youtube_id': best_match['id'],
                        'track_name': track['name'],
                        'file_path': downloaded_file,
                        'file_size': os.path.getsize(downloaded_file),
                        'status': 'downloaded'
                    })
                    
                except Exception as e:
                    logger.error(f"Failed to download track {track['name']}: {e}")
                    failed_tracks += 1
                    
            self.db.update_queue_item(item_id, {
                'status': 'completed',
                'progress': 100,
                'completed_tracks': completed_tracks,
                'failed_tracks': failed_tracks,
                'dir_path': album_dir,
                'completed_at': datetime.now().isoformat(),
                'tracks': track_results
            })
            
            self.db.add_download_record({
                'type': 'album',
                'spotify_id': album_id,
                'album_name': album_info['name'],
                'artist_name': album_info['artists'][0]['name'],
                'track_count': total_tracks,
                'completed_tracks': completed_tracks,
                'failed_tracks': failed_tracks,
                'dir_path': album_dir,
                'tracks': track_results,
                'source': 'spotify'
            })
            
            logger.info(f"Album downloaded: {album_info['name']} - {completed_tracks}/{total_tracks} tracks")
            
        except Exception as e:
            logger.error(f"Album download failed: {e}")
            self.db.update_queue_item(item_id, {
                'status': 'failed',
                'error': str(e),
                'completed_at': datetime.now().isoformat()
            })
            raise
            
    def _download_playlist(self, item_id, playlist_data):
        try:
            playlist_id = playlist_data.get('spotify_id')
            if not playlist_id:
                raise ValueError("No Spotify playlist ID provided")
                
            playlist_info = self.spotify.get_playlist(playlist_id)
            if not playlist_info:
                raise ValueError(f"Could not get playlist info for {playlist_id}")
                
            self.db.update_queue_item(item_id, {
                'playlist_name': playlist_info['name'],
                'owner_name': playlist_info['owner']['display_name'],
                'track_count': len(playlist_info['tracks']['items']),
                'progress': 5
            })
            
            tracks = [item['track'] for item in playlist_info['tracks']['items'] if item['track']]
            total_tracks = len(tracks)
            completed_tracks = 0
            failed_tracks = 0
            track_results = []
            
            playlist_dir = self.download_dir
            if self.config.getboolean('Spotify', 'create_playlist_folders', True):
                playlist_name = sanitize_filename(playlist_info['name'])
                playlist_dir = os.path.join(self.download_dir, 'Playlists', playlist_name)
                os.makedirs(playlist_dir, exist_ok=True)
                
            for i, track in enumerate(tracks):
                track_progress = 5 + int((i / total_tracks) * 90)
                self.db.update_queue_item(item_id, {
                    'progress': track_progress,
                    'note': f"Downloading track {i+1}/{total_tracks}: {track['name']}"
                })
                
                try:
                    best_match = self.youtube.find_best_match(track)
                    if not best_match:
                        logger.warning(f"Could not find YouTube match for {track['name']}")
                        failed_tracks += 1
                        continue
                        
                    artist_name = sanitize_filename(track['artists'][0]['name'])
                    track_name = sanitize_filename(track['name'])
                    filename = f"{artist_name} - {track_name}.mp3"
                    output_path = os.path.join(playlist_dir, filename)
                    
                    if os.path.exists(output_path):
                        completed_tracks += 1
                        track_results.append({
                            'spotify_id': track['id'],
                            'track_name': track['name'],
                            'artist_name': track['artists'][0]['name'],
                            'file_path': output_path,
                            'status': 'existing'
                        })
                        continue
                        
                    album_art_url = None
                    if track.get('album', {}).get('images'):
                        album_art_url = track['album']['images'][0]['url']
                        
                    release_date = track.get('album', {}).get('release_date', '')
                    metadata = {
                        'title': track['name'],
                        'artist': track['artists'][0]['name'],
                        'album': track.get('album', {}).get('name', ''),
                        'date': release_date,
                        'cover_url': album_art_url
                    }
                    
                    downloaded_file = self.youtube.download_audio(
                        best_match['id'], 
                        output_path, 
                        metadata
                    )
                    
                    if not downloaded_file or not os.path.exists(downloaded_file):
                        logger.warning(f"Download failed for {track['name']}")
                        failed_tracks += 1
                        continue
                        
                    completed_tracks += 1
                    track_results.append({
                        'spotify_id': track['id'],
                        'youtube_id': best_match['id'],
                        'track_name': track['name'],
                        'artist_name': track['artists'][0]['name'],
                        'file_path': downloaded_file,
                        'file_size': os.path.getsize(downloaded_file),
                        'status': 'downloaded'
                    })
                    
                except Exception as e:
                    logger.error(f"Failed to download track {track['name']}: {e}")
                    failed_tracks += 1
                    
            self.db.update_queue_item(item_id, {
                'status': 'completed',
                'progress': 100,
                'completed_tracks': completed_tracks,
                'failed_tracks': failed_tracks,
                'dir_path': playlist_dir,
                'completed_at': datetime.now().isoformat(),
                'tracks': track_results
            })
            
            self.db.add_download_record({
                'type': 'playlist',
                'spotify_id': playlist_id,
                'playlist_name': playlist_info['name'],
                'owner_name': playlist_info['owner']['display_name'],
                'track_count': total_tracks,
                'completed_tracks': completed_tracks,
                'failed_tracks': failed_tracks,
                'dir_path': playlist_dir,
                'tracks': track_results,
                'source': 'spotify'
            })
            
            logger.info(f"Playlist downloaded: {playlist_info['name']} - {completed_tracks}/{total_tracks} tracks")
            
        except Exception as e:
            logger.error(f"Playlist download failed: {e}")
            self.db.update_queue_item(item_id, {
                'status': 'failed',
                'error': str(e),
                'completed_at': datetime.now().isoformat()
            })
            raise
            
    def queue_track(self, track_id):
        if track_id.startswith('http'):
            match = re.search(r'/track/([a-zA-Z0-9]+)', track_id)
            if match:
                track_id = match.group(1)
                
        queue_item = {
            'type': 'track',
            'spotify_id': track_id,
            'status': 'pending',
            'progress': 0,
            'added_at': datetime.now().isoformat()
        }
        
        item_id = self.db.add_to_queue(queue_item)
        
        self.download_queue.put((item_id, 'track', {'spotify_id': track_id}))
        
        return item_id
        
    def queue_album(self, album_id):
        if album_id.startswith('http'):
            match = re.search(r'/album/([a-zA-Z0-9]+)', album_id)
            if match:
                album_id = match.group(1)
                
        queue_item = {
            'type': 'album',
            'spotify_id': album_id,
            'status': 'pending',
            'progress': 0,
            'added_at': datetime.now().isoformat()
        }
        
        item_id = self.db.add_to_queue(queue_item)
        
        self.download_queue.put((item_id, 'album', {'spotify_id': album_id}))
        
        return item_id
        
    def queue_playlist(self, playlist_id):
        if playlist_id.startswith('http'):
            match = re.search(r'/playlist/([a-zA-Z0-9]+)', playlist_id)
            if match:
                playlist_id = match.group(1)
                
        queue_item = {
            'type': 'playlist',
            'spotify_id': playlist_id,
            'status': 'pending',
            'progress': 0,
            'added_at': datetime.now().isoformat()
        }
        
        item_id = self.db.add_to_queue(queue_item)
        
        self.download_queue.put((item_id, 'playlist', {'spotify_id': playlist_id}))
        
        return item_id
        
    def cancel_download(self, item_id):
        queue_items = self.db.get_queue()
        found = False
        
        for item in queue_items:
            if item.get('id') == item_id:
                found = True
                
                if item.get('status') == 'pending':
                    self.db.update_queue_item(item_id, {
                        'status': 'canceled',
                        'completed_at': datetime.now().isoformat()
                    })
                    return True
                    
                return False
                
        return False
        
    def get_queue_status(self):
        queue_items = self.db.get_queue()
        
        status_counts = {
            'pending': 0,
            'downloading': 0,
            'completed': 0,
            'failed': 0,
            'canceled': 0,
            'total': len(queue_items)
        }
        
        for item in queue_items:
            status = item.get('status', 'pending')
            status_counts[status] = status_counts.get(status, 0) + 1
            
        return status_counts
        
    def shutdown(self):
        logger.info("Shutting down download manager...")
        
        self.shutdown_flag.set()
        
        for _ in range(len(self.download_threads)):
            try:
                self.download_queue.put(None)
            except:
                pass
            
        for thread in self.download_threads:
            if thread.is_alive():
                thread.join(timeout=2)
                
        logger.info("Download manager shutdown complete.")

class FancyProgressBar:
    def __init__(self, total=100, prefix='', suffix='', length=50, fill='█', empty='░', style='default'):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.empty = empty
        self.style = style
        self.iteration = 0
        self.animation_frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.animation_index = 0
        self.start_time = time.time()
        
    def update(self, iteration):
        self.iteration = iteration
        
    def print_progress(self):
        percent = 100 * (self.iteration / float(self.total))
        filled_length = int(self.length * self.iteration // self.total)
        
        elapsed_time = time.time() - self.start_time
        if self.iteration > 0:
            eta = elapsed_time * (self.total / self.iteration - 1)
            eta_str = f" ETA: {int(eta//60):02d}:{int(eta%60):02d}"
        else:
            eta_str = " ETA: --:--"
        
        self.animation_index = (self.animation_index + 1) % len(self.animation_frames)
        spinner = self.animation_frames[self.animation_index]
        
        if self.style == 'rainbow':
            colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE]
            bar = ''
            for i in range(self.length):
                if i < filled_length:
                    color_idx = i % len(colors)
                    bar += colors[color_idx] + self.fill + Style.RESET_ALL
                else:
                    bar += self.empty
        elif self.style == 'pulse':
            pulse_position = filled_length
            bar = ''
            for i in range(self.length):
                if i < filled_length:
                    if i == pulse_position - 1:
                        bar += Fore.YELLOW + self.fill + Style.RESET_ALL
                    else:
                        bar += self.fill
                else:
                    bar += self.empty
        else:  # default
            bar = self.fill * filled_length + self.empty * (self.length - filled_length)
            
        speed = self.iteration / elapsed_time if elapsed_time > 0 else 0
        speed_str = f"{speed:.2f} it/s"
        
        sys.stdout.write(f"\r{spinner} {self.prefix} |{bar}| {percent:.1f}% {self.suffix} {speed_str}{eta_str}")
        sys.stdout.flush()

class SpotiFXApp:
    def __init__(self):
        create_directories()
        
        self.config = ConfigManager()
        self.credentials = CredentialsManager()
        self.db = DatabaseManager()
        self.cache = CacheManager()
        
        self.main_menu_options = [
            "Download a track",
            "Download an album",
            "Download a playlist",
            "View download queue",
            "Download history",
            "Settings",
            "About SpotiFX",
            "Exit"
        ]
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_logo(self):
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE]
        
        for i, line in enumerate(LOGO_ASCII.split('\n')):
            color = colors[i % len(colors)]
            print(f"{color}{line}{Style.RESET_ALL}")
            
        print(f"{Fore.YELLOW}🎵 The Ultimate Spotify Downloader 🎵{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Version {VERSION} - Created by Amir.Void (GitHub: AmirVoid12){Style.RESET_ALL}")
        print("=" * 60)
        
    def print_menu(self, options, title="MENU"):
        print(f"\n{Style.BRIGHT}{title}{Style.RESET_ALL}")
        
        for i, option in enumerate(options, 1):
            print(f"{Fore.CYAN}[{i}]{Style.RESET_ALL} {option}")
            
        choice = input(f"\n{Fore.YELLOW}Enter your choice (1-{len(options)}): {Style.RESET_ALL}")
        return choice
        
    def _setup_spotify(self):
        if self.credentials.has_spotify_credentials():
            client_id, client_secret = self.credentials.get_spotify_credentials()
            
            try:
                self.spotify = SpotifyClient(client_id, client_secret, self.cache)
                if self.spotify.test_connection():
                    return True
            except Exception as e:
                print(f"{Fore.RED}Error connecting to Spotify: {e}{Style.RESET_ALL}")
                
        return self._prompt_for_spotify_credentials()
        
    def _prompt_for_spotify_credentials(self):
        self.clear_screen()
        self.print_logo()
        
        print(f"{Fore.YELLOW}Spotify API Credentials Required{Style.RESET_ALL}")
        print("You need a Spotify Developer account to use this application.")
        print("1. Go to https://developer.spotify.com/dashboard/")
        print("2. Log in with your Spotify account")
        print("3. Create a new application")
        print("4. Copy the Client ID and Client Secret\n")
        
        if input("Would you like to open the Spotify Developer Dashboard in your browser? (y/n): ").lower() == 'y':
            webbrowser.open("https://developer.spotify.com/dashboard/")
            
        client_id = input("Enter your Spotify Client ID: ")
        client_secret = input("Enter your Spotify Client Secret: ")
        
        if not client_id or not client_secret:
            print(f"{Fore.RED}Invalid credentials provided.{Style.RESET_ALL}")
            return False
            
        try:
            self.spotify = SpotifyClient(client_id, client_secret, self.cache)
            if self.spotify.test_connection():
                self.credentials.set_spotify_credentials(client_id, client_secret)
                print(f"{Fore.GREEN}✓ Connected to Spotify API successfully!{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}Could not connect to Spotify API with provided credentials.{Style.RESET_ALL}")
                return False
        except Exception as e:
            print(f"{Fore.RED}Error connecting to Spotify: {e}{Style.RESET_ALL}")
            return False
            
    def _setup_downloader(self):
        self.youtube = YouTubeDownloader(self.config)
        
        self.download_manager = DownloadManager(
            self.spotify,
            self.youtube,
            self.db,
            self.config
        )
        
    def display_download_track_menu(self):
        self.clear_screen()
        self.print_logo()
        
        print(f"{Fore.YELLOW}Download a Track{Style.RESET_ALL}")
        
        track_input = input("Enter Spotify track URL or ID (or 'back' to return): ")
        
        if track_input.lower() == 'back':
            return
            
        if not (track_input.startswith('https://open.spotify.com/track/') or 
                track_input.startswith('spotify:track:') or
                re.match(r'^[a-zA-Z0-9]{22}$', track_input)):
            print(f"{Fore.RED}Invalid Spotify track URL or ID{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
            return
            
        try:
            print(f"{Fore.CYAN}Fetching track information...{Style.RESET_ALL}")
            
            if track_input.startswith('spotify:track:'):
                track_id = track_input.split(':')[-1]
            elif re.match(r'^[a-zA-Z0-9]{22}$', track_input):
                track_id = track_input
            else:
                match = re.search(r'/track/([a-zA-Z0-9]+)', track_input)
                track_id = match.group(1) if match else None
            
            if not track_id:
                print(f"{Fore.RED}Could not extract track ID{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                return
                
            track_info = self.spotify.get_track(track_id)
            if not track_info:
                print(f"{Fore.RED}Could not fetch track information{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                return
                
            print("\n" + "=" * 60)
            print(f"{Fore.GREEN}Track Information:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Title:{Style.RESET_ALL} {track_info['name']}")
            print(f"{Fore.CYAN}Artist:{Style.RESET_ALL} {track_info['artists'][0]['name']}")
            print(f"{Fore.CYAN}Album:{Style.RESET_ALL} {track_info['album']['name']}")
            print(f"{Fore.CYAN}Release Date:{Style.RESET_ALL} {track_info['album'].get('release_date', 'Unknown')}")
            duration_ms = track_info['duration_ms']
            minutes = int(duration_ms / 1000 / 60)
            seconds = int(duration_ms / 1000 % 60)
            print(f"{Fore.CYAN}Duration:{Style.RESET_ALL} {minutes}:{seconds:02d}")
            print(f"{Fore.CYAN}Popularity:{Style.RESET_ALL} {track_info['popularity']}")
            print("=" * 60)
            
            if input("\nDo you want to download this track? (y/n): ").lower() == 'y':
                item_id = self.download_manager.queue_track(track_id)
                
                print(f"{Fore.GREEN}✓ Track added to download queue (ID: {item_id[:8]}...){Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            
        input("\nPress Enter to continue...")
        
    def display_download_album_menu(self):
        self.clear_screen()
        self.print_logo()
        
        print(f"{Fore.YELLOW}Download an Album{Style.RESET_ALL}")
        
        album_input = input("Enter Spotify album URL or ID (or 'back' to return): ")
        
        if album_input.lower() == 'back':
            return
            
        if not (album_input.startswith('https://open.spotify.com/album/') or 
                album_input.startswith('spotify:album:') or
                re.match(r'^[a-zA-Z0-9]{22}$', album_input)):
            print(f"{Fore.RED}Invalid Spotify album URL or ID{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
            return
            
        try:
            print(f"{Fore.CYAN}Fetching album information...{Style.RESET_ALL}")
            
            if album_input.startswith('spotify:album:'):
                album_id = album_input.split(':')[-1]
            elif re.match(r'^[a-zA-Z0-9]{22}$', album_input):
                album_id = album_input
            else:
                match = re.search(r'/album/([a-zA-Z0-9]+)', album_input)
                album_id = match.group(1) if match else None
            
            if not album_id:
                print(f"{Fore.RED}Could not extract album ID{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                return
                
            album_info = self.spotify.get_album(album_id)
            if not album_info:
                print(f"{Fore.RED}Could not fetch album information{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                return
                
            print("\n" + "=" * 60)
            print(f"{Fore.GREEN}Album Information:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Title:{Style.RESET_ALL} {album_info['name']}")
            print(f"{Fore.CYAN}Artist:{Style.RESET_ALL} {album_info['artists'][0]['name']}")
            print(f"{Fore.CYAN}Release Date:{Style.RESET_ALL} {album_info.get('release_date', 'Unknown')}")
            print(f"{Fore.CYAN}Tracks:{Style.RESET_ALL} {album_info['total_tracks']}")
            print("=" * 60)
            
            print(f"\n{Fore.GREEN}Tracks:{Style.RESET_ALL}")
            for i, track in enumerate(album_info['tracks']['items'], 1):
                duration_ms = track.get('duration_ms', 0)
                minutes = int(duration_ms / 1000 / 60)
                seconds = int(duration_ms / 1000 % 60)
                print(f"{i}. {track['name']} ({minutes}:{seconds:02d})")
                
            if input("\nDo you want to download this album? (y/n): ").lower() == 'y':
                item_id = self.download_manager.queue_album(album_id)
                
                print(f"{Fore.GREEN}✓ Album added to download queue (ID: {item_id[:8]}...){Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            
        input("\nPress Enter to continue...")
        
    def display_download_playlist_menu(self):
        self.clear_screen()
        self.print_logo()
        
        print(f"{Fore.YELLOW}Download a Playlist{Style.RESET_ALL}")
        
        playlist_input = input("Enter Spotify playlist URL or ID (or 'back' to return): ")
        
        if playlist_input.lower() == 'back':
            return
            
        if not (playlist_input.startswith('https://open.spotify.com/playlist/') or 
                playlist_input.startswith('spotify:playlist:') or
                re.match(r'^[a-zA-Z0-9]{22}$', playlist_input)):
            print(f"{Fore.RED}Invalid Spotify playlist URL or ID{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
            return
            
        try:
            print(f"{Fore.CYAN}Fetching playlist information...{Style.RESET_ALL}")
            
            if playlist_input.startswith('spotify:playlist:'):
                playlist_id = playlist_input.split(':')[-1]
            elif re.match(r'^[a-zA-Z0-9]{22}$', playlist_input):
                playlist_id = playlist_input
            else:
                match = re.search(r'/playlist/([a-zA-Z0-9]+)', playlist_input)
                playlist_id = match.group(1) if match else None
            
            if not playlist_id:
                print(f"{Fore.RED}Could not extract playlist ID{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                return
                
            playlist_info = self.spotify.get_playlist(playlist_id)
            if not playlist_info:
                print(f"{Fore.RED}Could not fetch playlist information{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                return
                
            print("\n" + "=" * 60)
            print(f"{Fore.GREEN}Playlist Information:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Title:{Style.RESET_ALL} {playlist_info['name']}")
            print(f"{Fore.CYAN}Owner:{Style.RESET_ALL} {playlist_info['owner']['display_name']}")
            print(f"{Fore.CYAN}Description:{Style.RESET_ALL} {playlist_info.get('description', 'No description')}")
            print(f"{Fore.CYAN}Tracks:{Style.RESET_ALL} {playlist_info['tracks']['total']}")
            print("=" * 60)
            
            if playlist_info['tracks']['total'] > 50:
                print(f"{Fore.YELLOW}Warning: This playlist contains {playlist_info['tracks']['total']} tracks. Downloading may take a while.{Style.RESET_ALL}")
                
            if input("\nDo you want to download this playlist? (y/n): ").lower() == 'y':
                item_id = self.download_manager.queue_playlist(playlist_id)
                
                print(f"{Fore.GREEN}✓ Playlist added to download queue (ID: {item_id[:8]}...){Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            
        input("\nPress Enter to continue...")
        
    def display_queue_menu(self):
        self.clear_screen()
        self.print_logo()
        
        print(f"{Fore.YELLOW}Download Queue{Style.RESET_ALL}")
        
        queue_status = self.download_manager.get_queue_status()
        
        print("\n" + "=" * 60)
        print(f"{Fore.GREEN}Queue Status:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Pending:{Style.RESET_ALL} {queue_status.get('pending', 0)}")
        print(f"{Fore.CYAN}Downloading:{Style.RESET_ALL} {queue_status.get('downloading', 0)}")
        print(f"{Fore.CYAN}Completed:{Style.RESET_ALL} {queue_status.get('completed', 0)}")
        print(f"{Fore.CYAN}Failed:{Style.RESET_ALL} {queue_status.get('failed', 0)}")
        print(f"{Fore.CYAN}Canceled:{Style.RESET_ALL} {queue_status.get('canceled', 0)}")
        print(f"{Fore.CYAN}Total:{Style.RESET_ALL} {queue_status.get('total', 0)}")
        print("=" * 60)
        
        active_queue = self.db.get_queue('downloading')
        pending_queue = self.db.get_queue('pending')
        
        if active_queue:
            print(f"\n{Fore.GREEN}Active Downloads:{Style.RESET_ALL}")
            
            for item in active_queue:
                progress = item.get('progress', 0)
                progress_bar = '█' * int(progress / 10) + '░' * (10 - int(progress / 10))
                
                if item.get('type') == 'track':
                    name = f"{item.get('artist_name', '')} - {item.get('track_name', '')}"
                elif item.get('type') == 'album':
                    name = f"{item.get('artist_name', '')} - {item.get('album_name', '')}"
                elif item.get('type') == 'playlist':
                    name = item.get('playlist_name', '')
                else:
                    name = "Unknown"
                    
                print(f"ID: {item.get('id', '')[:8]}... | {item.get('type', 'unknown').capitalize()} | {name}")
                print(f"Status: [{progress_bar}] {progress}% | {item.get('note', '')}")
                print("-" * 60)
                
        if pending_queue:
            print(f"\n{Fore.GREEN}Pending Downloads:{Style.RESET_ALL}")
            
            for item in pending_queue:
                added_at = item.get('added_at', '')
                if added_at:
                    try:
                        dt = datetime.fromisoformat(added_at)
                        added_at = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        pass
                        
                print(f"ID: {item.get('id', '')[:8]}... | {item.get('type', 'unknown').capitalize()} | Added: {added_at}")
                
        print("\nOptions:")
        print("1. Refresh Queue")
        print("2. Cancel Download")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            self.display_queue_menu()
        elif choice == "2":
            item_id = input("Enter the ID of the download to cancel: ")
            if self.download_manager.cancel_download(item_id):
                print(f"{Fore.GREEN}✓ Download canceled successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Could not cancel download. It may be already in progress or completed.{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
            self.display_queue_menu()
            
    def display_download_history_menu(self):
        self.clear_screen()
        self.print_logo()
        
        print(f"{Fore.YELLOW}Download History{Style.RESET_ALL}")
        
        history = self.db.get_download_history(limit=20)
        
        if not history:
            print(f"{Fore.YELLOW}No download history found.{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
            return
            
        print("\n" + "=" * 60)
        print(f"{Fore.GREEN}Recent Downloads:{Style.RESET_ALL}")
        
        for item in history:
            timestamp = item.get('timestamp', '')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    timestamp = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
                    
            if item.get('type') == 'track':
                name = f"{item.get('artist_name', '')} - {item.get('track_name', '')}"
                status = "Downloaded"
            elif item.get('type') == 'album':
                name = f"{item.get('artist_name', '')} - {item.get('album_name', '')}"
                status = f"{item.get('completed_tracks', 0)}/{item.get('track_count', 0)} tracks"
            elif item.get('type') == 'playlist':
                name = item.get('playlist_name', '')
                status = f"{item.get('completed_tracks', 0)}/{item.get('track_count', 0)} tracks"
            else:
                name = "Unknown"
                status = "Unknown"
                
            print(f"Date: {timestamp} | {item.get('type', 'unknown').capitalize()} | {name} | {status}")
            
        print("=" * 60)
        
        print("\nOptions:")
        print("1. View Download Statistics")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            self.display_download_statistics()
            input("\nPress Enter to continue...")
            self.display_download_history_menu()
            
    def display_download_statistics(self):
        self.clear_screen()
        self.print_logo()
        
        print(f"{Fore.YELLOW}Download Statistics{Style.RESET_ALL}")
        
        stats = self.db.get_stats()
        
        print("\n" + "=" * 60)
        print(f"{Fore.CYAN}Total Tracks Downloaded:{Style.RESET_ALL} {stats.get('total_tracks', 0)}")
        print(f"{Fore.CYAN}Total Playlists Downloaded:{Style.RESET_ALL} {stats.get('total_playlists', 0)}")
        
        total_bytes = stats.get('total_bytes_downloaded', 0)
        if total_bytes < 1024:
            size_str = f"{total_bytes} B"
        elif total_bytes < 1024 * 1024:
            size_str = f"{total_bytes/1024:.2f} KB"
        elif total_bytes < 1024 * 1024 * 1024:
            size_str = f"{total_bytes/(1024*1024):.2f} MB"
        else:
            size_str = f"{total_bytes/(1024*1024*1024):.2f} GB"
            
        print(f"{Fore.CYAN}Total Data Downloaded:{Style.RESET_ALL} {size_str}")
        
        first_date = stats.get('first_download_date', '')
        if first_date:
            try:
                dt = datetime.fromisoformat(first_date)
                first_date = dt.strftime("%Y-%m-%d %H:%M")
            except:
                pass
        print(f"{Fore.CYAN}First Download:{Style.RESET_ALL} {first_date or 'Never'}")
        
        last_date = stats.get('last_download_date', '')
        if last_date:
            try:
                dt = datetime.fromisoformat(last_date)
                last_date = dt.strftime("%Y-%m-%d %H:%M")
            except:
                pass
        print(f"{Fore.CYAN}Last Download:{Style.RESET_ALL} {last_date or 'Never'}")
        print("=" * 60)
        
    def display_settings_menu(self):
        self.clear_screen()
        self.print_logo()
        
        print(f"{Fore.YELLOW}Settings{Style.RESET_ALL}")
        
        print("\n" + "=" * 60)
        print(f"{Fore.GREEN}Current Settings:{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}Download Directory:{Style.RESET_ALL} {self.config.get('General', 'download_dir', DEFAULT_DOWNLOAD_DIR)}")
        print(f"{Fore.CYAN}Concurrent Downloads:{Style.RESET_ALL} {self.config.get('General', 'concurrent_downloads', '3')}")
        print(f"{Fore.CYAN}Audio Quality:{Style.RESET_ALL} {self.config.get('Audio', 'audio_quality', '320')} kbps")
        print(f"{Fore.CYAN}Audio Format:{Style.RESET_ALL} {self.config.get('Audio', 'audio_format', 'mp3')}")
        print(f"{Fore.CYAN}Create Playlist Folders:{Style.RESET_ALL} {'Yes' if self.config.getboolean('Spotify', 'create_playlist_folders', True) else 'No'}")
        print("=" * 60)
        
        print("\nSettings Menu:")
        print("1. Change Download Directory")
        print("2. Change Concurrent Downloads")
        print("3. Change Audio Quality")
        print("4. Toggle Playlist Folders")
        print("5. Clear Cache")
        print("6. Reset Settings")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            current = self.config.get('General', 'download_dir', DEFAULT_DOWNLOAD_DIR)
            new_dir = input(f"Enter new download directory [{current}]: ") or current
            
            try:
                os.makedirs(new_dir, exist_ok=True)
                self.config.set('General', 'download_dir', new_dir)
                print(f"{Fore.GREEN}✓ Download directory updated{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error creating directory: {e}{Style.RESET_ALL}")
                
            input("\nPress Enter to continue...")
            self.display_settings_menu()
            
        elif choice == "2":
            current = self.config.getint('General', 'concurrent_downloads', 3)
            new_value = input(f"Enter maximum concurrent downloads (1-10) [{current}]: ") or str(current)
            
            if new_value.isdigit() and 1 <= int(new_value) <= 10:
                self.config.set('General', 'concurrent_downloads', new_value)
                print(f"{Fore.GREEN}✓ Concurrent downloads updated{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Note: This change will take effect after restarting the application.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid value. Please enter a number between 1 and 10.{Style.RESET_ALL}")
            
            input("\nPress Enter to continue...")
            self.display_settings_menu()
            
        elif choice == "3":
            current = self.config.get('Audio', 'audio_quality', '320')
            print("Audio Quality Options:")
            print("1. 128 kbps")
            print("2. 192 kbps")
            print("3. 256 kbps")
            print("4. 320 kbps")
            
            quality_choice = input(f"Select audio quality [current: {current} kbps]: ")
            
            if quality_choice == "1":
                self.config.set('Audio', 'audio_quality', '128')
                print(f"{Fore.GREEN}✓ Audio quality updated to 128 kbps{Style.RESET_ALL}")
            elif quality_choice == "2":
                self.config.set('Audio', 'audio_quality', '192')
                print(f"{Fore.GREEN}✓ Audio quality updated to 192 kbps{Style.RESET_ALL}")
            elif quality_choice == "3":
                self.config.set('Audio', 'audio_quality', '256')
                print(f"{Fore.GREEN}✓ Audio quality updated to 256 kbps{Style.RESET_ALL}")
            elif quality_choice == "4":
                self.config.set('Audio', 'audio_quality', '320')
                print(f"{Fore.GREEN}✓ Audio quality updated to 320 kbps{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid choice. Audio quality not changed.{Style.RESET_ALL}")
            
            input("\nPress Enter to continue...")
            self.display_settings_menu()
            
        elif choice == "4":
            current = self.config.getboolean('Spotify', 'create_playlist_folders', True)
            new_value = not current
            
            self.config.set('Spotify', 'create_playlist_folders', str(new_value).lower())
            print(f"{Fore.GREEN}✓ Playlist folders {'enabled' if new_value else 'disabled'}{Style.RESET_ALL}")
            
            input("\nPress Enter to continue...")
            self.display_settings_menu()
            
        elif choice == "5":
            if input("Are you sure you want to clear the cache? (y/n): ").lower() == 'y':
                cleared = self.cache.clear()
                print(f"{Fore.GREEN}✓ Cache cleared ({cleared} items removed){Style.RESET_ALL}")
                
            input("\nPress Enter to continue...")
            self.display_settings_menu()
            
        elif choice == "6":
            if input("Are you sure you want to reset all settings to default? (y/n): ").lower() == 'y':
                self.config._create_default_config()
                print(f"{Fore.GREEN}✓ Settings reset to default{Style.RESET_ALL}")
                
            input("\nPress Enter to continue...")
            self.display_settings_menu()
            
    def display_about_menu(self):
        self.clear_screen()
        self.print_logo()
        
        print(f"{Fore.YELLOW}About SpotiFX{Style.RESET_ALL}")
        
        print("\n" + "=" * 60)
        print(f"SpotiFX {VERSION}")
        print("\nSpotiFX is an advanced Spotify music downloader that lets you download")
        print("your favorite tracks, albums, and playlists for offline listening.")
        print("\nFeatures:")
        print("- Download tracks, albums, and playlists from Spotify")
        print("- High-quality audio downloads")
        print("- Metadata tagging with album art")
        print("- Queue system for batch downloads")
        print("- Download history and statistics")
        print("- Customizable settings")
        print("\nTechnical Information:")
        print(f"- Python Version: {sys.version.split()[0]}")
        print(f"- Platform: {platform.system()} {platform.release()}")
        print(f"- Download Directory: {self.config.get('General', 'download_dir', DEFAULT_DOWNLOAD_DIR)}")
        print("\nCreated by Amir.Void (GitHub: AmirVoid12)")
        print("\nAcknowledgements:")
        print("This software is for educational purposes only. Please respect copyright laws")
        print("and artists' rights. Support your favorite artists by purchasing their music")
        print("or using paid streaming services.")
        print("=" * 60)
        
        input("\nPress Enter to continue...")
        
    def run(self):
        try:
            if not self._setup_spotify():
                print(f"{Fore.RED}Failed to set up Spotify client. Exiting.{Style.RESET_ALL}")
                return
                
            self._setup_downloader()
            
            running = True
            while running:
                self.clear_screen()
                self.print_logo()
                
                choice = self.print_menu(self.main_menu_options, "MAIN MENU")
                
                if choice == '1':
                    self.display_download_track_menu()
                elif choice == '2':
                    self.display_download_album_menu()
                elif choice == '3':
                    self.display_download_playlist_menu()
                elif choice == '4':
                    self.display_queue_menu()
                elif choice == '5':
                    self.display_download_history_menu()
                elif choice == '6':
                    self.display_settings_menu()
                elif choice == '7':
                    self.display_about_menu()
                elif choice == '8':
                    running = False
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                    time.sleep(1)
                    
            print(f"{Fore.YELLOW}Shutting down SpotiFX...{Style.RESET_ALL}")
            if hasattr(self, 'download_manager'):
                self.download_manager.shutdown()
            print(f"{Fore.GREEN}✓ Goodbye!{Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Interrupted by user. Shutting down...{Style.RESET_ALL}")
            if hasattr(self, 'download_manager'):
                self.download_manager.shutdown()
                
        except Exception as e:
            print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
            logger.error(f"Unexpected error: {e}")
            if hasattr(self, 'download_manager'):
                self.download_manager.shutdown()
                
    def display_help_menu(self):
        self.clear_screen()
        self.print_logo()
        
        print(f"{Fore.YELLOW}Help & Usage Instructions{Style.RESET_ALL}")
        
        print("\n" + "=" * 60)
        print("SpotiFX Command Line Usage:")
        print(f"\npython spotifx.py [options]")
        print("\nOptions:")
        print("  -t, --track URL     Download a Spotify track")
        print("  -a, --album URL     Download a Spotify album")
        print("  -p, --playlist URL  Download a Spotify playlist")
        print("  -d, --dir PATH      Set custom download directory")
        print("  -h, --help          Show this help message")
        print("  -v, --version       Show version information")
        
        print("\nExamples:")
        print("  python spotifx.py -t https://open.spotify.com/track/12345abcde")
        print("  python spotifx.py -a https://open.spotify.com/album/12345abcde")
        print("  python spotifx.py -p https://open.spotify.com/playlist/12345abcde -d /path/to/downloads")
        
        print("\nSpotify URLs:")
        print("SpotiFX accepts the following Spotify URL formats:")
        print("- https://open.spotify.com/track/...")
        print("- https://open.spotify.com/album/...")
        print("- https://open.spotify.com/playlist/...")
        print("- spotify:track:...")
        print("- spotify:album:...")
        print("- spotify:playlist:...")
        print("- Direct Spotify IDs (22 character alphanumeric strings)")
        
        print("\nSettings:")
        print("SpotiFX stores settings in:")
        print(f"  {CONFIG_DIR}")
        print("=" * 60)
        
        input("\nPress Enter to continue...")
        
    def display_search_menu(self):
        self.clear_screen()
        self.print_logo()
        
        print(f"{Fore.YELLOW}Search Spotify{Style.RESET_ALL}")
        
        search_query = input("Enter search query (or 'back' to return): ")
        
        if search_query.lower() == 'back':
            return
            
        if not search_query:
            print(f"{Fore.RED}No search query provided.{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
            return
            
        try:
            print(f"{Fore.CYAN}Searching Spotify...{Style.RESET_ALL}")
            
            results = self.spotify.search(search_query, search_type='track,album,playlist', limit=5)
            
            if not results:
                print(f"{Fore.RED}No results found.{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                return
                
            tracks = results.get('tracks', {}).get('items', [])
            albums = results.get('albums', {}).get('items', [])
            playlists = results.get('playlists', {}).get('items', [])
            
            items = []
            
            if tracks:
                print(f"\n{Fore.GREEN}Tracks:{Style.RESET_ALL}")
                for i, track in enumerate(tracks, 1):
                    print(f"{i}. {track['name']} - {track['artists'][0]['name']} ({track['album']['name']})")
                    items.append(('track', track['id'], track['external_urls']['spotify']))
                    
            if albums:
                print(f"\n{Fore.GREEN}Albums:{Style.RESET_ALL}")
                for i, album in enumerate(albums, len(items) + 1):
                    print(f"{i}. {album['name']} - {album['artists'][0]['name']} ({album['release_date']})")
                    items.append(('album', album['id'], album['external_urls']['spotify']))
                    
            if playlists:
                print(f"\n{Fore.GREEN}Playlists:{Style.RESET_ALL}")
                for i, playlist in enumerate(playlists, len(items) + 1):
                    print(f"{i}. {playlist['name']} - {playlist['owner']['display_name']} ({playlist['tracks']['total']} tracks)")
                    items.append(('playlist', playlist['id'], playlist['external_urls']['spotify']))
                    
            if not items:
                print(f"{Fore.RED}No results found.{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                return
                
            print("\nOptions:")
            print("Enter the number of an item to download")
            print("0. Back to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == "0":
                return
                
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(items):
                    item_type, item_id, item_url = items[choice_num - 1]
                    
                    if item_type == 'track':
                        print(f"{Fore.CYAN}Adding track to download queue...{Style.RESET_ALL}")
                        self.download_manager.queue_track(item_id)
                    elif item_type == 'album':
                        print(f"{Fore.CYAN}Adding album to download queue...{Style.RESET_ALL}")
                        self.download_manager.queue_album(item_id)
                    elif item_type == 'playlist':
                        print(f"{Fore.CYAN}Adding playlist to download queue...{Style.RESET_ALL}")
                        self.download_manager.queue_playlist(item_id)
                        
                    print(f"{Fore.GREEN}✓ Item added to download queue{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            
        input("\nPress Enter to continue...")
        
    def display_export_menu(self):
        self.clear_screen()
        self.print_logo()
        
        print(f"{Fore.YELLOW}Export Data{Style.RESET_ALL}")
        
        print("\nExport options:")
        print("1. Export Download History")
        print("2. Export Current Queue")
        print("3. Export Settings")
        print("4. Export All Data")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "0":
            return
            
        try:
            if choice == "1":
                history = self.db.get_download_history()
                filename = os.path.join(self.download_dir, f"spotifx_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(history, f, indent=2)
                    
                print(f"{Fore.GREEN}✓ Download history exported to {filename}{Style.RESET_ALL}")
                
            elif choice == "2":
                queue = self.db.get_queue()
                filename = os.path.join(self.download_dir, f"spotifx_queue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(queue, f, indent=2)
                    
                print(f"{Fore.GREEN}✓ Current queue exported to {filename}{Style.RESET_ALL}")
                
            elif choice == "3":
                filename = os.path.join(self.download_dir, f"spotifx_settings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ini")
                
                with open(filename, 'w', encoding='utf-8') as f:
                    self.config.config.write(f)
                    
                print(f"{Fore.GREEN}✓ Settings exported to {filename}{Style.RESET_ALL}")
                
            elif choice == "4":
                export_dir = os.path.join(self.download_dir, f"spotifx_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                os.makedirs(export_dir, exist_ok=True)
                
                history_file = os.path.join(export_dir, "history.json")
                with open(history_file, 'w', encoding='utf-8') as f:
                    json.dump(self.db.get_download_history(), f, indent=2)
                    
                queue_file = os.path.join(export_dir, "queue.json")
                with open(queue_file, 'w', encoding='utf-8') as f:
                    json.dump(self.db.get_queue(), f, indent=2)
                    
                settings_file = os.path.join(export_dir, "settings.ini")
                with open(settings_file, 'w', encoding='utf-8') as f:
                    self.config.config.write(f)
                    
                stats_file = os.path.join(export_dir, "stats.json")
                with open(stats_file, 'w', encoding='utf-8') as f:
                    json.dump(self.db.get_stats(), f, indent=2)
                    
                print(f"{Fore.GREEN}✓ All data exported to {export_dir}{Style.RESET_ALL}")
                
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}Error exporting data: {e}{Style.RESET_ALL}")
            
        input("\nPress Enter to continue...")
        
    def display_batch_download_menu(self):
        self.clear_screen()
        self.print_logo()
        
        print(f"{Fore.YELLOW}Batch Download{Style.RESET_ALL}")
        
        print("\nOptions:")
        print("1. Download from file")
        print("2. Paste multiple URLs")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "0":
            return
            
        try:
            if choice == "1":
                file_path = input("Enter path to file containing Spotify URLs (one per line): ")
                
                if not os.path.exists(file_path):
                    print(f"{Fore.RED}File not found: {file_path}{Style.RESET_ALL}")
                    input("\nPress Enter to continue...")
                    return
                    
                with open(file_path, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]
                    
                if not urls:
                    print(f"{Fore.RED}No URLs found in file.{Style.RESET_ALL}")
                    input("\nPress Enter to continue...")
                    return
                    
                print(f"{Fore.CYAN}Found {len(urls)} URLs in file.{Style.RESET_ALL}")
                
            elif choice == "2":
                print("Paste multiple Spotify URLs (one per line, end with an empty line):")
                urls = []
                while True:
                    line = input()
                    if not line:
                        break
                    urls.append(line.strip())
                    
                if not urls:
                    print(f"{Fore.RED}No URLs provided.{Style.RESET_ALL}")
                    input("\nPress Enter to continue...")
                    return
                    
                print(f"{Fore.CYAN}Found {len(urls)} URLs.{Style.RESET_ALL}")
                
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                return
                
            added_count = {'track': 0, 'album': 0, 'playlist': 0, 'unknown': 0}
            
            for url in urls:
                if '/track/' in url or url.startswith('spotify:track:'):
                    self.download_manager.queue_track(url)
                    added_count['track'] += 1
                elif '/album/' in url or url.startswith('spotify:album:'):
                    self.download_manager.queue_album(url)
                    added_count['album'] += 1
                elif '/playlist/' in url or url.startswith('spotify:playlist:'):
                    self.download_manager.queue_playlist(url)
                    added_count['playlist'] += 1
                else:
                    added_count['unknown'] += 1
                    
            print(f"{Fore.GREEN}✓ Added to download queue:{Style.RESET_ALL}")
            print(f"  - Tracks: {added_count['track']}")
            print(f"  - Albums: {added_count['album']}")
            print(f"  - Playlists: {added_count['playlist']}")
            
            if added_count['unknown'] > 0:
                print(f"{Fore.YELLOW}Skipped {added_count['unknown']} unknown URLs.{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            
        input("\nPress Enter to continue...")
    
    def display_troubleshooting_menu(self):
        self.clear_screen()
        self.print_logo()
        
        print(f"{Fore.YELLOW}Troubleshooting{Style.RESET_ALL}")
        
        print("\nTroubleshooting options:")
        print("1. Test Spotify API connection")
        print("2. Test YouTube downloader")
        print("3. Check system requirements")
        print("4. Clear cache")
        print("5. Reset configuration")
        print("6. Show logs")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "0":
            return
            
        try:
            if choice == "1":
                print(f"{Fore.CYAN}Testing Spotify API connection...{Style.RESET_ALL}")
                
                if not hasattr(self, 'spotify'):
                    print(f"{Fore.RED}Spotify client not initialized. Please set up credentials first.{Style.RESET_ALL}")
                    input("\nPress Enter to continue...")
                    return
                    
                if self.spotify.test_connection():
                    print(f"{Fore.GREEN}✓ Spotify API connection successful!{Style.RESET_ALL}")
                    
                    print("\nFetching some data to verify access...")
                    try:
                        new_releases = self.spotify.sp.new_releases(limit=1)
                        if new_releases and 'albums' in new_releases and 'items' in new_releases['albums']:
                            album = new_releases['albums']['items'][0]
                            print(f"Successfully fetched new release: {album['name']} by {album['artists'][0]['name']}")
                    except Exception as e:
                        print(f"{Fore.YELLOW}Data fetch test failed: {e}{Style.RESET_ALL}")
                        
                else:
                    print(f"{Fore.RED}✗ Spotify API connection failed.{Style.RESET_ALL}")
                    print("Please check your credentials and try again.")
                    
            elif choice == "2":
                print(f"{Fore.CYAN}Testing YouTube downloader...{Style.RESET_ALL}")
                
                if not hasattr(self, 'youtube'):
                    self.youtube = YouTubeDownloader(self.config)
                    
                test_query = "test audio sample"
                print(f"Searching YouTube for '{test_query}'...")
                
                results = self.youtube.search_youtube(test_query, limit=1)
                
                if results:
                    print(f"{Fore.GREEN}✓ YouTube search successful!{Style.RESET_ALL}")
                    result = results[0]
                    print(f"Found: {result.get('title')} (ID: {result.get('id')})")
                    
                    if input("\nDo you want to test downloading? (y/n): ").lower() == 'y':
                        print(f"{Fore.CYAN}Testing download (this may take a moment)...{Style.RESET_ALL}")
                        
                        test_dir = os.path.join(self.download_dir, "test")
                        os.makedirs(test_dir, exist_ok=True)
                        
                        test_path = os.path.join(test_dir, "youtube_test.mp3")
                        
                        def progress_callback(info):
                            if info['status'] == 'downloading':
                                downloaded = info.get('downloaded_bytes', 0)
                                total = info.get('total_bytes') or info.get('total_bytes_estimate', 0)
                                
                                if total > 0:
                                    percent = int(downloaded * 100 / total)
                                    bar = '█' * (percent // 5) + '░' * (20 - percent // 5)
                                    print(f"\r[{bar}] {percent}%", end='', flush=True)
                                    
                        self.youtube.add_progress_hook(progress_callback)
                        
                        downloaded_file = self.youtube.download_audio(
                            result['id'],
                            test_path
                        )
                        
                        self.youtube.progress_hooks.remove(progress_callback)
                        
                        if downloaded_file and os.path.exists(downloaded_file):
                            print(f"\n{Fore.GREEN}✓ Download test successful!{Style.RESET_ALL}")
                            print(f"Downloaded to: {downloaded_file}")
                            print(f"File size: {os.path.getsize(downloaded_file) / 1024:.2f} KB")
                            
                            if input("\nDo you want to delete the test file? (y/n): ").lower() == 'y':
                                try:
                                    os.remove(downloaded_file)
                                    print(f"{Fore.GREEN}✓ Test file deleted.{Style.RESET_ALL}")
                                except Exception as e:
                                    print(f"{Fore.YELLOW}Could not delete test file: {e}{Style.RESET_ALL}")
                        else:
                            print(f"\n{Fore.RED}✗ Download test failed.{Style.RESET_ALL}")
                    
                else:
                    print(f"{Fore.RED}✗ YouTube search failed.{Style.RESET_ALL}")
                    
            elif choice == "3":
                print(f"{Fore.CYAN}Checking system requirements...{Style.RESET_ALL}")
                
                print("\nPython version:", sys.version)
                print("Platform:", platform.platform())
                
                requirements = {
                    'requests': 'For making HTTP requests',
                    'spotipy': 'For Spotify API access',
                    'yt_dlp': 'For YouTube downloads',
                    'mutagen': 'For audio metadata',
                    'colorama': 'For console colors'
                }
                
                print("\nChecking required packages:")
                all_installed = True
                
                for package, description in requirements.items():
                    try:
                        __import__(package)
                        version = "Unknown"
                        if package == 'requests':
                            version = requests.__version__
                        elif package == 'spotipy':
                            version = spotipy.__version__
                        elif package == 'yt_dlp':
                            version = yt_dlp.version.__version__
                        elif package == 'mutagen':
                            version = mutagen.__version__
                        elif package == 'colorama':
                            version = colorama.__version__
                            
                        print(f"{Fore.GREEN}✓ {package} - v{version} - {description}{Style.RESET_ALL}")
                    except (ImportError, AttributeError):
                        print(f"{Fore.RED}✗ {package} - Not found - {description}{Style.RESET_ALL}")
                        all_installed = False
                        
                if all_installed:
                    print(f"\n{Fore.GREEN}All required packages are installed.{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.YELLOW}Some required packages are missing.{Style.RESET_ALL}")
                    print("Run 'pip install -r requirements.txt' to install them.")
                    
                print("\nChecking external dependencies:")
                
                try:
                    ffmpeg_output = subprocess.check_output(['ffmpeg', '-version'], stderr=subprocess.STDOUT, text=True)
                    ffmpeg_version = ffmpeg_output.split('\n')[0].split(' ')[2] if ffmpeg_output else "Unknown"
                    print(f"{Fore.GREEN}✓ FFmpeg - v{ffmpeg_version} - For audio conversion{Style.RESET_ALL}")
                except (subprocess.SubprocessError, FileNotFoundError):
                    print(f"{Fore.RED}✗ FFmpeg - Not found - For audio conversion{Style.RESET_ALL}")
                    print("  Please install FFmpeg: https://ffmpeg.org/download.html")
                    
            elif choice == "4":
                if input("Are you sure you want to clear the cache? (y/n): ").lower() == 'y':
                    cleared = self.cache.clear()
                    print(f"{Fore.GREEN}✓ Cache cleared ({cleared} items removed){Style.RESET_ALL}")
                    
            elif choice == "5":
                if input("Are you sure you want to reset all configuration? (y/n): ").lower() == 'y':
                    self.config._create_default_config()
                    print(f"{Fore.GREEN}✓ Configuration reset to defaults.{Style.RESET_ALL}")
                    print("Please restart the application for changes to take effect.")
                    
            elif choice == "6":
                log_file = os.path.join(CONFIG_DIR, "spotifx.log")
                
                if os.path.exists(log_file):
                    print(f"{Fore.CYAN}Last 20 lines of log file:{Style.RESET_ALL}\n")
                    
                    with open(log_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for line in lines[-20:]:
                            print(line.strip())
                            
                    if input("\nDo you want to view the full log file? (y/n): ").lower() == 'y':
                        if os.name == 'nt':  # Windows
                            os.system(f'notepad {log_file}')
                        else:  # Unix-like
                            os.system(f'cat {log_file} | less')
                else:
                    print(f"{Fore.YELLOW}No log file found.{Style.RESET_ALL}")
                    
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            
        input("\nPress Enter to continue...")

def parse_arguments():
    import argparse
    
    parser = argparse.ArgumentParser(description=f"SpotiFX v{VERSION} - Advanced Spotify Music Downloader")
    parser.add_argument('-t', '--track', help='Download a Spotify track by URL or ID')
    parser.add_argument('-a', '--album', help='Download a Spotify album by URL or ID')
    parser.add_argument('-p', '--playlist', help='Download a Spotify playlist by URL or ID')
    parser.add_argument('-d', '--directory', help='Custom download directory')
    parser.add_argument('-v', '--version', action='version', version=f'SpotiFX v{VERSION}')
    
    return parser.parse_args()

def init_colorama():
    try:
        init(autoreset=True)
    except:
        pass

def check_system():
    if sys.version_info < (3, 6):
        print(f"{Fore.RED}Error: SpotiFX requires Python 3.6 or higher{Style.RESET_ALL}")
        print(f"Your Python version: {sys.version}")
        return False
        
    return True

def print_banner():
    width = os.get_terminal_size().columns
    
    print("\n" + "=" * width)
    print(Fore.CYAN + LOGO_ASCII + Style.RESET_ALL)
    print(Fore.YELLOW + "  🎵 SpotiFX - Advanced Spotify Music Downloader 🎵" + Style.RESET_ALL)
    print(Fore.CYAN + f"  Version {VERSION} - Created by Amir.Void (GitHub: AmirVoid12)" + Style.RESET_ALL)
    print("=" * width + "\n")

def main():
    init_colorama()
    
    if not check_system():
        return 1
        
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    
    args = parse_arguments()
    
    app = SpotiFXApp()
    
    if args.directory:
        app.config.set('General', 'download_dir', args.directory)
        
    if args.track or args.album or args.playlist:
        if not app._setup_spotify():
            print(f"{Fore.RED}Failed to set up Spotify client. Exiting.{Style.RESET_ALL}")
            return 1
            
        app._setup_downloader()
        
        if args.track:
            print(f"{Fore.CYAN}Downloading track: {args.track}{Style.RESET_ALL}")
            app.download_manager.queue_track(args.track)
            
        if args.album:
            print(f"{Fore.CYAN}Downloading album: {args.album}{Style.RESET_ALL}")
            app.download_manager.queue_album(args.album)
            
        if args.playlist:
            print(f"{Fore.CYAN}Downloading playlist: {args.playlist}{Style.RESET_ALL}")
            app.download_manager.queue_playlist(args.playlist)
            
        print(f"{Fore.YELLOW}Waiting for downloads to complete...{Style.RESET_ALL}")
        
        try:
            while not app.download_manager.download_queue.empty():
                time.sleep(1)
                
            print(f"{Fore.GREEN}✓ Downloads completed!{Style.RESET_ALL}")
        except:
            pass
            
        app.download_manager.shutdown()
        
    else:
        app.run()
        
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Interrupted by user. Exiting...{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)

# -- END OF WRITING CODE -- 