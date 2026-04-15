#!/usr/bin/env python3
"""
DEMOSTRACIÓN SIMPLE: Lógica económica correcta de Treqe
Versión sin caracteres Unicode
"""

print("="*70)
print("DEMOSTRACION: LOGICA ECONOMICA CORRECTA DE TREQE")
print("="*70)

# ============================================================================
# EJEMPLO CONCRETO
# ============================================================================

print("\n1. ESCENARIO REAL (3 usuarios):")
print("-"*40)

# Definir usuarios reales
usuarios = [
    {'nombre': 'Ana', 'ofrece': 'iPhone 13', 'valor_ofrece': 600, 'quiere': 'MacBook Air M1', 'valor_quiere': 800},
    {'nombre': 'Carlos', 'ofrece': 'MacBook Air M1', 'valor_ofrece': 800, 'quiere': 'Bicicleta carretera', 'valor_quiere': 400},
    {'nombre': 'Beatriz', 'ofrece': 'Bicicleta carretera', 'valor_ofrece': 400, 'quiere': 'iPhone 13', 'valor_quiere': 600}
]

# Mostrar situación inicial
for usuario in usuarios:
    print(f"{usuario['nombre']}: Ofrece {usuario['ofrece']} (EUR{usuario['valor_ofrece']}), Quiere {usuario['quiere']} (EUR{usuario['valor_quiere']})")

# ============================================================================
# SIN TREQE (MERCADO ACTUAL)
# ============================================================================

print("\n\n2. SIN TREQE (mercado actual):")
print("-"*40)
print("PROBLEMA: No hay coincidencias directas k=2")
print("* Ana <-> Carlos: NO (Ana quiere MacBook, Carlos quiere Bicicleta)")
print("* Carlos <-> Beatriz: NO (Carlos quiere Bicicleta, Beatriz quiere iPhone)")
print("* Beatriz <-> Ana: NO (Beatriz quiere iPhone, Ana quiere MacBook)")
print("\nRESULTADO: 0 intercambios posibles (0% cobertura)")

# ============================================================================
# CON TREQE (CICLO K=3)
# ============================================================================

print("\n\n3. CON TREQE (ciclo k=3):")
print("-"*40)
print("CICLO ENCONTRADO: Ana -> Carlos -> Beatriz -> Ana")
print("\nINTERCAMBIO:")
print("1. Ana da iPhone a Beatriz")
print("2. Carlos da MacBook a Ana")
print("3. Beatriz da Bicicleta a Carlos")

# ============================================================================
# CÁLCULO COMPENSACIONES (LÓGICA CORRECTA)
# ============================================================================

print("\n\n4. CALCULO DE COMPENSACIONES (regla CORRECTA):")
print("-"*40)
print("REGLA: Quien recibe item de MAYOR valor PAGA la diferencia")

# Calcular diferencias
print("\nDIFERENCIAS DE VALOR:")
for i in range(3):
    usuario = usuarios[i]
    siguiente = usuarios[(i + 1) % 3]
    
    valor_da = usuario['valor_ofrece']
    valor_recibe = siguiente['valor_ofrece']
    diferencia = valor_recibe - valor_da
    
    if diferencia > 0:
        print(f"* {usuario['nombre']}: Recibe {siguiente['ofrece']} (EUR{valor_recibe}) que vale EUR{diferencia} MAS que su {usuario['ofrece']} (EUR{valor_da}) -> PAGA EUR{diferencia}")
    elif diferencia < 0:
        print(f"* {usuario['nombre']}: Da {usuario['ofrece']} (EUR{valor_da}) que vale EUR{abs(diferencia)} MAS que lo que recibe {siguiente['ofrece']} (EUR{valor_recibe}) -> RECIBE EUR{abs(diferencia)}")

# ============================================================================
# COMISIONES TREQE
# ============================================================================

print("\n\n5. COMISIONES TREQE (6% promedio):")
print("-"*40)

comision_tasa = 0.06
flujo_dinero = []

for i in range(3):
    usuario = usuarios[i]
    siguiente = usuarios[(i + 1) % 3]
    
    valor_da = usuario['valor_ofrece']
    valor_recibe = siguiente['valor_ofrece']
    diferencia = valor_recibe - valor_da
    
    if diferencia > 0:
        comision = diferencia * comision_tasa
        pago_total = diferencia + comision
        flujo_dinero.append(f"{usuario['nombre']} -> Treqe: EUR{pago_total:.2f} (EUR{diferencia} diferencia + EUR{comision:.2f} comision)")
    elif diferencia < 0:
        comision = abs(diferencia) * comision_tasa
        recibe_total = abs(diferencia) - comision
        flujo_dinero.append(f"Treqe -> {usuario['nombre']}: EUR{recibe_total:.2f} (EUR{abs(diferencia)} diferencia - EUR{comision:.2f} comision)")

print("FLUJO DE DINERO:")
for flujo in flujo_dinero:
    print(f"* {flujo}")

# ============================================================================
# RESULTADO FINAL PARA CADA USUARIO
# ============================================================================

print("\n\n6. RESULTADO FINAL PARA CADA USUARIO:")
print("-"*40)

for i in range(3):
    usuario = usuarios[i]
    siguiente = usuarios[(i + 1) % 3]
    
    valor_da = usuario['valor_ofrece']
    valor_recibe = siguiente['valor_ofrece']
    diferencia = valor_recibe - valor_da
    
    print(f"\n{usuario['nombre'].upper()}:")
    print(f"  Da: {usuario['ofrece']} (EUR{valor_da})")
    print(f"  Recibe: {siguiente['ofrece']} (EUR{valor_recibe})")
    
    if diferencia > 0:
        comision = diferencia * comision_tasa
        pago_total = diferencia + comision
        print(f"  Paga: EUR{pago_total:.2f} (EUR{diferencia} diferencia + EUR{comision:.2f} comision)")
        print(f"  NETO ECONOMICO: EUR{valor_da} (EMPATE vs vender+comprar)")
        print(f"  GANA: CONVENIENCIA (todo gestionado, sin buscar)")
    elif diferencia < 0:
        comision = abs(diferencia) * comision_tasa
        recibe_total = abs(diferencia) - comision
        print(f"  Recibe dinero: EUR{recibe_total:.2f} (EUR{abs(diferencia)} diferencia - EUR{comision:.2f} comision)")
        print(f"  NETO ECONOMICO: EUR{valor_da} (EMPATE vs vender+comprar)")
        print(f"  GANA: CONVENIENCIA (todo en un intercambio)")

# ============================================================================
# COMPARATIVA: CON vs SIN TREQE
# ============================================================================

print("\n\n7. COMPARATIVA: CON vs SIN TREQE")
print("-"*40)

print("SIN TREQE (mercado actual):")
print("* Ana: iPhone -> NO consigue MacBook")
print("* Carlos: MacBook -> NO consigue Bicicleta")
print("* Beatriz: Bicicleta -> NO consigue iPhone")
print("* RESULTADO: 0% exito, valor atrapado: EUR1,800")

print("\nCON TREQE:")
print("* Ana: iPhone -> MacBook + paga EUR212 (EUR200 diferencia + EUR12 comision)")
print("* Carlos: MacBook -> Bicicleta + recibe EUR376 (EUR400 diferencia - EUR24 comision)")
print("* Beatriz: Bicicleta -> iPhone + paga EUR188 (EUR200 diferencia + EUR12 comision)")
print("* RESULTADO: 100% exito, valor intercambiado: EUR1,800")
print("* Comisiones Treqe: EUR48 total")

# ============================================================================
# PROPUESTA EN LA APP (EJEMPLO PARA ANA)
# ============================================================================

print("\n\n8. COMO SE VERIA EN LA APP (ejemplo para Ana):")
print("-"*40)

print("""
[NOTIFICACION PUSH]
¡Intercambio encontrado para ti, Ana!

[PANTALLA PRINCIPAL]
========================================
INTERCAMBIO ENCONTRADO: Obtienes MacBook Air M1
========================================

Cambias: iPhone 13 (valorado en EUR600)
Recibes: MacBook Air M1 (valorado en EUR800)

EUR AJUSTE FINANCIERO:
Pagas EUR212.00 total
* EUR200.00 diferencia de valor
* EUR12.00 comision Treqe (6%)

BENEFICIOS PARA TI:
* Obtienes EXACTAMENTE el MacBook que querias
* Sin buscar vendedor ni gestionar envios por separado
* Garantia Treqe 30 dias
* Mismo costo que vender iPhone + comprar MacBook, pero mas simple

OTROS PARTICIPANTES:
* Usuario intercambia MacBook por Bicicleta
* Usuario intercambia Bicicleta por iPhone

RESULTADO NETO:
Das EUR600 valor, recibes EUR800 valor, pagas EUR212 = NETO: EUR600
(EMPATE economico vs vender+comprar, GANAS conveniencia)

[ ACEPTAR POR CONVENIENCIA ]   [ VER DETALLES ]   [ RECHAZAR ]
""")

# ============================================================================
# CONCLUSIÓN
# ============================================================================

print("\n\n9. CONCLUSION:")
print("-"*40)

print("""
LOGICA ECONOMICA CORRECTA IMPLEMENTADA:

1. REGLA FUNDAMENTAL:
   * Quien recibe item de MAYOR valor -> PAGA la diferencia
   * Quien da item de MAYOR valor -> RECIBE la diferencia
   * Sistema cerrado: Total dinero = 0

2. NO HAY MAGIA ECONOMICA:
   * Los usuarios NO ganan dinero extra
   * Logran el MISMO resultado economico que vender+comprar
   * Pero con MUCHA MAS CONVENIENCIA

3. VALOR DE TREQE:
   * Resuelve coincidencia imposible (k=2 -> k=3)
   * Proporciona conveniencia extrema
   * Da confianza (garantias, reputacion)
   * Crea posibilidades donde antes no las habia

4. EN LA APP:
   * Propuestas CLARAS y TRANSPARENTES
   * Usuario ve exactamente que da/recibe/paga/recibe
   * 1 clic para aceptar
   * Todo gestionado por Treqe

TREQE NO CREA VALOR MAGICO
CREA POSIBILIDADES DONDE ANTES NO LAS HABIA
""")

print("\n" + "="*70)
print("FIN DE LA DEMOSTRACION")
print("="*70)