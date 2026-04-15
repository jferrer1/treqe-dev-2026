# 🎯 DEMO PRIVADA TREQE - SOLO PARA TI

## 📋 **RESUMEN**
- **Backend:** `localhost:8000` (solo tu PC)
- **Landing page:** Archivo local (solo tu navegador)
- **Acceso:** 100% privado, nadie más puede ver
- **Dominios:** Registrados pero NO publicados

## 🚀 **CÓMO EJECUTAR LA DEMO**

### **OPCIÓN 1: SCRIPT AUTOMÁTICO (RECOMENDADO)**
1. Doble clic en `open_demo_local.bat`
2. Espera 3 segundos
3. Se abren 3 ventanas:
   - Terminal con backend (localhost:8000)
   - Landing page en navegador
   - Navegador con API docs

### **OPCIÓN 2: MANUAL**
```bash
# Terminal 1: Backend API
cd backend
python demo_local.py

# Terminal 2: Abrir landing page
# Navega a: file:///C:/Users/Shadow/.openclaw/workspace/projects/Treqe/landing-page/index.html
```

## 🔗 **URLS LOCALES**

### **BACKEND API:**
- **Raíz:** http://localhost:8000
- **Health:** http://localhost:8000/health
- **Usuarios:** http://localhost:8000/api/v1/users
- **Login:** http://localhost:8000/api/v1/users/login?username=ana_tech&password=password123
- **Matching:** http://localhost:8000/api/v1/matching/find/1
- **Items:** http://localhost:8000/api/v1/items

### **LANDING PAGE:**
- **Local:** `file:///C:/Users/Shadow/.openclaw/workspace/projects/Treqe/landing-page/index.html`
- **Solo funciona** desde tu navegador local

## 👤 **USUARIOS DEMO**

| Usuario | Password | ID |
|---------|----------|----|
| `ana_tech` | `password123` | 1 |
| `carlos_deportes` | `password123` | 2 |
| `beatriz_eco` | `password123` | 3 |

## 🎯 **QUÉ PROBAR**

### **1. Backend API:**
```bash
# Verificar que funciona
curl http://localhost:8000/health

# Ver usuarios demo
curl http://localhost:8000/api/v1/users

# Probar login
curl "http://localhost:8000/api/v1/users/login?username=ana_tech&password=password123"

# Probar matching
curl http://localhost:8000/api/v1/matching/find/1
```

### **2. Landing Page:**
- Abrir archivo local
- Ver diseño completo
- Probar formularios (alertas locales)
- Ver demo del intercambio circular

### **3. Algoritmo Demo:**
- El endpoint `/api/v1/matching/find/{id}` devuelve:
  - Ciclo de intercambio k=3
  - Resumen financiero
  - Comisiones calculadas

## 🛡️ **SEGURIDAD/PRIVACIDAD**

### **¿Por qué es 100% privado?**
1. **localhost:** Solo accesible desde tu máquina
2. **Archivos locales:** No subidos a internet
3. **Sin DNS:** Dominios registrados pero no configurados
4. **Sin servidor público:** Todo corre localmente

### **Para acceso remoto seguro (si necesitas):**
```bash
# SSH Tunnel (recomendado)
ssh -L 8000:localhost:8000 usuario@tu_ip

# Ngrok (temporal)
ngrok http 8000
# Solo tú tienes la URL
```

## 💰 **DOMINIOS REGISTRADOS**

### **Estado actual:**
- `treqe.es` - Registrado pero **NO configurado**
- `treqe.com.es` - Registrado pero **NO configurado**
- **DNS:** Sin configurar (parking mode)
- **Acceso público:** CERO

### **Cuándo hacer público:**
1. Cuando tengas MVP funcional
2. Cuando quieras lanzar waitlist
3. Cuando estés listo para early adopters

## 🔧 **TROUBLESHOOTING**

### **Problema: Backend no inicia**
```bash
# Verificar Python y dependencias
python --version
pip install fastapi uvicorn

# Verificar base de datos
cd backend
dir treqe_demo.db
# Si no existe: python crear_datos_final.py
```

### **Problema: Landing page no carga**
- Asegúrate de usar `file:///` protocolo
- Chrome/Edge funcionan mejor que otros navegadores
- Deshabilitar bloqueadores de contenido para archivos locales

### **Problema: API no responde**
```bash
# Verificar que el proceso está corriendo
netstat -an | find "8000"

# Reiniciar backend
Ctrl+C en terminal
python demo_local.py
```

## 🚀 **PRÓXIMOS PASOS**

### **FASE ACTUAL: DEMO PRIVADA**
- ✅ Backend local funcionando
- ✅ Landing page local
- ✅ Algoritmo demo integrado
- ✅ Total privacidad

### **FASE SIGUIENTE: MVP CERRADO**
- Landing page con password protection
- Backend en servidor privado
- Acceso por invitación solo

### **FASE FINAL: PÚBLICO**
- Landing page en treqe.es
- Waitlist abierta
- Early adopters program

## 📞 **SUPORTE**
- **Problemas técnicos:** Revisar troubleshooting
- **Preguntas estrategia:** Documentado en memoria
- **Privacidad:** 100% garantizada en esta fase

---
**Última actualización:** 20 marzo 2026  
**Estado:** ✅ DEMO PRIVADA LISTA  
**Acceso:** 🔒 SOLO LOCALHOST