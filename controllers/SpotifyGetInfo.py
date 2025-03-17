
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

from controllers import Spotify_Connector as sc # Importar la conexión con Spotify
import logging as log  # Importar el módulo logging para registrar información y errores

# Configuración básica del logging
log.basicConfig(level=log.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class GetTracks:
    """
    Clase encargada de obtener la información de Spotify (por ejemplo, las canciones más escuchadas)
    utilizando la API de Spotify a través de la clase `spotifyConnector` de `Spotify_Connector`.
    Implementa el patrón Singleton para asegurar que solo haya una instancia en toda la ejecución.
    """

    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls, *args, **kwargs):
        """Método para aplicar el patrón Singleton, asegurando una única instancia."""
        if cls._instance is None:
            cls._instance = super(GetTracks, cls).__new__(cls)
            cls._instance._initialized = False  # Marcar como no inicializado
        return cls._instance  # Retornar la misma instancia cada vez que se llame a la clase

    def __init__(self):
        """Inicializa la clase GetTracks, configura el logger y establece la conexión con Spotify."""
        if self._initialized:  # Si ya fue inicializado, no volver a ejecutarlo
            return

        self.logger = log.getLogger(__name__)  # Inicializar el logger
        self.spotify = None  # Inicializar la variable que contendrá la API autenticada
        self.logger.info("SpotifyGetInfo initialized")

        try:
            # Crear una instancia de `spotifyConnector` y autenticar
            connector = sc.spotifyConnector()
            self.spotify = connector.authenticate()
            self.logger.info("✅ Conexión con Spotify establecida correctamente")
            self._initialized = True  # Marcar la instancia como inicializada

        except Exception as e:
            self.logger.error(f"❌ Error al inicializar SpotifyGetInfo: {e}")
            GetTracks._instance = None  # Eliminar la instancia en caso de error
            raise e

    def is_authenticated(self):
        """
        Verifica si la autenticación con Spotify fue exitosa.
        
        Retorna:
        - (bool) True si la autenticación fue exitosa, False en caso contrario.
        """
        return self.spotify is not None

    def get_top_tracks(self, limit=15):
        """
        Obtiene las canciones más escuchadas del usuario desde la API de Spotify.

        Parámetros:
        limit (int): Número máximo de canciones a obtener (por defecto 15).

        Retorna:
        list | None: Lista de las canciones más escuchadas del usuario o None en caso de error.
        """
        if not self.is_authenticated():
            self.logger.error("❌ No se pueden obtener canciones: autenticación fallida")
            return None

        try:
            # Obtener las canciones más escuchadas
            top_tracks = self.spotify.current_user_top_tracks(limit=limit,time_range='long_term')

            # Verificar si la respuesta tiene datos
            if "items" not in top_tracks or not top_tracks["items"]:
                self.logger.warning("⚠ No se encontraron canciones en el historial")
                return None

            self.logger.info(f"🎵 {len(top_tracks['items'])} canciones recuperadas correctamente")
            return top_tracks["items"]

        except Exception as e:
            self.logger.error(f"❌ Error al obtener canciones: {e}")
            return None


# Bloque principal para ejecutar el código
if __name__ == "__main__":
    try:
        # Instanciar la clase Singleton (si ya existe, usa la misma)
        spotify_info = GetTracks()
        tracks_list = spotify_info.get_top_tracks(limit=15)

        # Imprimir las canciones de manera legible
        if tracks_list:
            print("\n🎶 Tus canciones más escuchadas:\n")
            for i, track in enumerate(tracks_list, 1):
                track_name = track.get("name", "Desconocido")
                artists = track.get("artists", [])
                artist_name = artists[0]["name"] if artists else "Desconocido"
                print(f"{i}. {track_name} - {artist_name}")
        else:
            print("\n❌ No se pudieron obtener las canciones.")

    except Exception as e:
        print(f"\n❌ Error en la ejecución: {e}")
