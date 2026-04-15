        # 2. JSON Data
        dashboard_data = self.generate_dashboard_data()
        with open(os.path.join(prototype_dir, "dashboard_data.json"), "w", encoding="utf-8") as f:
            json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
        
        # 3. Documentation
        doc_content = self.generate_documentation()
        with open(os.path.join(prototype_dir, "documentation.md"), "w", encoding="utf-8") as f:
            f.write(doc_content)
        
        # 4. Simulation script
        sim_content = self.generate_simulation_script()
        with open(os.path.join(prototype_dir, "simulate.py"), "w", encoding="utf-8") as f:
            f.write(sim_content)
        
        print(f"✅ Prototype created in: {prototype_dir}")
        return prototype_dir
    
    def generate_html_dashboard(self):
        """Generate HTML dashboard for interactive prototype"""
        return """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Treqe Scoring System Prototype</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
            color: #333;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 2rem;
        }
        .card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .card h3 {
            margin-top: 0;
            color: #667eea;
        }
        .simulation-controls {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .controls-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 1rem;
        }
        .control-group {
            display: flex;
            flex-direction: column;
        }
        .control-group label {
            margin-bottom: 5px;
            font-weight: 600;
            color: #555;
        }
        .control-group input, .control-group select {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: background 0.3s;
        }
        .btn:hover {
            background: #5a67d8;
        }
        .results {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-top: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .level-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        .novato { background: #e0e0e0; color: #333; }
        .miembro { background: #90caf9; color: #333; }
        .confiable { background: #a5d6a7; color: #333; }
        .elite { background: #ffd54f; color: #333; }
        .insight {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 5px 5px 0;
        }
        .insight h4 {
            margin-top: 0;
            color: #667eea;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #f8f9fa;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏆 Treqe Scoring System Prototype</h1>
        <p>Sistema de reputación y beneficios escalonados para el intercambio inteligente</p>
    </div>

    <div class="simulation-controls">
        <h2>🧪 Simulador Interactivo</h2>
        <p>Ajusta los parámetros y simula el comportamiento de usuarios</p>
        
        <div class="controls-grid">
            <div class="control-group">
                <label for="userProfile">Perfil de Usuario:</label>
                <select id="userProfile">
                    <option value="novato">👶 Novato (0-100 puntos)</option>
                    <option value="activo">👤 Activo (101-500 puntos)</option>
                    <option value="confiable">👍 Confiable (501-1000 puntos)</option>
                    <option value="elite">🏆 Elite (1001+ puntos)</option>
                </select>
            </div>
            
            <div class="control-group">
                <label for="transactions">Transacciones/mes:</label>
                <input type="range" id="transactions" min="1" max="20" value="5">
                <span id="transactionsValue">5</span>
            </div>
            
            <div class="control-group">
                <label for="avgValue">Valor promedio (€):</label>
                <input type="range" id="avgValue" min="50" max="1000" value="200" step="50">
                <span id="avgValueValue">200€</span>
            </div>
            
            <div class="control-group">
                <label for="shippingFailures">Fallos envío/mes:</label>
                <input type="range" id="shippingFailures" min="0" max="5" value="0">
                <span id="shippingFailuresValue">0</span>
            </div>
        </div>
        
        <button class="btn" onclick="runSimulation()">▶️ Ejecutar Simulación</button>
        <button class="btn" onclick="resetSimulation()">🔄 Reiniciar</button>
    </div>

    <div class="dashboard-grid">
        <div class="card">
            <h3>📊 Fórmula de Puntuación</h3>
            <p><strong>PUNTUACIÓN =</strong></p>
            <ul>
                <li>(Transacciones exitosas × 10) +</li>
                <li>(Valor total intercambiado / 100) +</li>
                <li>(Tiempo promedio envío < 48h × 5) -</li>
                <li>(Fallos de envío × 50) -</li>
                <li>(Desistimientos × 30) -</li>
                <li>(Reclamos recibidos × 20)</li>
            </ul>
        </div>
        
        <div class="card">
            <h3>🎯 Niveles y Beneficios</h3>
            <div class="level-badge novato">NOVATO</div>
            <p>0-100 puntos • Comisión: 1.0%</p>
            
            <div class="level-badge miembro">MIEMBRO</div>
            <p>101-500 puntos • Comisión: 1.0%</p>
            
            <div class="level-badge confiable">CONFIABLE</div>
            <p>501-1000 puntos • Comisión: 0.9%</p>
            
            <div class="level-badge elite">ELITE</div>
            <p>1001+ puntos • Comisión: 0.8%</p>
        </div>
        
        <div class="card">
            <h3>💰 Ahorro en Comisiones</h3>
            <canvas id="savingsChart"></canvas>
            <p id="savingsText">Usuarios Elite ahorran 20% vs Novatos</p>
        </div>
    </div>

    <div class="results" id="simulationResults">
        <h2>📈 Resultados de Simulación</h2>
        <p>Ejecuta una simulación para ver los resultados...</p>
    </div>

    <div class="card">
        <h3>💡 Insights y Recomendaciones</h3>
        
        <div class="insight">
            <h4>🎯 Incentivos de Comportamiento</h4>
            <p>El sistema incentiva específicamente:</p>
            <ul>
                <li>✅ Reducir fallos de envío (-50 puntos por fallo)</li>
                <li>✅ Evitar desistimientos (-30 puntos por desistimiento)</li>
                <li>✅ Aumentar transacciones (+10 puntos por transacción)</li>
                <li>✅ Intercambiar artículos de mayor valor (+1 punto por 100€)</li>
                <li>✅ Mantener envíos rápidos (+5 puntos si promedio < 48h)</li>
            </ul>
        </div>
        
        <div class="insight">
            <h4>📊 Impacto Esperado</h4>
            <table>
                <tr>
                    <th>Métrica</th>
                    <th>Mejora Estimada</th>
                </tr>
                <tr>
                    <td>Fallos de envío</td>
                    <td>Reducción 40-60%</td>
                </tr>
                <tr>
                    <td>Desistimientos</td>
                    <td>Reducción 30-50%</td>
                </tr>
                <tr>
                    <td>Transacciones exitosas</td>
                    <td>Aumento 20-40%</td>
                </tr>
                <tr>
                    <td>Valor promedio</td>
                    <td>Aumento 15-30%</td>
                </tr>
                <tr>
                    <td>Tiempo de envío</td>
                    <td>Reducción 25-35%</td>
                </tr>
            </table>
        </div>
        
        <div class="insight">
            <h4>🎮 Gamificación Efectiva</h4>
            <p>El sistema crea un ciclo virtuoso:</p>
            <ol>
                <li>Usuarios ven progreso claro (puntos visibles)</li>
                <li>Beneficios tangibles (ahorro en comisiones)</li>
                <li>Reconocimiento social (niveles visibles)</li>
                <li>Incentivos para mejorar (siguiente nivel alcanzable)</li>
                <li>Comportamiento positivo recompensado</li>
            </ol>
        </div>
    </div>

    <script>
        // Initialize charts
        const savingsCtx = document.getElementById('savingsChart').getContext('2d');
        const savingsChart = new Chart(savingsCtx, {
            type: 'bar',
            data: {
                labels: ['Novato', 'Miembro', 'Confiable', 'Elite'],
                datasets: [{
                    label: 'Comisión (%)',
                    data: [1.0, 1.0, 0.9, 0.8],
                    backgroundColor: [
                        '#e0e0e0',
                        '#90caf9',
                        '#a5d6a7',
                        '#ffd54f'
                    ]
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Comisión (%)'
                        }
                    }
                }
            }
        });

        // Update range values
        document.getElementById('transactions').addEventListener('input', function() {
            document.getElementById('transactionsValue').textContent = this.value;
        });
        
        document.getElementById('avgValue').addEventListener('input', function() {
            document.getElementById('avgValueValue').textContent = this.value + '€';
        });
        
        document.getElementById('shippingFailures').addEventListener('input', function() {
            document.getElementById('shippingFailuresValue').textContent = this.value;
        });

        // Simulation logic
        function calculateScore(data) {
            let score = 0;
            score += data.transactions * 10;
            score += (data.transactions * data.avgValue) / 100;
            score += 5; // Assuming good shipping time
            score -= data.shippingFailures * 50;
            // Default values for other factors
            score -= 0; // No cancellations
            score -= 0; // No complaints
            return Math.max(0, Math.round(score));
        }

        function determineLevel(score) {
            if (score >= 1001) return {name: 'ELITE', color: 'elite', commission: 0.008};
            if (score >= 501) return {name: 'CONFIABLE', color: 'confiable', commission: 0.009};
            if (score >= 101) return {name: 'MIEMBRO', color: 'miembro', commission: 0.01};
            return {name: 'NOVATO', color: 'novato', commission: 0.01};
        }

        function runSimulation() {
            const profile = document.getElementById('userProfile').value;
            const transactions = parseInt(document.getElementById('transactions').value);
            const avgValue = parseInt(document.getElementById('avgValue').value);
            const shippingFailures = parseInt(document.getElementById('shippingFailures').value);
            
            const monthlyData = {
                transactions: transactions,
                avgValue: avgValue,
                shippingFailures: shippingFailures
            };
            
            const score = calculateScore(monthlyData);
            const level = determineLevel(score);
            const monthlyValue = transactions * avgValue;
            const monthlyCommission = monthlyValue * level.commission;
            const yearlyCommission = monthlyCommission * 12;
            const yearlySavings = (monthlyValue * 0.01 * 12) - yearlyCommission;
            
            const resultsHTML = `
                <h3>📊 Resultados Mensuales</h3>
                <table>
                    <tr>
                        <th>Métrica</th>
                        <th>Valor</th>
                    </tr>
                    <tr>
                        <td>Puntuación calculada</td>
                        <td><strong>${score} puntos</strong></td>
                    </tr>
                    <tr>
                        <td>Nivel alcanzado</td>
                        <td><span class="level-badge ${level.color}">${level.name}</span></td>
                    </tr>
                    <tr>
                        <td>Transacciones mensuales</td>
                        <td>${transactions}</td>
                    </tr>
                    <tr>
                        <td>Valor intercambiado/mes</td>
                        <td>${monthlyValue.toLocaleString()}€</td>
                    </tr>
                    <tr>
                        <td>Comisión aplicada</td>
                        <td>${(level.commission * 100).toFixed(1)}%</td>
                    </tr>
                    <tr>
                        <td>Comisión mensual</td>
                        <td>${monthlyCommission.toFixed(2)}€</td>
                    </tr>
                    <tr>
                        <td>Comisión anual</td>
                        <td>${yearlyCommission.toFixed(2)}€</td>
                    </tr>
                    <tr>
                        <td>Ahorro anual vs Novato</td>
                        <td><strong style="color: green;">${yearlySavings.toFixed(2)}€</strong></td>
                    </tr>
                </table>
                
                <div class="insight">
                    <h4>🎯 Recomendaciones para ${level.name}</h4>
                    <p>Para subir de nivel:</p>
                    <ul>
                        ${level.name === 'NOVATO' ? '<li>Aumenta transacciones a 3-4/mes para llegar a MIEMBRO</li>' : ''}
                        ${level.name === 'MIEMBRO' ? '<li>Reduce fallos de envío para acelerar progresión</li>' : ''}
                        ${level.name === 'CONFIABLE' ? '<li>Mantén consistencia para alcanzar ELITE</li>' : ''}
                        ${level.name === 'ELITE' ? '<li>¡Felicidades! Mantén tu estatus Elite</li>' : ''}
                        <li>Cada transacción adicional suma 10 puntos</li>
                        <li>Cada 100€ adicionales suma 1 punto</li>
                        <li>Cada fallo de en