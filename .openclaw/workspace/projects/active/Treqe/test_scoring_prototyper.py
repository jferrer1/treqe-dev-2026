#!/usr/bin/env python3
"""
Simple test of Scoring Prototyper framework
"""

import os
import json
from pathlib import Path

class SimpleScoringPrototyper:
    """Simple version for testing"""
    
    def __init__(self):
        self.scoring_algorithm = {
            "formula": "PUNTUACION = (Transacciones × 10) + (Valor/100) - (Fallos × 50) - (Desistimientos × 30)",
            "levels": {
                "NOVATO": {"min": 0, "max": 100, "commission": 0.01},
                "MIEMBRO": {"min": 101, "max": 500, "commission": 0.01},
                "CONFIABLE": {"min": 501, "max": 1000, "commission": 0.009},
                "ELITE": {"min": 1001, "max": float('inf'), "commission": 0.008}
            }
        }
    
    def calculate_score(self, transactions, value, failures=0, cancellations=0):
        """Calculate simple score"""
        score = (transactions * 10) + (value / 100) - (failures * 50) - (cancellations * 30)
        return max(0, score)
    
    def determine_level(self, score):
        """Determine level from score"""
        for level_name, level_data in self.scoring_algorithm["levels"].items():
            if level_data["min"] <= score <= level_data["max"]:
                return level_name
        return "NOVATO"
    
    def run_demo(self):
        """Run a simple demo"""
        print("="*60)
        print("🏆 TREQE SCORING PROTOTYPER - DEMO SIMPLE")
        print("="*60)
        
        # Test cases
        test_cases = [
            {"name": "Novato básico", "tx": 5, "value": 500, "failures": 1, "cancellations": 0},
            {"name": "Usuario activo", "tx": 12, "value": 2400, "failures": 0, "cancellations": 1},
            {"name": "Usuario confiable", "tx": 20, "value": 6000, "failures": 0, "cancellations": 0},
            {"name": "Usuario elite", "tx": 30, "value": 15000, "failures": 0, "cancellations": 0},
            {"name": "Usuario problemático", "tx": 8, "value": 800, "failures": 3, "cancellations": 2}
        ]
        
        print("\n🧪 Casos de prueba:")
        print("-"*60)
        
        for case in test_cases:
            score = self.calculate_score(
                case["tx"], 
                case["value"], 
                case["failures"], 
                case["cancellations"]
            )
            level = self.determine_level(score)
            commission = self.scoring_algorithm["levels"][level]["commission"]
            monthly_commission = case["value"] * commission
            
            print(f"\n📊 {case['name']}:")
            print(f"  • Transacciones: {case['tx']}")
            print(f"  • Valor: {case['value']}€")
            print(f"  • Fallos: {case['failures']}")
            print(f"  • Desistimientos: {case['cancellations']}")
            print(f"  → Puntuación: {score:.0f} puntos")
            print(f"  → Nivel: {level}")
            print(f"  → Comisión: {commission*100}% ({monthly_commission:.2f}€/mes)")
            
            # Calculate savings vs Novato
            novato_commission = case["value"] * 0.01
            savings = novato_commission - monthly_commission
            if savings > 0:
                print(f"  → Ahorro vs Novato: {savings:.2f}€/mes ({(savings/novato_commission*100):.1f}%)")
        
        print("\n" + "="*60)
        print("💡 Insights del sistema:")
        print("1. Cada fallo de envío (-50 puntos) equivale a 5 transacciones exitosas")
        print("2. Cada desistimiento (-30 puntos) equivale a 3 transacciones exitosas")  
        print("3. Para alcanzar ELITE (1001+ puntos) se necesitan aproximadamente:")
        print("   • 100 transacciones de 100€ cada una")
        print("   • O 50 transacciones de 500€ cada una")
        print("   • O 25 transacciones de 1000€ cada una")
        print("4. Penalizaciones son significativas para disuadir comportamientos negativos")
        
        print("\n" + "="*60)
        print("✅ Demo completado exitosamente!")
        print("El sistema de scoring está listo para implementación.")
        print("="*60)
        
        # Create simple output files
        self.create_output_files(test_cases)
    
    def create_output_files(self, test_cases):
        """Create simple output files"""
        output_dir = "projects/Treqe/scoring_output/"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 1. JSON data
        data = {
            "algorithm": self.scoring_algorithm,
            "test_results": [],
            "insights": [
                "Sistema incentiva transacciones frecuentes y de alto valor",
                "Penalizaciones fuertes para comportamientos negativos",
                "Progresión clara y alcanzable para usuarios activos",
                "Ahorro económico tangible como motivador principal"
            ]
        }
        
        for case in test_cases:
            score = self.calculate_score(
                case["tx"], 
                case["value"], 
                case["failures"], 
                case["cancellations"]
            )
            level = self.determine_level(score)
            
            data["test_results"].append({
                "profile": case["name"],
                "score": score,
                "level": level,
                "transactions": case["tx"],
                "value": case["value"],
                "failures": case["failures"],
                "cancellations": case["cancellations"]
            })
        
        with open(os.path.join(output_dir, "scoring_data.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # 2. Simple HTML
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Treqe Scoring Demo</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .case { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .novato { border-left: 4px solid #ccc; }
        .miembro { border-left: 4px solid #4fc3f7; }
        .confiable { border-left: 4px solid #66bb6a; }
        .elite { border-left: 4px solid #ffb74d; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>🏆 Treqe Scoring System Demo</h1>
    <p>Sistema de reputación validado por usuario</p>
    
    <h2>🧪 Casos de Prueba</h2>
"""
        
        for case in test_cases:
            score = self.calculate_score(
                case["tx"], 
                case["value"], 
                case["failures"], 
                case["cancellations"]
            )
            level = self.determine_level(score)
            level_class = level.lower()
            
            html += f"""
    <div class="case {level_class}">
        <h3>{case['name']} - {level}</h3>
        <p><strong>Puntuación:</strong> {score:.0f} puntos</p>
        <p><strong>Transacciones:</strong> {case['tx']} | <strong>Valor:</strong> {case['value']}€</p>
        <p><strong>Fallos:</strong> {case['failures']} | <strong>Desistimientos:</strong> {case['cancellations']}</p>
    </div>
"""
        
        html += """
    <h2>💡 Insights</h2>
    <ul>
        <li>Cada fallo de envío (-50 pts) = 5 transacciones exitosas</li>
        <li>Cada desistimiento (-30 pts) = 3 transacciones exitosas</li>
        <li>Para Elite: ~100 transacciones de 100€ o 25 de 1000€</li>
        <li>Penalizaciones significativas disuaden comportamientos negativos</li>
    </ul>
    
    <h2>🎯 Objetivos del Sistema</h2>
    <ol>
        <li>Incentivar transacciones frecuentes y de alto valor</li>
        <li>Reducir fallos de envío y desistimientos</li>
        <li>Crear engagement mediante gamificación</li>
        <li>Ofrecer ahorro económico tangible</li>
        <li>Generar confianza entre usuarios</li>
    </ol>
</body>
</html>"""
        
        with open(os.path.join(output_dir, "demo.html"), "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"\n📁 Archivos creados en: {output_dir}")
        print("   • scoring_data.json - Datos completos en JSON")
        print("   • demo.html - Demo interactiva simple")

if __name__ == "__main__":
    prototyper = SimpleScoringPrototyper()
    prototyper.run_demo()