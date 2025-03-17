
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Agregar la carpeta raíz del proyecto al PYTHONPATH

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from utils.ReaderProps import Auth
import logging


class spotifyConnector:
    """Clase para manejar la conexión con Spotify usando OAuth"""

    def __init__(self):
        """Inicializa el logger y configura la conexión con Spotify"""
        self.logger = logging.getLogger(__name__)

        # Obtener las credenciales usando la clase Auth
        ec = Auth()
        self.client_id = ec.get_spotify_client_id
        self.client_secret = ec.get_spotify_client_secret
        self.redirect_uri = ec.get_spotify_redirect_uri
        self.scope = "user-top-read playlist-modify-public"
        
        try:
            # Intentar autenticar
            self.spotify = self.authenticate()
            self.logger.info("Spotify Connector initialized")
        except Exception as e:
            self.logger.error(f"Spotify Connector failed to initialize: {e}")
            raise e

    def authenticate(self):
        """Autentica la conexión con Spotify y devuelve la instancia autenticada"""
        return spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_path=".cache"
        ))

# Bloque principal para probar la conexión
if __name__ == "__main__":
    try:
        connector = spotifyConnector()
        
        # Comprobar si la autenticación fue exitosa
        if connector.spotify:
            print("✅ Conexión exitosa con Spotify")
        else:
            print("❌ No se pudo conectar con Spotify")
    except Exception as e:
        print(f"❌ Error en la autenticación: {e}")
