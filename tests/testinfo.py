import unittest
from unittest.mock import patch, MagicMock
from controllers.SpotifyGetInfo import SpotifyManager  

class TestSpotifyManager(unittest.TestCase):
    
    def setUp(self):
        """Configura una instancia de SpotifyManager antes de cada prueba"""
        self.spotify_manager = SpotifyManager()  

    @patch("controllers.Spotify_Connector.spotifyConnector.authenticate")  
    def test_get_top_tracks_success(self, mock_authenticate):
        """Prueba obtener top tracks con una respuesta válida"""
        
        # Simulación de datos de respuesta de la API de Spotify
        mock_spotify = MagicMock()
        mock_spotify.current_user_top_tracks.return_value = {
            "items": [
                {"name": "Song 1", "artists": [{"name": "Artist 1"}]},
                {"name": "Song 2", "artists": [{"name": "Artist 2"}]}
            ]
        }
        
        # Asignamos el objeto mock a la instancia de SpotifyManager
        mock_authenticate.return_value = mock_spotify
        self.spotify_manager.spotify = mock_spotify  # Asegurar que se usa el mock

        # Ejecutar la función de prueba
        tracks = self.spotify_manager.get_top_tracks(limit=2)
        
        # Verificaciones
        self.assertIsNotNone(tracks)  # Asegurar que tracks no es None
        self.assertEqual(len(tracks), 2)  # Deben ser exactamente 2 canciones
        self.assertEqual(tracks[0]["name"], "Song 1")  # Primera canción correcta
        self.assertEqual(tracks[1]["artists"][0]["name"], "Artist 2")  # Segundo artista correcto

    @patch("controllers.Spotify_Connector.spotifyConnector.authenticate")  
    def test_get_top_artists_success(self, mock_authenticate):
        """Prueba obtener artistas más escuchados con una respuesta válida"""
        
        # Simulación de datos de respuesta de la API de Spotify
        mock_spotify = MagicMock()
        mock_spotify.current_user_top_artists.return_value = {
            "items": [
                {"name": "Artist 1"},
                {"name": "Artist 2"}
            ]
        }
        
        # Asignamos el objeto mock a la instancia de SpotifyManager
        mock_authenticate.return_value = mock_spotify
        self.spotify_manager.spotify = mock_spotify  # Asegurar que se usa el mock

        # Ejecutar la función de prueba
        artists = self.spotify_manager.get_top_artists(limit=2)
        
        # Verificaciones
        self.assertIsNotNone(artists)  # Asegurar que artists no es None
        self.assertEqual(len(artists), 2)  # Deben ser exactamente 2 artistas
        self.assertEqual(artists[0]["name"], "Artist 1")  # Primer artista correcto
        self.assertEqual(artists[1]["name"], "Artist 2")  # Segundo artista correcto

    @patch("controllers.Spotify_Connector.spotifyConnector.authenticate")  
    def test_get_top_tracks_empty(self, mock_authenticate):
        """Prueba cuando no se encuentran canciones"""
        
        # Simulación de respuesta vacía
        mock_spotify = MagicMock()
        mock_spotify.current_user_top_tracks.return_value = {"items": []}
        
        # Asignamos el objeto mock a la instancia de SpotifyManager
        mock_authenticate.return_value = mock_spotify
        self.spotify_manager.spotify = mock_spotify  # Asegurar que se usa el mock

        # Ejecutar la función de prueba
        tracks = self.spotify_manager.get_top_tracks(limit=2)
        
        # Verificación
        self.assertIsNone(tracks)  # Debería devolver None cuando no haya canciones

    @patch("controllers.Spotify_Connector.spotifyConnector.authenticate")  
    def test_get_top_artists_empty(self, mock_authenticate):
        """Prueba cuando no se encuentran artistas"""
        
        # Simulación de respuesta vacía
        mock_spotify = MagicMock()
        mock_spotify.current_user_top_artists.return_value = {"items": []}
        
        # Asignamos el objeto mock a la instancia de SpotifyManager
        mock_authenticate.return_value = mock_spotify
        self.spotify_manager.spotify = mock_spotify  # Asegurar que se usa el mock

        # Ejecutar la función de prueba
        artists = self.spotify_manager.get_top_artists(limit=2)
        
        # Verificación
        self.assertIsNone(artists)  # Debería devolver None cuando no haya artistas

    @patch("controllers.Spotify_Connector.spotifyConnector.authenticate")  
    def test_get_top_tracks_error(self, mock_authenticate):
        """Prueba cuando ocurre un error en la API al obtener las canciones"""
        
        # Simulación de error en la llamada a la API
        mock_spotify = MagicMock()
        mock_spotify.current_user_top_tracks.side_effect = Exception("Error en la API")
        
        # Asignamos el objeto mock a la instancia de SpotifyManager
        mock_authenticate.return_value = mock_spotify
        self.spotify_manager.spotify = mock_spotify  # Asegurar que se usa el mock

        # Ejecutar la función de prueba y verificar el error
        tracks = self.spotify_manager.get_top_tracks(limit=2)
        self.assertIsNone(tracks)  # Debería devolver None cuando ocurre un error

    @patch("controllers.Spotify_Connector.spotifyConnector.authenticate")  
    def test_authentication_failure(self, mock_authenticate):
        """Prueba cuando la autenticación falla"""
        
        # Configuramos el mock para lanzar una excepción
        mock_authenticate.side_effect = Exception("Autenticación fallida")

        # Ahora, cuando intentemos inicializar SpotifyManager, esperamos que lance una excepción
        with self.assertRaises(Exception):
            self.spotify_manager = spotifyConnector()  # Esto debería disparar la excepción
        


if __name__ == "__main__":
    unittest.main()
