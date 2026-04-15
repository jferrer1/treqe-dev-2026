#!/usr/bin/env python3
"""
ALGORITMO TREQE - VERSIÓN FINAL CORREGIDA
Lógica económica correcta sin problemas de encoding
"""

import time
import random
import json
from typing import List, Dict, Set, Tuple, Optional, Any
from collections import defaultdict
from datetime import datetime

# ============================================================================
# CLASES PRINCIPALES
# ============================================================================

class UsuarioTreqe:
    """Usuario del sistema Treqe"""
    def __init__(self, id_usuario: int, nombre: str, item_ofrece: str, 
                 valor_ofrece: float, items_desea: List[str], 
                 valores_desea: List[float]):
        self.id = id_usuario
        self.nombre = nombre
        self.item_ofrece = item_ofrece
        self.valor_ofrece = valor_ofrece
        self.items_desea = items_desea
        self.valores_desea = valores_desea
        self.reputacion = random.randint(40, 90)  # Reputación inicial
        self.ubicacion = random.choice(["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"])
    
    def __repr__(self):
        return f"Usuario({self.id}: {self.item_ofrece} EUR{self.valor_ofrece} -> {self.items_desea})"

class CicloIntercambio:
    """Ciclo de intercambio con compensaciones económicas correctas"""
    def __init__(self, ids_usuarios: List[int], usuarios: List[UsuarioTreqe]):
        self.ids_usuarios = ids_usuarios
        self.k = len(ids_usuarios)
        self.usuarios = {u.id: u for u in usuarios}
        self.intercambios = []
        self.compensaciones = {}
        self.calcular_intercambios()
    
    def calcular_intercambios(self):
        """Determinar qué recibe cada usuario y calcular compensaciones"""
        # Paso 1: Determinar flujo de items
        for i in range(self.k):
            id_de = self.ids_usuarios[i]
            id_para = self.ids_usuarios[(i + 1) % self.k]
            
            usuario_de = self.usuarios[id_de]
            usuario_para = self.usuarios[id_para]
            
            # Encontrar qué item quiere 'de' de 'para'
            item_recibe = None
            valor_recibe = 0
            
            for item_deseado, valor_deseado in zip(usuario_de.items_desea, usuario_de.valores_desea):
                if item_deseado == usuario_para.item_ofrece:
                    item_recibe = item_deseado
                    valor_recibe = valor_deseado
                    break
            
            if item_recibe:
                self.intercambios.append({
                    'id_usuario': id_de,
                    'nombre': usuario_de.nombre,
                    'da': usuario_de.item_ofrece,
                    'valor_da': usuario_de.valor_ofrece,
                    'recibe': item_recibe,
                    'valor_recibe': valor_recibe,
                    'de_usuario': id_para,
                    'de_nombre': usuario_para.nombre
                })
        
        # Paso 2: Calcular compensaciones (regla CORRECTA)
        for intercambio in self.intercambios:
            id_usuario = intercambio['id_usuario']
            valor_da = intercambio['valor_da']
            valor_recibe = intercambio['valor_recibe']
            
            diferencia = valor_recibe - valor_da  # Positiva si recibe más valor
            
            # Comisión Treqe (4-8% según reputación)
            usuario = self.usuarios[id_usuario]
            tasa_comision = 0.08 if usuario.reputacion < 60 else 0.06 if usuario.reputacion < 80 else 0.04
            
            if diferencia > 0:
                # Recibe item de MAYOR valor -> PAGA diferencia + comisión
                comision = diferencia * tasa_comision
                pago_total = diferencia + comision
                
                self.compensaciones[id_usuario] = {
                    'tipo': 'paga',
                    'monto': pago_total,
                    'diferencia_valor': diferencia,
                    'comision': comision,
                    'tasa_comision': tasa_comision * 100,
                    'razon': f"Recibe {intercambio['recibe']} (EUR{valor_recibe}) que vale EUR{diferencia} mas que su {intercambio['da']} (EUR{valor_da})"
                }
            elif diferencia < 0:
                # Da item de MAYOR valor -> RECIBE diferencia - comisión
                comision = abs(diferencia) * tasa_comision
                recibe_total = abs(diferencia) - comision
                
                self.compensaciones[id_usuario] = {
                    'tipo': 'recibe',
                    'monto': recibe_total,
                    'diferencia_valor': diferencia,
                    'comision': comision,
                    'tasa_comision': tasa_comision * 100,
                    'razon': f"Da {intercambio['da']} (EUR{valor_da}) que vale EUR{abs(diferencia)} mas que lo que recibe {intercambio['recibe']} (EUR{valor_recibe})"
                }
            else:
                # Valores iguales
                self.compensaciones[id_usuario] = {
                    'tipo': 'equitativo',
                    'monto': 0,
                    'diferencia_valor': 0,
                    'comision': 0,
                    'tasa_comision': 0,
                    'razon': f"Intercambio equitativo"
                }
    
    def generar_propuesta_app(self, id_usuario: int) -> Dict[str, Any]:
        """Generar propuesta para mostrar en la app"""
        if id_usuario not in self.usuarios:
            return None
        
        # Encontrar intercambio de este usuario
        intercambio_usuario = None
        for intercambio in self.intercambios:
            if intercambio['id_usuario'] == id_usuario:
                intercambio_usuario = intercambio
                break
        
        if not intercambio_usuario:
            return None
        
        compensacion = self.compensaciones.get(id_usuario, {'tipo': 'equitativo', 'monto': 0})
        
        # Construir propuesta según tipo
        if compensacion['tipo'] == 'paga':
            propuesta = {
                'titulo': f"INTERCAMBIO ENCONTRADO: Obtienes {intercambio_usuario['recibe']}",
                'resumen': f"Cambias {intercambio_usuario['da']} (EUR{intercambio_usuario['valor_da']}) por {intercambio_usuario['recibe']} (EUR{intercambio_usuario['valor_recibe']})",
                'ajuste_financiero': f"Pagas EUR{compensacion['monto']:.2f} total (EUR{compensacion['diferencia_valor']:.2f} diferencia + EUR{compensacion['comision']:.2f} comision Treqe {compensacion['tasa_comision']:.0f}%)",
                'beneficios': [
                    f"Obtienes EXACTAMENTE {intercambio_usuario['recibe']} que querias",
                    f"Sin buscar vendedor ni gestionar envios por separado",
                    f"Garantia Treqe 30 dias",
                    f"Mismo costo que vender {intercambio_usuario['da']} + comprar {intercambio_usuario['recibe']}, pero mas simple"
                ],
                'accion_recomendada': "ACEPTAR POR CONVENIENCIA",
                'resultado_neto': f"Das EUR{intercambio_usuario['valor_da']} valor, recibes EUR{intercambio_usuario['valor_recibe']} valor, pagas EUR{compensacion['monto']:.2f} = NETO: EUR{intercambio_usuario['valor_da']} (EMPATE economico, ganas conveniencia)"
            }
        elif compensacion['tipo'] == 'recibe':
            propuesta = {
                'titulo': f"INTERCAMBIO ENCONTRADO: Cambias {intercambio_usuario['da']} por {intercambio_usuario['recibe']} + EUR{compensacion['monto']:.2f}",
                'resumen': f"Cambias {intercambio_usuario['da']} (EUR{intercambio_usuario['valor_da']}) por {intercambio_usuario['recibe']} (EUR{intercambio_usuario['valor_recibe']})",
                'ajuste_financiero': f"Recibes EUR{compensacion['monto']:.2f} (EUR{abs(compensacion['diferencia_valor']):.2f} diferencia - EUR{compensacion['comision']:.2f} comision Treqe {compensacion['tasa_comision']:.0f}%)",
                'beneficios': [
                    f"Obtienes {intercambio_usuario['recibe']} que querias",
                    f"Recibes EUR{compensacion['monto']:.2f} en efectivo",
                    f"Todo gestionado en un solo intercambio",
                    f"Sin tener que vender {intercambio_usuario['da']} primero"
                ],
                'accion_recomendada': "ACEPTAR Y RECIBIR DINERO",
                'resultado_neto': f"Das EUR{intercambio_usuario['valor_da']} valor, recibes EUR{intercambio_usuario['valor_recibe']} valor + EUR{compensacion['monto']:.2f} = NETO: EUR{intercambio_usuario['valor_da']} (EMPATE economico, ganas conveniencia)"
            }
        else:
            propuesta = {
                'titulo': f"INTERCAMBIO PERFECTO: Cambias {intercambio_usuario['da']} por {intercambio_usuario['recibe']}",
                'resumen': f"Intercambio equitativo: {intercambio_usuario['da']} (EUR{intercambio_usuario['valor_da']}) por {intercambio_usuario['recibe']} (EUR{intercambio_usuario['valor_recibe']})",
                'ajuste_financiero': "Sin ajuste monetario (valores iguales)",
                'beneficios': [
                    f"Obtienes EXACTAMENTE lo que querias",
                    f"Intercambio perfectamente equilibrado",
                    f"Sin pagos adicionales",
                    f"Todo gestionado por Treqe"
                ],
                'accion_recomendada': "ACEPTAR INTERCAMBIO",
                'resultado_neto': f"Das EUR{intercambio_usuario['valor_da']} valor, recibes EUR{intercambio_usuario['valor_recibe']} valor = NETO: EUR{intercambio_usuario['valor_da']} (EMPATE economico, ganas conveniencia)"
            }
        
        # Información sobre otros participantes (anonimizada)
        otros = []
        for intercambio in self.intercambios:
            if intercambio['id_usuario'] != id_usuario:
                otros.append(f"Usuario intercambia {intercambio['da']} por {intercambio['recibe']}")
        
        propuesta['otros_participantes'] = otros
        propuesta['total_participantes'] = self.k
        propuesta['fecha_generacion'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        return propuesta
    
    def verificar_consistencia_economica(self) -> bool:
        """Verificar que el sistema económico sea consistente"""
        total_pagos = 0
        total_recibos = 0
        
        for compensacion in self.compensaciones.values():
            if compensacion['tipo'] == 'paga':
                total_pagos += compensacion['monto']
            elif compensacion['tipo'] == 'recibe':
                total_recibos += compensacion['monto']
        
        # En un sistema cerrado, pagos = recibos + comisiones Treqe
        comisiones_treqe = sum(c['comision'] for c in self.compensaciones.values())
        
        return abs(total_pagos - total_recibos - comisiones_treqe) < 0.01
    
    def __repr__(self):
        return f"Ciclo(k={self.k}, usuarios={self.ids_usuarios})"

# ============================================================================
# ALGORITMO PRINCIPAL
# ============================================================================

class AlgoritmoTreqeFinal:
    """Algoritmo final con lógica económica correcta"""
    
    def __init__(self, limite_tiempo: int = 180, k_maximo: int = 6):
        self.limite_tiempo = limite_tiempo
        self.k_maximo = k_maximo
        self.usuarios = []
        self.resultados = {}
    
    def crear_usuarios_reales(self, n_usuarios: int = 50, densidad: float = 0.05) -> List[UsuarioTreqe]:
        """Crear usuarios realistas con densidad del mercado español"""
        # Catálogo realista de items
        items = [
            "iPhone 15 Pro", "Samsung S24", "MacBook Pro M3", "iPad Air",
            "Canon EOS R5", "Sony A7IV", "Nintendo Switch", "PlayStation 5",
            "Zapatos Nike", "Chaqueta North Face", "Bolso Michael Kors", 
            "Sofa 3 plazas", "Mesa comedor", "Bicicleta carretera", "Cinta correr"
        ]
        
        valores = {
            "iPhone 15 Pro": 900, "Samsung S24": 800, "MacBook Pro M3": 1800,
            "iPad Air": 600, "Canon EOS R5": 2500, "Sony A7IV": 2200,
            "Nintendo Switch": 250, "PlayStation 5": 450,
            "Zapatos Nike": 80, "Chaqueta North Face": 120, 
            "Bolso Michael Kors": 150, "Sofa 3 plazas": 300,
            "Mesa comedor": 200, "Bicicleta carretera": 400,
            "Cinta correr": 350
        }
        
        nombres = ["Ana", "Carlos", "Beatriz", "David", "Elena", "Fernando", 
                  "Gabriela", "Hector", "Isabel", "Javier", "Laura", "Miguel",
                  "Nuria", "Oscar", "Patricia", "Quique", "Rosa", "Sergio",
                  "Teresa", "Ulises", "Victoria", "Walter", "Ximena", "Yolanda",
                  "Zoe"]
        
        usuarios = []
        for id_usuario in range(n_usuarios):
            # Seleccionar nombre
            nombre = random.choice(nombres) + " " + random.choice(["Gomez", "Rodriguez", "Fernandez", "Lopez", "Martinez"])
            
            # Usuario ofrece un item aleatorio
            item_ofrece = random.choice(items)
            valor_ofrece = valores[item_ofrece]
            
            # Determinar qué items desea (1-2 items, densidad 5%)
            items_desea = []
            valores_desea = []
            
            # Intentar 3 veces para conseguir al menos un item deseado
            for _ in range(3):
                if random.random() < densidad:  # 5% probabilidad por item
                    item_deseado = random.choice([i for i in items if i != item_ofrece])
                    items_desea.append(item_deseado)
                    valores_desea.append(valores[item_deseado])
                    break
            
            # Si no tiene items deseados (95% casos), asignar uno genérico
            if not items_desea:
                item_deseado = random.choice([i for i in items if i != item_ofrece])
                items_desea.append(item_deseado)
                valores_desea.append(valores[item_deseado])
            
            usuarios.append(UsuarioTreqe(id_usuario, nombre, item_ofrece, valor_ofrece, items_desea, valores_desea))
        
        return usuarios
    
    def construir_grafo(self, usuarios: List[UsuarioTreqe]) -> Dict[int, Set[int]]:
        """Construir grafo de quién quiere qué de quién"""
        grafo = defaultdict(set)
        item_a_propietarios = defaultdict(set)
        
        # Mapear items a sus dueños
        for usuario in usuarios:
            item_a_propietarios[usuario.item_ofrece].add(usuario.id)
        
        # Construir aristas: usuario A -> usuario B si B tiene lo que A quiere
        for usuario in usuarios:
            for item_deseado in usuario.items_desea:
                if item_deseado in item_a_propietarios:
                    for id_propietario in item_a_propietarios[item_deseado]:
                        if id_propietario != usuario.id:
                            grafo[usuario.id].add(id_propietario)
        
        return grafo
    
    def buscar_ciclos_k(self, grafo: Dict[int, Set[int]], k: int, 
                       excluidos: Set[int], tiempo_inicio: float) -> List[Tuple[int, ...]]:
        """Buscar ciclos de tamaño k usando DFS limit