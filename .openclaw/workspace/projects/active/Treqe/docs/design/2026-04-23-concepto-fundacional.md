# TREQE — Concepto Fundacional (23 Abril 2026)

> Documento de referencia para el diseño de producto. Filosofía, experiencia de usuario, y principios rectores.
> Validado con Pepe el 23 de Abril de 2026.

---

## 1. Filosofía del Producto

### El Modelo de Negocio (para el equipo, NO para el usuario)

Treqe es un **marketplace circular** donde todo se puede pagar con dinero, con objetos, o con una mezcla de ambos.

- Los usuarios suben objetos → se valoran en € → generan **crédito** en la plataforma
- Cualquier usuario puede elegir **cualquier artículo del catálogo** (como en Amazon/Wallapop)
- Al solicitar un artículo, puede pagar con dinero, con su crédito de objetos, o mezcla
- Un algoritmo de intercambio circular (k=3, invisible para el usuario) resuelve las transacciones
- **Sistema de scoring:** usuarios con más actividad tienen prioridad en artículos populares

### Regla de Oro

> **El usuario NO debe saber nada sobre:**
> - Algoritmo de intercambio circular
> - Círculos de intercambio (k=3)
> - Matching indirecto
> - De quién es el artículo que recibe
> - A dónde va su artículo
> - Colas, posiciones, otros interesados

### Lo que el usuario SÍ sabe:

> *"Treqe es el marketplace donde puedes conseguir lo que quieras. Paga con dinero, con tus artículos, o una mezcla de ambos. Simplemente elige lo que te gusta y pídelo."*

**Scoring:**
> *"Cuantos más intercambios completes, más alto será tu scoring. Los usuarios con scoring alto tienen prioridad para conseguir los artículos más populares."*

---

## 2. Experiencia de Usuario (3 Pantallas, 3 Pasos)

### Flujo Principal

```
📸 SUELTA ARTÍCULOS  →  👀 EXPLORA EL CATÁLOGO  →  ❤️ PIDE LO QUE QUIERAS
```

### Pantalla 1: Catálogo

```
┌──────────────────────────────────┐
│ 🔍 Buscar...                   ☰ │
│                                  │
│  🎸 Fender Stratocaster    580€ │  → [Solicitar]
│  ⌚ G-SHOCK Mudmaster       250€ │  → [Solicitar]
│  🚲 Trek Marlin 7           420€ │  → [Solicitar]
│  📱 iPhone 15 Pro           890€ │  → [Solicitar]
│  🎮 PlayStation 5           480€ │  → [Solicitar]
│  ...                            │
│                                  │
│  [⬆️ Subir artículo]  [⭐ Perfil]│
└──────────────────────────────────┘
```

- El usuario ve el catálogo completo con precios en €
- Puede buscar, filtrar por categorías, ordenar
- Navegación idéntica a Wallapop / Amazon / cualquier marketplace

### Pantalla 2: Detalle del Artículo

```
┌──────────────────────────────────┐
│ ← Catálogo                       │
│                                  │
│        📸 FOTO GRANDE            │
│        (múltiples imágenes)      │
│                                  │
│ 🎸 Fender Stratocaster           │
│ Estado: Bueno · Ubicación: Málaga│
│                                  │
│ Precio: 580€                     │
│                                  │
│ ═══════════════════════════════  │
│                                  │
│ 💳 PAGAR CON TARJETA            │
│ [Pagar 580€]                     │
│                                  │
│ ─── o ───                       │
│                                  │
│ 📦 USA TUS ARTÍCULOS            │
│ Tienes: 🚲 Trek Marlin 7 (420€) │
│         💻 MacBook Air (890€)   │
│                                  │
│ Total a pagar: 160€             │
│ [Solicitar con tu artículo]     │
│                                  │
│ ⭐ Tu scoring: 82/100            │
└──────────────────────────────────┘
```

**Casos:**
- **Sin artículos subidos:** Solo ve "Pagar con tarjeta"
- **Con artículos subidos:** Ve ambas opciones
- **Artículo más barato que el suyo:** "Recibirás 170€ de diferencia"
- **Múltiples artículos:** Puede elegir cuál usar o combinarlos

### Pantalla 3: Confirmación

```
┌──────────────────────────────────┐
│                                  │
│        ✅ ¡TODO LISTO!           │
│                                  │
│   🎸 Fender Stratocaster         │
│                                  │
│   Pagas: 160€                    │
│   Usas: 🚲 Trek Marlin 7         │
│                                  │
│   Recibirás tu artículo en       │
│   3-5 días laborables.           │
│                                  │
│   ⭐ Scoring: +5 (ahora 87)      │
│                                  │
│   ┌────────────────────────┐    │
│   │   SEGUIR EXPLORANDO    │    │
│   └────────────────────────┘    │
└──────────────────────────────────┘
```

**Lo que NO aparece NUNCA:**
- ❌ Nombre del vendedor/anterior dueño
- ❌ A dónde va el artículo del usuario
- ❌ Círculo de intercambio o algoritmo
- ❌ Cola de espera o posición
- ❌ Otros interesados
- ❌ Términos como "circular", "intercambio", "trueque directo"

Todo se gestiona detrás. El usuario solo sabe que da X y recibe Y.

---

## 3. Sistema de Scoring

### Propósito
Recompensar la actividad y garantizar que usuarios comprometidos tengan mejor acceso a artículos.

### Reglas (internas, no visibles)
- +5 por cada intercambio completado
- +1 por cada artículo subido (hasta 20/mes)
- -2 por solicitud cancelada después de aceptada
- -10 por incidencia no resuelta (objeto no enviado, dañado, etc.)
- Scoring máximo: 100

### Lo que ve el usuario
Una barra de progreso con el número, y un mensaje tipo:
> *"Tu scoring es 82. A más scoring, más probabilidad de conseguir los artículos más populares."*

---

## 4. El "Momento WOW"

Solo una animación en toda la app:

> Cuando el usuario completa una solicitud y el sistema procesa el intercambio:

**Animación:** Una línea curva elegante conecta dos puntos en pantalla y se cierra suavemente formando un círculo (3 segundos, sutil).

**Texto:** *"Todo encaja. Recibirás tu artículo pronto."*

**Sin explicar que es un círculo de intercambio.** Es una metáfora visual bonita que no necesita explicación.

---

## 5. Mensajes Clave (UX Writing)

### Microcopy estándar

| Contexto | Texto |
|----------|-------|
| **Home vacía** | "Sube tu primer artículo y empieza a explorar" |
| **Sin artículos subidos en detalle** | "¿Tienes algo que aportar? Súbelo y quizás puedas conseguir este artículo sin pagar el precio completo." |
| **Scoring alto** | "Tienes prioridad. ¡Sigue así!" |
| **Scoring bajo** | "Completa intercambios para subir tu scoring y tener más prioridad." |
| **Solicitud enviada** | "¡Hecho! Nos encargamos de que todo encaje. Te avisaremos cuando esté listo." |
| **Artículo recibido** | "¡Tu artículo ha llegado! Esperamos que disfrutes de tu nueva adquisición." |

### Tono
- Cálido pero no empalagoso
- Directo, sin rodeos
- Confiable (como un buen recepcionista de hotel)
- Sin jerga técnica

---

## 6. Principios de Diseño

1. **Ultra minimalista** — Menos es más. Cada elemento en pantalla tiene una razón de existir.
2. **Fotos protagonistas** — El objeto es la estrella. Fondo blanco o negro para que resalte.
3. **Sin ruido** — No hay contadores, ni notificaciones no esenciales, ni badges.
4. **Mobile-first** — Diseñado para pulgares, no para ratón.
5. **Accesible** — Contraste suficiente, tipografía legible, tap targets de al menos 48px.
6. **Confianza visual** — La app debe transmitir seguridad (datos protegidos, transacciones seguras).

---

## 7. Estrategia de Crecimiento (Resumen)

1. **Landing page** (hecha) → Explica el concepto simple
2. **Web app** (en desarrollo) → MVP funcional
3. **Mobile app** (futuro) → Experiencia nativa
4. **Bucle viral:** Cada intercambio completado → el usuario cuenta la historia → nuevos usuarios
5. **Scoring como retention:** Los usuarios con scoring alto no quieren perderlo

---

## 8. Decisiones Clave (Registro)

| Fecha | Decisión | Razón |
|------|----------|-------|
| 23 Abr 2026 | El usuario elige CUALQUIER artículo, no solo los que puede "pagar" con sus objetos | Simplicidad máxima, UX universal |
| 23 Abr 2026 | El algoritmo circular es COMPLETAMENTE invisible | El usuario no necesita saberlo, confianza |
| 23 Abr 2026 | Se muestra el scoring como barra + número | Transparencia sin complejidad |
| 23 Abr 2026 | El dueño anterior del artículo NO se muestra | Evita sesgos, fricción, y preguntas incómodas |
| 23 Abr 2026 | Sólo un "Momento WOW" (animación de círculo al completar) | Una sorpresa bien ejecutada > muchas mediocres |

---

*Documento fundacional. Cualquier cambio en estas decisiones debe ser discutido y validado.*
