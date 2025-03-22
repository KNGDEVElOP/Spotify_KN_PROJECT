import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

from controllers import Spotify_Connector as sc  
import logging as log  
from typing import List, Dict, Optional, Any  

log.basicConfig(level=log.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class SpotifyManager:
    """
    Clase encargada de obtener información de Spotify (canciones y artistas más escuchados).
    Implementa el patrón Singleton para asegurar que solo haya una instancia.
    """

    _instance = None  
    _initialized = False  

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SpotifyManager, cls).__new__(cls)
            cls._instance._initialized = False  
        return cls._instance  

    def __init__(self):
        if self._initialized:  
            return

        self.logger = log.getLogger(__name__)  
        self.spotify = None  
        self.logger.info("SpotifyManager initialized")
        self.offset = 0  

        try:
            connector = sc.spotifyConnector()
            self.spotify = connector.authenticate()
            self.logger.info("✅ Conexión con Spotify establecida correctamente")
            self._initialized = True  

        except Exception as e:
            self.logger.error(f"❌ Error al inicializar SpotifyManager: {e}")
            SpotifyManager._instance = None  
            raise e

    def is_authenticated(self) -> bool:
        return self.spotify is not None

    def get_top_tracks(self, limit: int = 50, time_range: str = "long_term") -> Optional[List[Dict[str, Any]]]:
        """
        Obtiene las canciones más escuchadas del usuario con paginación.

        Args:
            limit (int): Número total de canciones a obtener (máximo permitido por solicitud: 50).
            time_range (str): Periodo de tiempo ('short_term', 'medium_term', 'long_term').

        Returns:
            Optional[List[Dict[str, Any]]]: Lista de canciones más escuchadas o None en caso de error.
        """
        if not self.is_authenticated():
            self.logger.error("❌ No se pueden obtener canciones: autenticación fallida")
            return None

        all_tracks = []
        self.offset = 0  

        try:
            while limit > 0:
                current_limit = min(50, limit)  
                top_tracks = self.spotify.current_user_top_tracks(
                    limit=current_limit, 
                    offset=self.offset, 
                    time_range=time_range
                )

                if "items" not in top_tracks or not top_tracks["items"]:
                    if self.offset == 0:  
                        self.logger.warning("⚠ No se encontraron canciones en el historial")
                        return None
                    else:  
                        break

                all_tracks.extend(top_tracks["items"])  

                if len(top_tracks["items"]) < current_limit:
                    break

                limit -= current_limit
                self.offset += current_limit

            self.logger.info(f"🎵 {len(all_tracks)} canciones recuperadas correctamente")
            return all_tracks

        except Exception as e:
            self.logger.error(f"❌ Error al obtener canciones: {e}")
            return None

    def get_top_artists(self, limit: int = 15, time_range: str = "long_term") -> Optional[List[Dict[str, Any]]]:
        """
        Obtiene los artistas más escuchados del usuario.

        Args:
            limit (int): Número total de artistas a obtener (máximo permitido por solicitud: 50).
            time_range (str): Periodo de tiempo ('short_term', 'medium_term', 'long_term').

        Returns:
            Optional[List[Dict[str, Any]]]: Lista de artistas más escuchados o None en caso de error.
        """
        if not self.is_authenticated():
            self.logger.error("❌ No se pueden obtener artistas: autenticación fallida")
            return None
            
        try:
            self.offset = 0  
            all_artists = []

            while limit > 0:
                current_limit = min(50, limit)  
                top_artists = self.spotify.current_user_top_artists(
                    limit=current_limit,
                    offset=self.offset,
                    time_range=time_range
                )
                
                if "items" not in top_artists or not top_artists["items"]:
                    if self.offset == 0:
                        self.logger.warning("⚠ No se encontraron artistas en el historial")
                        return None
                    else:
                        break

                all_artists.extend(top_artists["items"])

                if len(top_artists["items"]) < current_limit:
                    break

                limit -= current_limit
                self.offset += current_limit

            self.logger.info(f"🎵 {len(all_artists)} artistas recuperados correctamente")
            return all_artists
            
        except Exception as e:
            self.logger.error(f"❌ Error al obtener artistas: {e}")
            return None


# Bloque principal para ejecutar el código
if __name__ == "__main__":
    try:
        spotify_info = SpotifyManager()
        tracks_list = spotify_info.get_top_tracks(limit=100, time_range="medium_term")
        artists_list = spotify_info.get_top_artists(limit=30, time_range="medium_term")

        if tracks_list:
            print("\n🎶 Tus canciones más escuchadas:\n")
            for i, track in enumerate(tracks_list, 1):
                track_name = track.get("name", "Desconocido")
                artist_name = track["artists"][0]["name"] if track.get("artists") else "Desconocido"
                print(f"{i}. {track_name} - {artist_name}")
        
        if artists_list:
            print("\n🎶 Tus artistas más escuchados:\n")
            for i, artist in enumerate(artists_list, 1):
                print(f"{i}. {artist.get('name', 'Desconocido')}")

    except Exception as e:
        print(f"\n❌ Error en la ejecución: {e}")
