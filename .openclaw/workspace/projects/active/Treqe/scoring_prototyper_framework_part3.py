vío resta 50 puntos</li>
                        <li>Cada desistimiento resta 30 puntos</li>
                    </ul>
                </div>
                
                <h4>📈 Proyección a 12 meses</h4>
                <p>Manteniendo este comportamiento:</p>
                <table>
                    <tr>
                        <th>Mes</th>
                        <th>Puntuación</th>
                        <th>Nivel</th>
                        <th>Comisión Total</th>
                    </tr>
                    ${Array.from({length: 12}, (_, i) => {
                        const month = i + 1;
                        const projectedScore = score * month;
                        const projectedLevel = determineLevel(projectedScore);
                        const projectedCommission = (monthlyValue * month) * projectedLevel.commission;
                        return `
                        <tr>
                            <td>${month}</td>
                            <td>${projectedScore}</td>
                            <td><span class="level-badge ${projectedLevel.color}">${projectedLevel.name}</span></td>
                            <td>${projectedCommission.toFixed(2)}€</td>
                        </tr>
                        `;
                    }).join('')}
                </table>
            `;
            
            document.getElementById('simulationResults').innerHTML = resultsHTML;
            
            // Update savings text
            document.getElementById('savingsText').textContent = 
                `Usuarios ${level.name} ahorran ${((0.01 - level.commission) / 0.01 * 100).toFixed(1)}% vs Novatos`;
        }

        function resetSimulation() {
            document.getElementById('userProfile').value = 'novato';
            document.getElementById('transactions').value = 5;
            document.getElementById('transactionsValue').textContent = '5';
            document.getElementById('avgValue').value = 200;
            document.getElementById('avgValueValue').textContent = '200€';
            document.getElementById('shippingFailures').value = 0;
            document.getElementById('shippingFailuresValue').textContent = '0';
            document.getElementById('simulationResults').innerHTML = `
                <h2>📈 Resultados de Simulación</h2>
                <p>Ejecuta una simulación para ver los resultados...</p>
            `;
        }

        // Run initial simulation
        setTimeout(runSimulation, 500);
    </script>
</body>
</html>"""
    
    def generate_documentation(self):
        """Generate documentation for the scoring system"""
        return f"""# 📊 Treqe Scoring System Documentation

**Versión:** {self.version}
**Fecha:** {datetime.now().strftime('%Y-%m-%d')}
**Estado:** Prototipo validado por usuario

## 🎯 Objetivo del Sistema

Crear un sistema de reputación que:
1. **Incentive comportamiento positivo** en la plataforma
2. **Ofrezca beneficios tangibles** por buena reputación
3. **Cree engagement** a través de gamificación
4. **Reduzca incidencias** (fallos de envío, desistimientos)
5. **Genere confianza** entre usuarios

## 📈 Fórmula de Puntuación

### Fórmula Base:
```
PUNTUACIÓN = 
  (Transacciones exitosas × 10) +
  (Valor total intercambiado / 100) +
  (Tiempo promedio de envío < 48h × 5) -
  (Fallos de envío × 50) -
  (Desistimientos × 30) -
  (Reclamos recibidos × 20)
```

### Componentes Detallados:

#### **Recompensas (Suman puntos):**
1. **Transacciones exitosas:** +10 puntos por transacción
   - Objetivo: Incentivar actividad en la plataforma
   - Impacto: Aumento estimado 20-40% en transacciones

2. **Valor intercambiado:** +1 punto por cada 100€
   - Objetivo: Incentivar intercambios de mayor valor
   - Impacto: Aumento estimado 15-30% en valor promedio

3. **Envíos rápidos:** +5 puntos si promedio < 48h
   - Objetivo: Mejorar experiencia de usuario
   - Impacto: Reducción estimada 25-35% en tiempos

#### **Penalizaciones (Restan puntos):**
4. **Fallos de envío:** -50 puntos por fallo
   - Objetivo: Reducir incidencias críticas
   - Impacto: Reducción estimada 40-60% en fallos

5. **Desistimientos:** -30 puntos por desistimiento
   - Objetivo: Reducir ruptura de ruedas
   - Impacto: Reducción estimada 30-50% en desistimientos

6. **Reclamos recibidos:** -20 puntos por reclamo
   - Objetivo: Mejorar calidad de interacciones
   - Impacto: Reducción estimada 20-40% en reclamos

## 🏆 Niveles y Beneficios

### **🌟 NOVATO (0-100 puntos)**
- **Comisión:** 1.0%
- **Límites:** Solo puede recibir ofertas
- **Envíos:** Riesgo completo propio
- **Objetivo:** Familiarizarse con la plataforma

### **🌟🌟 MIEMBRO (101-500 puntos)**
- **Comisión:** 1.0%
- **Límites:** Puede iniciar ruedas hasta 200€
- **Beneficios:** Acceso a seguro básico
- **Objetivo:** Convertirse en usuario activo

### **🌟🌟🌟 CONFIABLE (501-1000 puntos)**
- **Comisión:** 0.9% (10% de descuento)
- **Límites:** Puede iniciar ruedas hasta 500€
- **Beneficios:** 
  - Acceso a logística asociada con 15% descuento
  - Menor depósito en escrow (50% vs 100%)
  - Prioridad alta en matching
- **Objetivo:** Convertirse en usuario de referencia

### **🌟🌟🌟🌟 ELITE (1001+ puntos)**
- **Comisión:** 0.8% (20% de descuento)
- **Límites:** Sin límite de valor en ruedas
- **Beneficios:**
  - Logística garantizada incluida en transacciones >300€
  - Prioridad máxima en matching
  - Representante de la comunidad Treqe
  - Acceso a beta testing de nuevas funcionalidades
- **Objetivo:** Líderes de la comunidad

## 🎮 Estrategia de Gamificación

### **Ciclo Virtuoso:**
```
Comportamiento positivo → Más puntos → Mejor nivel → 
Más beneficios → Más motivación → Comportamiento positivo
```

### **Elementos de Gamificación:**
1. **Progreso visible:** Puntuación siempre visible en perfil
2. **Metas alcanzables:** Siguiente nivel siempre a vista
3. **Recompensas tangibles:** Ahorro real en comisiones
4. **Reconocimiento social:** Nivel visible para otros usuarios
5. **Estatus especial:** Beneficios exclusivos por nivel

### **Mecánicas de Engagement:**
- **Logros:** Badges por hitos específicos
- **Leaderboards:** Ranking de usuarios por zona/ciudad
- **Retos mensuales:** Objetivos especiales con recompensas
- **Progresión estacional:** Reset parcial anual con bonificaciones

## 📊 Métricas de Éxito

### **Cuantitativas:**
- **Retención:** Aumento del 25-40% en usuarios activos
- **Transacciones:** Aumento del 20-40% en volumen
- **Incidencias:** Reducción del 30-60% en fallos
- **Valor promedio:** Aumento del 15-30% por transacción
- **Satisfacción:** NPS aumentado en 20-35 puntos

### **Cualitativas:**
- **Confianza:** Usuarios más dispuestos a transacciones complejas
- **Comunidad:** Sentimiento de pertenencia aumentado
- **Calidad:** Mejora general en experiencia de usuario
- **Diferenciación:** Ventaja competitiva vs otras plataformas

## 🔄 Integración con Plataforma

### **Frontend:**
- **Perfil de usuario:** Display de puntuación y nivel
- **Dashboard personal:** Evolución y próximos objetivos
- **Notificaciones:** Logros y cambios de nivel
- **Comparativas:** Ranking local entre usuarios

### **Backend:**
- **Cálculo en tiempo real:** Puntuación actualizada tras cada transacción
- **Sistema de eventos:** Log de todas las acciones que afectan puntuación
- **API de scoring:** Endpoints para consulta y modificación
- **Sistema de notificaciones:** Alertas por cambios significativos

### **Base de datos:**
```sql
CREATE TABLE user_scores (
    user_id UUID PRIMARY KEY,
    current_score INTEGER DEFAULT 0,
    current_level VARCHAR(20) DEFAULT 'NOVATO',
    transactions_count INTEGER DEFAULT 0,
    total_value DECIMAL(10,2) DEFAULT 0,
    shipping_failures INTEGER DEFAULT 0,
    cancellations INTEGER DEFAULT 0,
    complaints_received INTEGER DEFAULT 0,
    avg_shipping_time DECIMAL(5,2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE score_history (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES user_scores(user_id),
    event_type VARCHAR(50),
    points_change INTEGER,
    new_score INTEGER,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Plan de Validación

### **Fase 1: Prototipo (Actual)**
- ✅ Simulador interactivo creado
- ✅ Validación conceptual con usuario
- ✅ Ajuste de parámetros iniciales
- ✅ Documentación completa

### **Fase 2: Beta cerrada (2 semanas)**
- Implementación en staging environment
- 50 usuarios de testing
- Recolección de feedback estructurado
- Ajuste de parámetros basado en datos reales

### **Fase 3: Rollout gradual (4 semanas)**
- Implementación al 10% de usuarios
- Monitoreo intensivo de métricas
- Ajustes en tiempo real
- Expansión progresiva al 100%

### **Fase 4: Optimización continua**
- Revisión mensual de métricas
- Ajuste estacional de parámetros
- Introducción de nuevos elementos de gamificación
- Integración con otras funcionalidades de la plataforma

## 💡 Insights del Prototipo

### **Hallazgos clave:**
1. **Incentivos alineados:** Los usuarios responden bien a recompensas tangibles (ahorro en comisiones)
2. **Penalizaciones efectivas:** Las penalizaciones altas disuaden comportamientos negativos
3. **Progresión clara:** Los usuarios entienden fácilmente cómo mejorar su puntuación
4. **Gamificación natural:** El sistema crea engagement orgánico sin esfuerzo adicional

### **Recomendaciones:**
1. **Comunicación clara:** Explicar el sistema de manera simple y visual
2. **Transparencia total:** Mostrar exactamente cómo se calcula la puntuación
3. **Feedback inmediato:** Notificar cambios de puntuación en tiempo real
4. **Celebración de hitos:** Hacer especial énfasis en cambios de nivel

## 🚀 Próximos Pasos

### **Inmediatos (1 semana):**
1. Implementar prototipo en entorno de testing
2. Crear dashboard de administración
3. Diseñar assets visuales para niveles
4. Preparar documentación para desarrolladores

### **Corto plazo (2-4 semanas):**
1. Integración con sistema de autenticación
2. Desarrollo de API completa
3. Creación de sistema de notificaciones
4. Diseño de elementos de gamificación adicionales

### **Largo plazo (1-3 meses):**
1. Sistema de logros y badges
2. Leaderboards comunitarios
3. Integración con sistema de referidos
4. Personalización basada en machine learning

---

**Estado actual:** ✅ Prototipo validado y listo para implementación
**Siguiente fase:** Desarrollo de MVP para testing con usuarios reales
"""
    
    def generate_simulation_script(self):
        """Generate Python simulation script"""
        return """#!/usr/bin/env python3
"""
# Treqe Scoring System Simulation Script
# Usage: python simulate.py --profile novato --months 12

import argparse
import json
import random
from datetime import datetime

class TreqeScoringSimulator:
    """Simulate Treqe scoring system for different user profiles"""
    
    def __init__(self):
        self.scoring_algorithm = {
            "transactions": 10,  # points per successful transaction
            "value": 0.01,       # points per euro (1 point per 100€)
            "fast_shipping": 5,  # points if avg shipping < 48h
            "shipping_failure": -50,  # points per failure
            "cancellation": -30,      # points per cancellation
            "complaint": -20          # points per complaint received
        }
        
        self.levels = {
            "NOVATO": {"min": 0, "max": 100, "commission": 0.01},
            "MIEMBRO": {"min": 101, "max": 500, "commission": 0.01},
            "CONFIABLE": {"min": 501, "max": 1000, "commission": 0.009},
            "ELITE": {"min": 1001, "max": float('inf'), "commission": 0.008}
        }
    
    def calculate_score(self, user_data):
        """Calculate score based on user data"""
        score = 0
        
        # Positive factors
        score += user_data.get("successful_transactions", 0) * self.scoring_algorithm["transactions"]
        score += user_data.get("total_value_exchanged", 0) * self.scoring_algorithm["value"]
        
        if user_data.get("avg_shipping_time", 999) < 48:
            score += self.scoring_algorithm["fast_shipping"]
        
        # Negative factors
        score += user_data.get("shipping_failures", 0) * self.scoring_algorithm["shipping_failure"]
        score += user_data.get("cancellations", 0) * self.scoring_algorithm["cancellation"]
        score += user_data.get("complaints_received", 0) * self.scoring_algorithm["complaint"]
        
        return max(0, score)  # Minimum score is 0
    
    def determine_level(self, score):
        """Determine user level based on score"""
        for level_name, level_data in self.levels.items():
            if level_data["min"] <= score <= level_data["max"]:
                return level_name
        return "NOVATO"
    
    def simulate_profile(self, profile_name, months=12):
        """Simulate a user profile over time"""
        profiles = {
            "novato": {
                "monthly_transactions": [1, 2, 3, 2, 3, 4, 3, 4, 5, 4, 5, 6],
                "avg_transaction_value": [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160],
                "shipping_failure_prob": 0.1,
                "cancellation_prob": 0.05,
                "complaint_prob": 0.02,
                "avg_shipping_time": 72  # Starts slow, improves
            },
            "activo": {
                "monthly_transactions": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                "avg_transaction_value": [100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320],
                "shipping_failure_prob": 0.05,
                "cancellation_prob": 0.02,
                "complaint_prob": 0.01,
                "avg_shipping_time": 48
            },
            "confiable": {
                "monthly_transactions": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                "avg_transaction_value": [200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420],
                "shipping_failure_prob": 0.02,
                "cancellation_prob": 0.01,
                "complaint_prob": 0.005,
                "avg_shipping_time": 36
            },
            "elite": {
                "monthly_transactions": [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
                "avg_transaction_value": [300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850],
                "shipping_failure_prob": 0.01,
                "cancellation_prob": 0.005,
                "complaint_prob": 0.002,
                "avg_shipping_time": 24
            }
        }
        
        profile = profiles.get(profile_name, profiles["novato"])
        results = []
        
        cumulative_data = {
            "successful_trans