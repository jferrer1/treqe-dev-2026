#!/usr/bin/env python3
"""
Servidor simple para probar la landing page de Treqe localmente
"""

import http.server
import socketserver
import webbrowser
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        # Reducir verbosidad de logs
        pass

def main():
    os.chdir(DIRECTORY)
    
    print("=" * 60)
    print("SERVIDOR LANDING PAGE TREQE")
    print("=" * 60)
    print(f"Directorio: {DIRECTORY}")
    print(f"Puerto: {PORT}")
    print(f"URL: http://localhost:{PORT}")
    print("=" * 60)
    print("\nArchivos disponibles:")
    
    # Listar archivos
    for file in os.listdir(DIRECTORY):
        if file.endswith(('.html', '.css', '.js', '.md')):
            print(f"  • {file}")
    
    print("\n" + "=" * 60)
    print("Iniciando servidor...")
    print("Presiona Ctrl+C para detener")
    print("=" * 60)
    
    # Abrir navegador automáticamente
    try:
        webbrowser.open(f'http://localhost:{PORT}')
    except:
        print("No se pudo abrir el navegador automáticamente")
    
    # Iniciar servidor
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServidor detenido por el usuario")
            httpd.shutdown()

if __name__ == "__main__":
    main()