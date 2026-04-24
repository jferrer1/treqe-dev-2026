# Treqe — Flujo completo de la app (10 pantallas)

> Documento de diseño de interfaz — 24 Abril 2026
> Prototipos desplegados en GitHub Pages

---

## 🗺️ Mapa de navegación

```
                    ┌─────────────────┐
                    │   v9 SPLASH     │  (1 vez al abrir)
                    │   treqe.        │
                    │   carga 2.2s    │
                    └────────┬────────┘
                             │ auto
                             ▼
 ┌─── NO ───┐ ┌─────────────────┐
 │ REGISTRO │ │  v5 ONBOARDING  │  (solo primera vez)
 │ opcional │ │  3 slides       │
 └──────────┘ │  swipe / dots   │
              └────────┬────────┘
                       │ "Ver catálogo"
                       ▼
              ┌─────────────────┐
              │  v10 REGISTRO   │  (cuando quiera participar)
              │  Google / Apple │
              │  / Email        │
              │  "Saltar" → cat │
              └────────┬────────┘
                       │ crear cuenta
                       ▼
              ┌─────────────────┐
              │  v1 CATÁLOGO    │  ← PÁGINA PRINCIPAL
              │  grid items     │
              │  search/filtros │
              │  scoring mini   │
              └──┬─────┬──────┬─┘
                 │     │      │
    ─────────────┘     │      └──────────────
   │              ┌────┴───┐              │
   ▼              ▼        ▼              ▼
┌────────┐ ┌───────────┐ ┌──────┐  ┌───────────┐
│v2 DETAL│ │v3 SUBIR   │ │v4    │  │v6 MATCH   │
│artículo │ │artículo   │ │PERFIL│  │notificación│
│         │ │formulario │ │      │  │(push/llegada)
│2 CTAs:  │ │fotos      │ │score │  │ ────────  │
│comprar/ │ │categorías │ │stats │  │bottom sheet│
│trueque  │ │precio     │ │acts  │  │⬆️ aceptar  │
│         │ │            │ │items │  │⬇️ cancelar │
└────┬────┘ └───────────┘ └──┬───┘  └─────┬─────┘
     │                       │            │ aceptado
     │"Solicitar"            │            ▼
     ▼                       │    ┌───────────────┐
  (match pendiente)          │    │ v7 SEGUIMIENTO│
     │                       │    │ timeline 6    │
     │recibir notif          │    │ pasos         │
     └──────→  v6  ←─────────┘    │ descargar     │
              │                   │ etiqueta      │
              └─────→ v7 ←───────┘               │
                                                 │
                    ┌──────────┐                  │
                    │ v8       │  ←── desde perfil│
                    │ AJUSTES  │                  │
                    │ toggles  │                  │
                    │ cerrar   │                  │
                    │ sesión   │                  │
                    └──────────┘                  │
```

---

## 🔗 Enlaces a prototipos

| # | Pantalla | URL |
|---|----------|-----|
| 🚀 v9 | Splash / Carga | <https://jferrer1.github.io/treqe-dev-2026/treqe-app/designs/v9-splash/> |
| 🚀 v5 | Onboarding (3 slides) | <https://jferrer1.github.io/treqe-dev-2026/treqe-app/designs/v5-onboarding/> |
| 📝 v10 | Registro (Google/Apple/Email) | <https://jferrer1.github.io/treqe-dev-2026/treqe-app/designs/v10-registro/> |
| 🏠 v1 | Catálogo (home) | <https://jferrer1.github.io/treqe-dev-2026/treqe-app/designs/v1-catalogo/> |
| 🎸 v2 | Detalle artículo | <https://jferrer1.github.io/treqe-dev-2026/treqe-app/designs/v2-detalle/> |
| 📸 v3 | Subir artículo | <https://jferrer1.github.io/treqe-dev-2026/treqe-app/designs/v3-subir/> |
| 👤 v4 | Perfil / Scoring | <https://jferrer1.github.io/treqe-dev-2026/treqe-app/designs/v4-perfil/> |
| 🎉 v6 | Match notificación | <https://jferrer1.github.io/treqe-dev-2026/treqe-app/designs/v6-match-notification/> |
| 📦 v7 | Seguimiento envío | <https://jferrer1.github.io/treqe-dev-2026/treqe-app/designs/v7-seguimiento/> |
| ⚙️ v8 | Ajustes | <https://jferrer1.github.io/treqe-dev-2026/treqe-app/designs/v8-ajustes/> |

---

## 🧭 Navegación detallada

### Bottom nav (persistente en pantallas principales)

```
🔍 Catálogo (v1)  |  ➕ Subir (v3)  |  👤 Perfil (v4)
```

### Flujo de entrada (primera vez)

```
Splash v9 (2.2s animación de carga)
  → Onboarding v5 (3 slides swipeables con dots)
    → "Ver catálogo" → Catálogo v1
    → "Inicia sesión" → Registro v10
      → "Saltar" → Catálogo v1 (sin cuenta)
      → Google / Apple / Email → crear cuenta → Catálogo v1
```

### Flujo de entrada (usuario recurrente)

```
Splash v9 (2.2s)
  → Sesión activa detectada → Catálogo v1 (salta onboarding y registro)
```

### Flujo de intercambio (core de la app)

```
1. Catálogo v1 → usuario busca/navega artículos
2. Tap en artículo → Detalle v2
3. En Detalle v2:
   - "💳 Comprar con tarjeta" → compra directa
   - "🔄 Solicitar con trueque" → selector de tus artículos + diferencia a pagar
4. Confirmar solicitud → queda pendiente de match
5. Match encontrado → Notificación push → Match v6 (bottom sheet)
   - Muestra: Recibes 🎸 Fender / Ofreces 🚲 Trek / Diferencia +160€
   - Timer 48h para decidir
   - ✅ Aceptar → artículo bloqueado (badge "Cambio" en perfil)
   - ❌ Cancelar → vuelve al catálogo
6. Al aceptar → Seguimiento v7 con timeline de 6 pasos:
   ✅ Match aceptado
   📦 Preparar envío → botón "Descargar etiqueta"
   ✈️ Enviado por ti
   🏭 Recibido por Treqe (verificación)
   🚚 En camino a ti
   🏠 Entregado
7. Intercambio completado → +5 scoring en Perfil v4
```

### Flujo de perfil y configuración

```
Perfil v4:
  1. Scoring grande con barra de progreso
  2. Estadísticas (intercambios, artículos, tiempo)
  3. Mis artículos con badges de estado (Activo / Cambio)
  4. Actividad reciente (feed cronológico)
     → Tap "Añadir artículo" → Subir v3
     → Tap ⚙️ engranaje → Ajustes v8

Ajustes v8:
  - Notificaciones (toggles: match, envío, email)
  - Dirección de envío
  - Métodos de pago
  - Contraseña
  - Términos y condiciones / Privacidad
  - FAQ / Soporte
  - Cerrar sesión → Splash v9
```

### Flujo de publicación

```
Subir v3:
  1. Fotos (grid 4 slots + slot "Principal")
  2. Título
  3. Categoría (principal + subcategoría, 10×8)
  4. Estado (Nuevo / Como nuevo / Bueno / Aceptable)
  5. Precio (campo libre)
  → "Publicar" → Catálogo v1 (artículo visible en grid)
```

---

## 🔑 Reglas de negocio reflejadas en las pantallas

| Regla | Implementación |
|-------|---------------|
| **Sin chat ni perfiles ajenos** | No hay botón de mensaje en v2 detalle. No existe perfil de vendedor/comprador. El usuario nunca ve a otra persona. |
| **Sin reseñas de usuarios** | La única métrica de confianza es el scoring (v1 mini-bar, v4 grande). No hay estrellas ni reviews. |
| **Algoritmo de intercambio invisible** | El usuario nunca ve "círculos", "k=3", ni nombres de otros usuarios. Solo ve "Match encontrado". |
| **Usuario pone su precio** | v3 Subir tiene campo de precio libre. No hay valoración automática ni tasación. |
| **Treqe centraliza la logística** | v7 Seguimiento: el usuario descarga una etiqueta de Treqe, no sabe quién recibe su paquete. Destino: "Recibirá una nueva casa". |
| **Artículo se bloquea al aceptar match** | v6 Match → al aceptar, el artículo aparece con badge "Cambio" en v4 Perfil y desaparece del catálogo. |
| **Registro no forzado** | v5 Onboarding tiene "Saltar". v10 Registro tiene "Saltar". El catálogo se ve completo sin cuenta. El registro solo se pide al solicitar un artículo. |
| **Social login como método principal** | v10: Google y Apple son los botones primarios. Email manual es la alternativa secundaria (botón dashed). |

---

## 📐 Matriz de navegación

| Desde | Acción | Lleva a |
|-------|--------|---------|
| v9 Splash | auto (nuevo usuario) | v5 Onboarding |
| v9 Splash | auto (sesión activa) | v1 Catálogo |
| v5 Onboarding | "Ver catálogo" | v1 Catálogo |
| v5 Onboarding | "Inicia sesión" | v10 Registro |
| v10 Registro | Google/Apple/Email | v1 Catálogo |
| v10 Registro | "Saltar" | v1 Catálogo |
| v1 Catálogo | Tap artículo | v2 Detalle |
| v1 Catálogo | Tap ➕ (bottom nav) | v3 Subir |
| v1 Catálogo | Tap 👤 (bottom nav) | v4 Perfil |
| v2 Detalle | "Solicitar con trueque" | (pendiente match → v6) |
| v3 Subir | Publicar | v1 Catálogo |
| v4 Perfil | Tap ⚙️ engranaje | v8 Ajustes |
| v4 Perfil | Tap "Añadir artículo" | v3 Subir |
| v4 Perfil | Tap artículo propio | v2 Detalle |
| v6 Match | Aceptar | v7 Seguimiento |
| v6 Match | Cancelar | v1 Catálogo |
| v6 Match | Cerrar (tap fuera) | Pantalla anterior |
| v7 Seguimiento | Completado | v4 Perfil (+5 scoring) |
| v8 Ajustes | Cerrar sesión | v9 Splash |

---

## 🎨 Guía de estilo visual (consistente en todas las pantallas)

| Elemento | Valor |
|----------|-------|
| Fondo | `#F8F6F0` (warm white) |
| Acento | `#FF6A35` (naranja) |
| Texto | `#1A1A1A` |
| Texto secundario | `#888888` |
| Bordes | `#E8E4DC` |
| Éxito | `#00B8B8` (teal) |
| Tipografía | Inter (300-900) |
| Cards | `#FFFFFF` con sombra suave |
| Esquinas cards | 14-16px radius |
| Bottom nav | Blur backdrop + border top |
| CTA primario | Fondo naranja + sombra |
| CTA secundario | Borde gris + texto gris |

---

*Documento generado el 24 Abril 2026. 10 pantallas prototipadas, flujo completo definido.*
