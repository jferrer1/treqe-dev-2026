#!/usr/bin/env python3
"""
Script para configurar dominio treqe.es en Netlify automáticamente.
Usa Netlify API vía netlify CLI.
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
            print(f"❌ Error ejecutando: {' '.join(cmd)}")
            print(f"Stderr: {result.stderr}")
            return None
        
        # Intentar parsear JSON si la salida es JSON
        if result.stdout.strip().startswith("{"):
            return json.loads(result.stdout)
        return result.stdout
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return None

def get_site_info():
    """Obtiene información del sitio Netlify"""
    print("📡 Obteniendo información del sitio Netlify...")
    info = run_netlify_command(["status", "--json"])
    
    if info and "siteData" in info:
        site_id = info["siteData"]["site-id"]
        site_name = info["siteData"]["site-name"]
        print(f"✅ Sitio: {site_name} (ID: {site_id})")
        return site_id
    else:
        print("❌ No se pudo obtener información del sitio")
        return None

def add_domain_via_api(site_id, domain):
    """Añade dominio usando Netlify API"""
    print(f"🌐 Añadiendo dominio: {domain}")
    
    # Usamos netlify api para añadir dominio
    api_data = {
        "site_id": site_id,
        "domain": domain
    }
    
    # Intentamos con diferentes métodos API
    methods = ["createSiteDomain", "addSiteDomain", "provisionSiteDomain"]
    
    for method in methods:
        print(f"  Intentando método: {method}")
        cmd = ["api", method, "--data", json.dumps(api_data)]
        result = run_netlify_command(cmd)
        
        if result:
            print(f"✅ Dominio {domain} añadido exitosamente")
            return True
    
    print(f"❌ No se pudo añadir dominio {domain} via API")
    return False

def verify_dns(domain):
    """Verifica configuración DNS"""
    print(f"🔍 Verificando DNS para {domain}...")
    
    try:
        import socket
        ip = socket.gethostbyname(domain)
        print(f"✅ {domain} → {ip}")
        
        # Verificar si apunta a Netlify (75.2.60.5)
        if ip == "75.2.60.5":
            print("✅ DNS correctamente configurado (apunta a Netlify)")
            return True
        else:
            print(f"⚠️  DNS apunta a {ip}, debería ser 75.2.60.5 (Netlify)")
            return False
    except Exception as e:
        print(f"❌ No se pudo resolver DNS: {e}")
        return False

def main():
    print("=" * 50)
    print("🚀 CONFIGURADOR AUTOMÁTICO DOMINIO NETLIFY")
    print("=" * 50)
    
    # 1. Obtener site ID
    site_id = get_site_info()
    if not site_id:
        print("❌ No se pudo continuar sin site ID")
        return 1
    
    # 2. Verificar DNS
    domains = ["treqe.es", "www.treqe.es"]
    dns_ok = True
    
    for domain in domains:
        if not verify_dns(domain):
            dns_ok = False
    
    if not dns_ok:
        print("⚠️  DNS no configurado correctamente. Configura primero en Dinahosting:")
        print("   @ → 75.2.60.5")
        print("   www → 75.2.60.5")
        return 1
    
    # 3. Añadir dominios (intento via API)
    print("\n🎯 Añadiendo dominios a Netlify...")
    
    # Método alternativo: Usar netlify open para configuración manual
    print("\n📋 Método alternativo: Abriendo configuración Netlify en navegador...")
    
    # Abrir configuración de dominios en navegador
    subprocess.run(["start", "https://app.netlify.com/sites/sparkling-sawine-898bad/domains"], shell=True)
    
    print("\n" + "=" * 50)
    print("📋 INSTRUCCIONES MANUALES (si API falla):")
    print("=" * 50)
    print("1. En la página que se abrió, busca 'Add custom domain'")
    print("2. Escribe: treqe.es")
    print("3. Marca: 'Add www.treqe.es as alias'")
    print("4. Clic en 'Verify'")
    print("5. Espera 5-15 minutos para SSL automático")
    print("\n6. Verificar después:")
    print("   curl -I https://treqe.es")
    print("   Debe devolver 200 OK")
    print("=" * 50)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())