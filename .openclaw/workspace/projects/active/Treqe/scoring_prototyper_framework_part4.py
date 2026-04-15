actions": 0,
            "total_value_exchanged": 0,
            "shipping_failures": 0,
            "cancellations": 0,
            "complaints_received": 0,
            "avg_shipping_time": profile["avg_shipping_time"]
        }
        
        for month in range(months):
            # Get monthly values (cycling through arrays if needed)
            monthly_tx = profile["monthly_transactions"][month % len(profile["monthly_transactions"])]
            avg_value = profile["avg_transaction_value"][month % len(profile["avg_transaction_value"])]
            
            # Update cumulative data
            cumulative_data["successful_transactions"] += monthly_tx
            cumulative_data["total_value_exchanged"] += monthly_tx * avg_value
            
            # Random events based on probabilities
            if random.random() < profile["shipping_failure_prob"]:
                cumulative_data["shipping_failures"] += 1
            
            if random.random() < profile["cancellation_prob"]:
                cumulative_data["cancellations"] += 1
            
            if random.random() < profile["complaint_prob"]:
                cumulative_data["complaints_received"] += 1
            
            # Improve shipping time over time (learning effect)
            if month > 0 and cumulative_data["avg_shipping_time"] > 24:
                cumulative_data["avg_shipping_time"] *= 0.95  # 5% improvement per month
            
            # Calculate current state
            current_score = self.calculate_score(cumulative_data)
            current_level = self.determine_level(current_score)
            commission_rate = self.levels[current_level]["commission"]
            monthly_value = monthly_tx * avg_value
            monthly_commission = monthly_value * commission_rate
            
            results.append({
                "month": month + 1,
                "score": round(current_score, 2),
                "level": current_level,
                "monthly_transactions": monthly_tx,
                "monthly_value": monthly_value,
                "total_transactions": cumulative_data["successful_transactions"],
                "total_value": round(cumulative_data["total_value_exchanged"], 2),
                "commission_rate": commission_rate,
                "monthly_commission": round(monthly_commission, 2),
                "cumulative_commission": round(monthly_commission * (month + 1), 2),
                "shipping_failures": cumulative_data["shipping_failures"],
                "cancellations": cumulative_data["cancellations"],
                "complaints": cumulative_data["complaints_received"],
                "avg_shipping_time": round(cumulative_data["avg_shipping_time"], 1)
            })
        
        return results
    
    def generate_report(self, simulation_results, profile_name):
        """Generate a comprehensive report from simulation results"""
        final_month = simulation_results[-1]
        
        report = {
            "profile": profile_name,
            "simulation_period": len(simulation_results),
            "final_score": final_month["score"],
            "final_level": final_month["level"],
            "total_transactions": final_month["total_transactions"],
            "total_value": final_month["total_value"],
            "total_commission": final_month["cumulative_commission"],
            "avg_monthly_value": final_month["total_value"] / len(simulation_results),
            "key_metrics": {
                "shipping_failure_rate": final_month["shipping_failures"] / final_month["total_transactions"] if final_month["total_transactions"] > 0 else 0,
                "cancellation_rate": final_month["cancellations"] / final_month["total_transactions"] if final_month["total_transactions"] > 0 else 0,
                "complaint_rate": final_month["complaints"] / final_month["total_transactions"] if final_month["total_transactions"] > 0 else 0,
                "avg_shipping_time": final_month["avg_shipping_time"]
            },
            "level_progression": [],
            "monthly_breakdown": simulation_results,
            "insights": []
        }
        
        # Track level progression
        current_level = None
        for month_data in simulation_results:
            if month_data["level"] != current_level:
                report["level_progression"].append({
                    "month": month_data["month"],
                    "level": month_data["level"],
                    "score": month_data["score"]
                })
                current_level = month_data["level"]
        
        # Generate insights
        report["insights"] = self._generate_insights(report, simulation_results)
        
        return report
    
    def _generate_insights(self, report, simulation_results):
        """Generate insights from simulation data"""
        insights = []
        
        # Insight 1: Time to reach Elite
        elite_month = None
        for month_data in simulation_results:
            if month_data["level"] == "ELITE":
                elite_month = month_data["month"]
                break
        
        if elite_month:
            insights.append({
                "type": "progression",
                "title": f"Tiempo para alcanzar ELITE: {elite_month} meses",
                "description": f"Este perfil alcanzó el nivel máximo en {elite_month} meses de actividad consistente.",
                "recommendation": "Comunicar claramente el camino hacia Elite para mantener engagement."
            })
        else:
            insights.append({
                "type": "progression",
                "title": "No alcanzó ELITE en el período simulado",
                "description": f"Después de {len(simulation_results)} meses, el perfil alcanzó nivel {report['final_level']} con {report['final_score']} puntos.",
                "recommendation": "Considerar ajustar parámetros o ofrecer bonificaciones para acelerar progresión."
            })
        
        # Insight 2: Commission savings
        if report["final_level"] != "NOVATO":
            novato_commission = report["total_value"] * 0.01
            actual_commission = report["total_commission"]
            savings = novato_commission - actual_commission
            savings_percentage = (savings / novato_commission) * 100 if novato_commission > 0 else 0
            
            insights.append({
                "type": "financial",
                "title": f"Ahorro en comisiones: {savings_percentage:.1f}%",
                "description": f"Por alcanzar nivel {report['final_level']}, ahorró {savings:.2f}€ vs comisión Novato.",
                "recommendation": "Destacar ahorro económico como motivador principal para mejorar comportamiento."
            })
        
        # Insight 3: Behavior impact
        failure_rate = report["key_metrics"]["shipping_failure_rate"]
        cancellation_rate = report["key_metrics"]["cancellation_rate"]
        
        if failure_rate < 0.05 and cancellation_rate < 0.03:
            insights.append({
                "type": "behavior",
                "title": "Comportamiento ejemplar",
                "description": f"Bajas tasas de fallos ({failure_rate*100:.1f}%) y desistimientos ({cancellation_rate*100:.1f}%).",
                "recommendation": "Recompensar comportamiento ejemplar con bonificaciones adicionales."
            })
        
        # Insight 4: Value growth
        first_month_value = simulation_results[0]["monthly_value"]
        last_month_value = simulation_results[-1]["monthly_value"]
        growth_rate = ((last_month_value - first_month_value) / first_month_value) * 100 if first_month_value > 0 else 0
        
        insights.append({
            "type": "growth",
            "title": f"Crecimiento de valor: {growth_rate:.1f}%",
            "description": f"Valor mensual creció de {first_month_value:.0f}€ a {last_month_value:.0f}€.",
            "recommendation": "Incentivar transacciones de mayor valor con bonificaciones progresivas."
        })
        
        return insights
    
    def save_report(self, report, filename):
        """Save report to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Report saved to {filename}")
    
    def print_summary(self, report):
        """Print a summary of the report"""
        print("\n" + "="*60)
        print("TREQE SCORING SYSTEM SIMULATION REPORT")
        print("="*60)
        print(f"Perfil: {report['profile'].upper()}")
        print(f"Período: {report['simulation_period']} meses")
        print(f"Puntuación final: {report['final_score']} puntos")
        print(f"Nivel final: {report['final_level']}")
        print(f"Transacciones totales: {report['total_transactions']}")
        print(f"Valor total intercambiado: {report['total_value']:.2f}€")
        print(f"Comisión total pagada: {report['total_commission']:.2f}€")
        print(f"Valor mensual promedio: {report['avg_monthly_value']:.2f}€")
        print("\n📊 Métricas clave:")
        print(f"  • Tasa de fallos de envío: {report['key_metrics']['shipping_failure_rate']*100:.2f}%")
        print(f"  • Tasa de desistimientos: {report['key_metrics']['cancellation_rate']*100:.2f}%")
        print(f"  • Tasa de reclamos: {report['key_metrics']['complaint_rate']*100:.2f}%")
        print(f"  • Tiempo promedio de envío: {report['key_metrics']['avg_shipping_time']:.1f}h")
        
        print("\n📈 Progresión de niveles:")
        for progression in report["level_progression"]:
            print(f"  • Mes {progression['month']}: {progression['level']} ({progression['score']} pts)")
        
        print("\n💡 Insights principales:")
        for i, insight in enumerate(report["insights"][:3], 1):
            print(f"  {i}. {insight['title']}")
            print(f"     {insight['description']}")
        
        print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(description="Simulate Treqe scoring system")
    parser.add_argument("--profile", choices=["novato", "activo", "confiable", "elite"], 
                       default="novato", help="User profile to simulate")
    parser.add_argument("--months", type=int, default=12, help="Number of months to simulate")
    parser.add_argument("--output", type=str, default="simulation_report.json", 
                       help="Output JSON file")
    parser.add_argument("--summary", action="store_true", help="Print summary to console")
    
    args = parser.parse_args()
    
    # Initialize simulator
    simulator = TreqeScoringSimulator()
    
    # Run simulation
    print(f"Simulando perfil '{args.profile}' por {args.months} meses...")
    simulation_results = simulator.simulate_profile(args.profile, args.months)
    
    # Generate report
    report = simulator.generate_report(simulation_results, args.profile)
    
    # Save report
    simulator.save_report(report, args.output)
    
    # Print summary if requested
    if args.summary:
        simulator.print_summary(report)
    
    print(f"\n✅ Simulación completada. Reporte guardado en '{args.output}'")

if __name__ == "__main__":
    main()
"""
    
    def run_demo(self):
        """Run a demo of the scoring prototyper"""
        print("="*60)
        print("🏆 TREQE SCORING PROTOTYPER DEMO")
        print("="*60)
        
        # Create prototype
        prototype_dir = self.create_interactive_prototype()
        
        # Run sample simulations
        print("\n🧪 Ejecutando simulaciones de ejemplo...")
        
        profiles = ["novato", "activo", "confiable", "elite"]
        for profile in profiles:
            simulation = self.simulate_user_journey(profile, 6)  # 6 months
            final_score = simulation[-1]["score"]
            final_level = simulation[-1]["level"]
            print(f"  • {profile.upper()}: {final_score} pts → {final_level}")
        
        # Generate dashboard data
        print("\n📊 Generando datos para dashboard...")
        dashboard_data = self.generate_dashboard_data()
        
        # Calculate commission savings
        savings = self.calculate_commission_savings()
        print(f"  • Ahorro Elite vs Novato: {savings['percentage']:.1f}% ({savings['yearly']:.0f}€/año)")
        
        # Analyze behavior impact
        impact = self.analyze_behavior_impact()
        print(f"  • Reducción estimada fallos de envío: {impact['metrics_improvement']['fallos_envio']}")
        
        print("\n💡 Insights generados:")
        insights = self.generate_insights(dashboard_data)
        for i, insight in enumerate(insights[:2], 1):
            print(f"  {i}. {insight['title']}")
            print(f"     {insight['description']}")
        
        print("\n" + "="*60)
        print("✅ Prototipo creado exitosamente!")
        print(f"📁 Directorio: {prototype_dir}")
        print("🌐 Abre 'dashboard.html' en tu navegador para ver el prototipo interactivo")
        print("📄 Revisa 'documentation.md' para la documentación completa")
        print("🐍 Ejecuta 'simulate.py' para más simulaciones")
        print("="*60)
        
        return prototype_dir

# Main execution
if __name__ == "__main__":
    # Initialize the scoring prototyper
    prototyper = ScoringPrototyper()
    
    # Run demo
    prototyper.run_demo()