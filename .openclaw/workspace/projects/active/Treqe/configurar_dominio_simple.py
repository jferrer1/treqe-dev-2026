#!/usr/bin/env python3
"""
Script para configurar dominio treqe.es en Netlify automáticamente.
Version simple sin emojis para Windows.
"""

import subprocess
import json
import sys
import os

def run_netlify_command(command):
    """Ejecuta comando netlify y devuelve resultado JSON"""
    try:
        cmd = ["npx", "netlify"] + command
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode != 0:
            print(f"ERROR ejecutando: {' '.join(cmd)}")
            print(f"Stderr: {result.stderr}")
            return None
        
        # Intentar parsear JSON si la salida es JSON
        if result.stdout.strip().startswith("{"):
            return json.loads(result.stdout)
        return result.stdout
    except Exception as e:
        print(f"EXCEPCION: {e}")
        return None

def main():
    print("=" * 50)
    print("CONFIGURADOR AUTOMATICO DOMINIO NETLIFY")
    print("=" * 50)
    
    # 1. Obtener información del sitio
    print("Obteniendo informacion del sitio Netlify...")
    info = run_netlify_command(["status", "--json"])
    
    if info and "siteData" in info:
        site_id = info["siteData"]["site-id"]
        site_name = info["siteData"]["site-name"]
        print(f"OK Sitio: {site_name} (ID: {site_id})")
    else:
        print("ERROR: No se pudo obtener informacion del sitio")
        site_id = "fe01fff1-84d7-483e-b037-35c682cb96d8"  # ID conocido
    
    # 2. Verificar DNS
    print("\nVerificando DNS...")
    import socket
    try:
        ip_treqe = socket.gethostbyname("treqe.es")
        ip_www = socket.gethostbyname("www.treqe.es")
        
        print(f"treqe.es -> {ip_treqe}")
        print(f"www.treqe.es -> {ip_www}")
        
        if ip_treqe == "75.2.60.5" and ip_www == "75.2.60.5":
            print("OK DNS correctamente configurado (apunta a Netlify)")
        else:
            print("ADVERTENCIA: DNS no apunta a Netlify (75.2.60.5)")
            print("Configura en Dinahosting:")
            print("  @ -> 75.2.60.5")
            print("  www -> 75.2.60.5")
    except Exception as e:
        print(f"ERROR resolviendo DNS: {e}")
    
    # 3. Abrir configuracion Netlify en navegador
    print("\nAbriendo configuracion Netlify en navegador...")
    
    # Abrir diferentes URLs de Netlify
    urls = [
        "https://app.netlify.com/sites/sparkling-sawine-898bad/domains",
        "https://app.netlify.com/sites/sparkling-sawine-898bad/overview",
        "https://app.netlify.com/teams/mvptreqe/sites"
    ]
    
    for url in urls:
        try:
            subprocess.run(["start", url], shell=True)
        except:
            pass
    
    print("\n" + "=" * 50)
    print("INSTRUCCIONES MANUALES:")
    print("=" * 50)
    print("1. En Netlify, busca 'Domain management' o 'Add custom domain'")
    print("2. Escribe: treqe.es")
    print("3. Marca: 'Add www.treqe.es as alias' (si aparece)")
    print("4. Clic en 'Verify' o 'Continue'")
    print("5. Netlify verificara DNS (ya configurado)")
    print("6. Espera 5-15 minutos para SSL automatico")
    print("\n7. Verificar despues:")
    print("   curl -I https://treqe.es")
    print("   Debe devolver 200 OK")
    print("=" * 50)
    
    # 4. Intentar usar API de Netlify
    print("\nIntentando configuracion automatica via API...")
    
    # Método 1: Usar netlify api si está disponible
    api_methods = [
        ["api", "getSite", "--data", json.dumps({"site_id": site_id})],
        ["open"],  # Abre panel de control
        ["deploy", "--prod"]  # Forzar redeploy
    ]
    
    for method in api_methods:
        print(f"Probando: netlify {' '.join(method)}")
        result = run_netlify_command(method)
        if result:
            print("OK Comando ejecutado")
            break
    
    return 0

if __name__ == "__main__":
    sys.exit(main())