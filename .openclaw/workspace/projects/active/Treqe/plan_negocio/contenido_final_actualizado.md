# PLAN DE NEGOCIO TREQE - VERSIÓN FINAL ACTUALIZADA

**Fecha:** 26 de febrero de 2026  
**Versión:** 3.0 - Conclusiones del Desarrollo del Algoritmo  
**Estado:** CONFIDENCIAL

---

## 1. INTRODUCCIÓN: EL CONTEXTO ACTUAL DEL MERCADO

El mercado de segunda mano en España ha experimentado una transformación notable en la última década. Lo que comenzó como una respuesta pragmática a limitaciones económicas se ha convertido en un movimiento cultural y económico de amplio alcance.

**Datos clave (2025-2026):**
- Volumen económico: 8.200 millones de euros
- Usuarios activos: 28 millones de españoles (47% de la población)
- Crecimiento desde 2020: 42%
- Mobile-first: 94% de transacciones desde dispositivos móviles

**El espacio no cubierto:** Ninguna plataforma actual atiende la demanda de trueque estructurado y escalable. Todas se centran exclusivamente en compraventa monetaria.

---

## 2. EL PROBLEMA NO RESUELTO: LA PARADOJA DE LA LIQUIDEZ

Millones de usuarios españoles enfrentan lo que denominamos "paradoja de la liquidez": tener valor atrapado en posesiones que ya no desean, mientras carecen del capital necesario para adquirir lo que realmente necesitan.

**La limitación matemática fundamental:** El trueque tradicional presenta el problema de la "doble coincidencia de deseos". Para que dos personas intercambien directamente, deben querer exactamente lo que la otra tiene.

**Estadísticas reales:**
- Tasa de éxito en intercambios directos: <5%
- Tiempo medio para encontrar coincidencia: 2-3 meses
- Abandono por frustración: 45% después de 1 mes

**Conclusión:** El trueque nunca ha escalado como modelo comercial viable debido a esta limitación matemática, a pesar de la demanda existente.

---

## 3. LA SOLUCIÓN TREQE: CUANDO LAS MATEMÁTICAS ENCUENTRAN PUENTES HUMANOS

Treqe introduce una innovación conceptual significativa: las "ruedas de intercambio inteligente". En lugar de limitarnos a buscar coincidencias directas entre dos personas (una tarea estadísticamente improbable), permitimos que tres, cuatro o incluso cinco usuarios participen en cadenas circulares donde cada uno recibe exactamente lo que desea.

**Lo que hace especial a Treqe:**
- **Supera la limitación histórica:** Rompe el problema de la doble coincidencia de deseos
- **Reconoce la naturaleza humana:** Entiende que nuestras necesidades son complejas
- **Crea posibilidad:** Transforma intercambios imposibles en realizables
- **Valora lo sentimental:** Reconoce que los objetos tienen tanto valor sentimental como económico

---

## 4. EL ALGORITMO: CONCLUSIONES DEL DESARROLLO Y ESTRATEGIA IMPLEMENTADA

Durante el desarrollo del algoritmo de matching de Treqe, aprendimos lecciones cruciales que han dado forma a nuestro enfoque técnico y filosófico.

### 4.1 k>2 no es el problema, es la solución
En mercados reales, la densidad de compatibilidad para intercambios directos (k=2) es inferior al 5%. Esto significa que los trueques 1:1 casi nunca funcionan. Treqe resuelve esto permitiendo círculos de 3, 4 o 5 personas, aumentando exponencialmente las probabilidades de encontrar matches viables.

### 4.2 La estrategia ascendente: k=2 → k_max
Nuestro algoritmo no comienza buscando círculos complejos. Empieza con k=2 (intercambios directos) y solo aumenta el tamaño del círculo si no encuentra matches. Este enfoque incremental garantiza que encontramos la solución más simple posible primero.

### 4.3 Límite de tiempo: 5 minutos por batch
Hemos establecido un timeout de 5 minutos para cada ejecución del algoritmo. Preferimos encontrar matches para el 80% de los usuarios en 5 minutos, que para el 100% en 5 horas. **La perfección es enemiga de lo posible.**

### 4.4 Complejidad como ventaja estratégica
El problema de encontrar ciclos de intercambio óptimos es matemáticamente complejo (NP-Completo para k>3). Esta complejidad no es un accidente - es una barrera de entrada deliberada que protege nuestro modelo de negocio.

### 4.5 Optimizaciones implementadas:
- **Búsqueda heurística:** En lugar de explorar todas las combinaciones (factorial), usamos heurísticas inteligentes
- **Paralelización:** Ejecución en múltiples núcleos de CPU (8 threads en nuestro hardware)
- **Poda temprana:** Descartamos caminos inviables rápidamente
- **Caché de resultados:** Reutilizamos cálculos similares
- **Procesamiento por lotes:** Ejecución cada 10 minutos para eficiencia

### 4.6 Validación con datos realistas:
Nuestras simulaciones iniciales eran demasiado optimistas (12-14% densidad). Con datos de mercado reales (5% densidad), ajustamos el algoritmo para funcionar en condiciones realistas, no ideales.

**Resultado final:** Un algoritmo que encuentra intercambios viables para la mayoría de usuarios en menos de 5 minutos, escalando hasta miles de usuarios simultáneos.

---

## 5. LA EXPERIENCIA DEL USUARIO: SIMPLE POR FUERA, INTELIGENTE POR DENTRO

### Para el usuario, Treqe funciona en tres pasos simples:

#### 1. Cuenta la historia de lo que tienes
No subes un "artículo". Cuentas la historia de ese objeto que ya no encaja en tu vida, pero que todavía tiene valor. Subes fotos que muestran por qué lo apreciabas. Le pones un precio justo, no porque sea una transacción fría, sino porque reconoces lo que vale.

#### 2. Descubre lo que te emociona
Navegas, miras, te dejas sorprender. No buscas solo lo que "necesitas" - descubres lo que te gusta. Marcas ese jersey que tiene exactamente el color que buscabas, esa lámpara que iluminaría perfectamente tu rincón de lectura.

#### 3. Vive tu vida mientras la magia ocurre
Aquí está lo mejor: tú no esperas. El sistema trabaja en silencio, buscando combinaciones inteligentes cada 10 minutos. Mientras tú trabajas, cenas, duermes, Treqe busca caminos donde antes solo había paredes.

#### 4. La notificación que cambia todo
Un día, tu teléfono vibra: **"¡Encontramos un intercambio para ti!"**
No es un algoritmo frío el que te escribe. Es el resultado de conectar tus deseos con los de otras personas reales.

#### 5. Conocerse y confiar
El resto es humano: coordináis envíos, activáis las garantías, os enviáis mensajes. La parte difícil - encontrar a las personas adecuadas - ya está hecha.

---

## 6. SISTEMA DE GARANTÍAS: CONFIANZA CONSTRUIDA CAPA POR CAPA

### En Treqe, la confianza no se da por sentado. Se construye, capa por capa.

#### Capa 1: El dinero está seguro hasta que todos cumplen
Usamos un sistema de depósito en garantía (escrow). Tu dinero y el de los demás están protegidos hasta que todos reciban lo que prometieron. No es "fe" ciega - son mecanismos que protegen a todos.

#### Capa 2: Si algo sale mal, hay red de seguridad
Todos los envíos tienen seguro. Los imprevistos no arruinan la experiencia ni dejan a nadie en desventaja.

#### Capa 3: Cada paso se confirma
Nada de sorpresas de última hora. Cada etapa del proceso se verifica antes de continuar.

#### Capa 4: Todos contribuyen a protegerse mutuamente
Cada transacción añade un pequeño porcentaje a un fondo común. Es un ecosistema donde la responsabilidad es compartida, no individual.

#### Capa 5: Tu reputación es tu activo más valioso
Cada intercambio exitoso construye tu identidad en Treqe. Con el tiempo, tu reputación te da acceso a mejores oportunidades y condiciones.

**Lo que realmente ofrecemos:** No es un "paquete de seguridad". Es la **tranquilidad** de saber que puedes intercambiar con desconocidos como si fueran amigos de confianza.

---

## 7. SISTEMA DE ENVÍOS: PROMESAS QUE SE CUMPLEN

### Los envíos no son solo paquetes que viajan. Son promesas que se cumplen.

#### Cómo funciona:
1. **Acordáis cómo enviar** (cada uno elige lo que le conviene)
2. **Compartís los códigos de seguimiento** (todos pueden ver dónde está cada paquete)
3. **Confirmáis la recepción** (un simple "¡llegó!" activa el siguiente paso)
4. **El sistema libera los pagos** (el dinero cambia de manos solo cuando todos están satisfechos)

#### Las opciones:
- **Envías tú mismo** (si prefieres control personal)
- **Usas nuestro servicio asociado** (con descuentos según tu reputación)
- **Recogida en punto designado** (para ahorrar y conocer a otros usuarios)

#### La triple protección:
1. **Escrow:** El dinero está seguro hasta que todos cumplen
2. **Seguro:** Si algo sale mal en el envío, hay cobertura
3. **Verificación:** Cada paso se confirma antes de continuar

**La magia está en lo simple:** No es un proceso burocrático. Es una conversación entre personas que se están ayudando mutuamente.

---

## 8. SISTEMA DE SCORING: TU REPUTACIÓN ES TU HISTORIA

### En Treqe, tu puntuación no es un número. Es la historia de cómo intercambias.

#### Cómo crece tu reputación:
- **Cada intercambio exitoso** suma a tu historia
- **El valor que mueves** muestra tu seriedad
- **La puntualidad en los envíos** demuestra tu respeto por los demás
- **La claridad en tus descripciones** construye confianza

#### Los niveles no son categorías. Son capítulos de tu historia en Treqe:

##### 📖 Capítulo 1: Empiezas
(Eres nuevo, aprendes cómo funciona)
- Puedes recibir propuestas de intercambio
- Comisión del 1%
- Envías los paquetes por tu cuenta

##### 🌱 Capítulo 2: Creces
(Ya has completado algunos intercambios)
- Puedes iniciar intercambios de hasta 200€
- Acceso al seguro básico
- La comunidad empieza a reconocerte

##### 🤝 Capítulo 3: Eres confiable
(Tu historial habla por ti)
- Intercambios de hasta 500€
- Comisión reducida al 0.9%
- Descuentos en logística
- Menos depósito requerido

##### 🏆 Capítulo 4: Eres parte esencial de la comunidad
(Eres un referente en Treqe)
- Sin límites de valor
- Comisión del 0.8%
- Logística incluida
- Prioridad en búsquedas
- Posibilidad de ayudar a nuevos usuarios

**La filosofía:** No castigamos los errores ocasionales. Reconocemos el aprendizaje. Valoramos la consistencia. Celebramos la contribución a la comunidad.

---

## 9. VENTAJA COMPETITIVA SOSTENIBLE

### 9.1 Primer mover en trueque estructurado
Somos los primeros en resolver el problema de la doble coincidencia de deseos a escala comercial.

### 9.2 Complejidad algorítmica como barrera
Nuestro algoritmo resuelve un problema NP-Completo para k>3. Esta complejidad técnica es una barrera de entrada significativa.

### 9.3 Efecto de red reforzado
Cada usuario adicional no solo aumenta el catálogo, sino que multiplica las posibilidades de intercambio (combinatoria, no lineal).

### 9.4 Integraciones complejas
La combinación de matching algorítmico, pagos en escrow, logística integrada y sistema de reputación crea un ecosistema difícil de replicar.

### 9.5 Confianza acumulada
Cada transacción exitosa construye confianza no solo entre usuarios, sino en la plataforma como institución.

---

## 10. MODELO DE NEGOCIO Y PROYECCIONES

### 10.1 Flujos de ingresos:
- **Comisión por transacción:** 1% (descendente según reputación)
- **Servicios premium:** Seguros mejorados, logística prioritaria
- **Soluciones B2B:** White-label para retailers sostenibles

### 10.2 Proyecciones clave:
- **Año 1:** 25.000 usuarios, 15.000 transacciones, 22.500€ ingresos
- **Año 2:** 75.000 usuarios, 60.000 transacciones, 90.000€ ingresos  
- **Año 3:** 200.000 usuarios, 180.000 transacciones, 270.000€ ingresos

### 10.3 Rentabilidad:
- **EBITDA año 3:** +129.000€ (margen 52.4%)
- **Resultado neto año 3:** +94.125€ (margen 38.3%)
- **ROI inversión inicial:** 162% en 3 años

---

## 11. CONCLUSIÓN: COLABORACIÓN HUMANA-ALGORÍTMICA

### Treqe nació de una conversación.

No de un plan de negocio perfecto. De un diálogo. De correcciones, ajustes, "no, así no funciona", "probemos esto otro".

Esa es la esencia de lo que construimos: **colaboración**. Humanos y algoritmos trabajando juntos para crear algo que ninguno podría crear solo.

### Lo que hemos aprendido:

#### 1. La perfección es enemiga de lo posible
Un algoritmo que promete menos pero cumple más, es mejor que uno que promete todo pero no cumple nada.

#### 2. La complejidad bien gestionada es una ventaja
Si fuera fácil, ya existiría. La dificultad técnica no es un problema - es lo que nos protege.

#### 3. "Suficientemente bueno a tiempo"
Preferimos encontrar intercambios para el 80% de los usuarios en 5 minutos, que para el 100% en 5 horas.

#### 4. k>2 no es el problema, es la solución
En mercados reales, los trueques directos funcionan menos del 5% del tiempo. Conectar a 3, 4, 5 personas no es complicar innecesariamente - es hacer posible lo imposible.

### Treqe no es sobre tecnología. Es sobre personas.
Es sobre esa cámara que llevas años queriendo, y ese iPhone que ya no usas pero que tiene valor para alguien más.
Es sobre descubrir que lo que para ti es ordinario, para otro es especial.
Es sobre la emoción de recibir esa notificación: "alguien quiere lo que tú tienes, y tiene lo que tú quieres".

### En un mundo de transacciones impersonales, Treqe es un recordatorio:
El intercambio, en su esencia, es humano. Y a veces, solo necesitamos un poco de ayuda para encontrar a las personas adecuadas.

---

**Treqe no facilita trueques. Crea conexiones.**  
Y esas conexiones empiezan con cómo hablamos de lo que hacemos.