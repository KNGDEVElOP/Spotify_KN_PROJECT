
import configparser


class Auth():
    def __init__(self,config_path="utils/Config.ini"):
        self._SPOTIPY_CLIENT_ID = None
        self._SPOTIPY_CLIENT_SECRET = None
        self._SPOTIPY_REDIRECT_URI = None
        try:
                # Cargar archivo de configuración
            config = configparser.ConfigParser()
            config.read(config_path)
                
                # Leer las configuraciones desde el archivo y asignarlas
            self._SPOTIPY_CLIENT_ID = config.get("api", "CLIENT_ID")
            self._SPOTIPY_CLIENT_SECRET = config.get("api", "CLIENT_SECRET")
            self._SPOTIPY_REDIRECT_URI = config.get("api", "REDIRECT_URI")
            
        except Exception as e:
            
            print(f"❌ Error al abrir el archivo de configuración: {e}")
            raise e

        
    @property
    def get_spotify_client_id(self):
        """Devuelve el CLIENT_ID de Spotify"""
        return self._SPOTIPY_CLIENT_ID
    @property
    def get_spotify_client_secret(self):
        """Devuelve el CLIENT_SECRET de Spotify"""
        return self._SPOTIPY_CLIENT_SECRET
    @property
    def get_spotify_redirect_uri(self):
        """Devuelve el REDIRECT_URI de Spotify"""
        return self._SPOTIPY_REDIRECT_URI
    
    
if __name__ == '__main__':
    q=Auth()
    q.get_spotify_client_id
    
    