_cycle:
            return [self.cycle_to_match(best_cycle)]
        return []
    
    def initialize_population(self, cycle_size: int) -> List[List[str]]:
        """Inicializa población con ciclos aleatorios"""
        population = []
        user_ids = [u.id for u in self.users]
        
        for _ in range(self.population_size):
            # Seleccionar usuarios aleatorios para ciclo
            if len(user_ids) >= cycle_size:
                cycle = random.sample(user_ids, cycle_size)
                population.append(cycle)
        
        return population
    
    def calculate_fitness(self, cycle: List[str]) -> float:
        """Calcula fitness de un ciclo"""
        if len(cycle) < 2:
            return 0.0
        
        # Verificar si es ciclo válido
        total_value = 0.0
        valid_connections = 0
        
        for i in range(len(cycle)):
            from_user = self.user_dict[cycle[i]]
            to_user = self.user_dict[cycle[(i + 1) % len(cycle)]]
            
            # Buscar item que from_user ofrezca y to_user desee
            connection_found = False
            for item in from_user.offered_items:
                if any(item.id == desired.id for desired in to_user.desired_items):
                    total_value += item.value
                    valid_connections += 1
                    connection_found = True
                    break
            
            if not connection_found:
                # Penalizar conexiones faltantes
                return -10.0
        
        # Fitness basado en valor y completitud
        completeness = valid_connections / len(cycle)
        avg_value = total_value / len(cycle) if len(cycle) > 0 else 0
        
        return completeness * avg_value
    
    def selection(self, fitness_scores: List[Tuple[float, List[str]]]) -> List[List[str]]:
        """Selección por ruleta"""
        total_fitness = sum(max(0, f) for f, _ in fitness_scores)
        if total_fitness == 0:
            return [c for _, c in fitness_scores[:self.population_size//2]]
        
        selected = []
        for _ in range(self.population_size // 2):
            pick = random.uniform(0, total_fitness)
            current = 0
            for fitness, cycle in fitness_scores:
                current += max(0, fitness)
                if current >= pick:
                    selected.append(cycle)
                    break
        
        return selected
    
    def crossover(self, selected: List[List[str]], cycle_size: int) -> List[List[str]]:
        """Cruzamiento de ciclos"""
        new_population = []
        
        while len(new_population) < self.population_size:
            if len(selected) < 2:
                break
            
            parent1, parent2 = random.sample(selected, 2)
            
            # Cruzamiento de orden (order crossover)
            child = self.order_crossover(parent1, parent2, cycle_size)
            new_population.append(child)
        
        return new_population
    
    def order_crossover(self, parent1: List[str], parent2: List[str], size: int) -> List[str]:
        """Cruzamiento de orden para ciclos"""
        if len(parent1) != size or len(parent2) != size:
            return random.sample(parent1, min(size, len(parent1)))
        
        # Seleccionar segmento de parent1
        start = random.randint(0, size - 1)
        end = random.randint(start, size - 1)
        
        child = [None] * size
        segment = parent1[start:end+1]
        
        # Copiar segmento a child
        for i in range(start, end+1):
            child[i] = parent1[i]
        
        # Completar con elementos de parent2
        parent2_idx = 0
        for i in range(size):
            if child[i] is None:
                while parent2[parent2_idx] in segment:
                    parent2_idx += 1
                    if parent2_idx >= size:
                        parent2_idx = 0
                child[i] = parent2[parent2_idx]
                parent2_idx += 1
        
        return child
    
    def mutation(self, population: List[List[str]]) -> List[List[str]]:
        """Mutación de ciclos"""
        mutation_rate = 0.1
        mutated = []
        
        for cycle in population:
            if random.random() < mutation_rate:
                # Intercambiar dos posiciones
                if len(cycle) >= 2:
                    i, j = random.sample(range(len(cycle)), 2)
                    cycle[i], cycle[j] = cycle[j], cycle[i]
            
            mutated.append(cycle)
        
        return mutated
    
    def cycle_to_match(self, cycle: List[str]) -> Dict:
        """Convierte ciclo a estructura de match"""
        exchanges = []
        total_value = 0
        
        for i in range(len(cycle)):
            from_user = self.user_dict[cycle[i]]
            to_user = self.user_dict[cycle[(i + 1) % len(cycle)]]
            
            # Encontrar item para intercambio
            exchange_item = None
            for item in from_user.offered_items:
                if any(item.id == desired.id for desired in to_user.desired_items):
                    exchange_item = item
                    break
            
            if exchange_item:
                exchanges.append({
                    "from": from_user.id,
                    "to": to_user.id,
                    "item": exchange_item.id,
                    "value": exchange_item.value
                })
                total_value += exchange_item.value
        
        return {
            "type": "genetic_circular",
            "participants": cycle,
            "exchanges": exchanges,
            "compensations": {uid: 0.0 for uid in cycle},  # Placeholder
            "total_value": total_value / len(cycle) if cycle else 0,
            "size": len(cycle)
        }

# ========== ALGORITMO DE BÚSQUEDA LOCAL ==========

class LocalSearchOptimizer:
    """Búsqueda local para refinar ciclos"""
    
    def __init__(self, users: List[User]):
        self.users = users
        self.user_dict = {u.id: u for u in users}
    
    def improve_cycle(self, cycle: List[str], max_iterations: int = 100) -> List[str]:
        """Mejora un ciclo usando búsqueda local"""
        if len(cycle) < 3:
            return cycle
        
        best_cycle = cycle.copy()
        best_score = self.cycle_score(best_cycle)
        
        for _ in range(max_iterations):
            # Generar vecino
            neighbor = self.generate_neighbor(best_cycle)
            neighbor_score = self.cycle_score(neighbor)
            
            if neighbor_score > best_score:
                best_cycle = neighbor
                best_score = neighbor_score
        
        return best_cycle
    
    def cycle_score(self, cycle: List[str]) -> float:
        """Puntúa un ciclo"""
        if len(cycle) < 2:
            return 0.0
        
        score = 0.0
        valid_connections = 0
        
        for i in range(len(cycle)):
            from_user = self.user_dict[cycle[i]]
            to_user = self.user_dict[cycle[(i + 1) % len(cycle)]]
            
            # Verificar conexión
            connection_value = 0.0
            for item in from_user.offered_items:
                if any(item.id == desired.id for desired in to_user.desired_items):
                    connection_value = item.value
                    valid_connections += 1
                    break
            
            score += connection_value
        
        # Penalizar ciclos incompletos
        completeness = valid_connections / len(cycle)
        return score * completeness
    
    def generate_neighbor(self, cycle: List[str]) -> List[str]:
        """Genera vecino intercambiando dos usuarios"""
        if len(cycle) < 2:
            return cycle.copy()
        
        neighbor = cycle.copy()
        i, j = random.sample(range(len(cycle)), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        
        return neighbor

# ========== FUNCIÓN PRINCIPAL DE OPTIMIZACIÓN ==========

def optimize_treqe_matching(users: List[User], target_k: int = 4, time_limit: float = 10.0):
    """
    Función principal de optimización para ruedas grandes
    Combina múltiples algoritmos para mejor rendimiento
    """
    print(f"\n{'='*80}")
    print(f"OPTIMIZACIÓN COMPLETA - RUEDAS k={target_k}")
    print(f"{'='*80}")
    
    start_time = time.time()
    
    # 1. Algoritmo greedy rápido
    print("\n[FASE 1] GREEDY RÁPIDO")
    greedy_matcher = OptimizedTreqeMatching(users)
    greedy_matches = greedy_matcher.greedy_cycle_finding(max_k=target_k, time_limit=time_limit/3)
    
    # Usuarios no emparejados
    matched_users = set()
    for match in greedy_matches:
        matched_users.update(match["participants"])
    
    remaining_users = [u for u in users if u.id not in matched_users]
    print(f"    Usuarios emparejados: {len(matched_users)}/{len(users)}")
    print(f"    Usuarios restantes: {len(remaining_users)}")
    
    # 2. Algoritmo genético para usuarios restantes
    print("\n[FASE 2] ALGORITMO GENÉTICO")
    genetic_matches = []
    
    if remaining_users and target_k >= 4:
        genetic_optimizer = GeneticCycleOptimizer(remaining_users, population_size=30, generations=50)
        genetic_matches = genetic_optimizer.optimize(cycle_size=target_k)
        
        # Actualizar usuarios emparejados
        for match in genetic_matches:
            matched_users.update(match["participants"])
    
    # 3. Búsqueda local para refinar
    print("\n[FASE 3] BÚSQUEDA LOCAL")
    local_optimizer = LocalSearchOptimizer(users)
    all_matches = greedy_matches + genetic_matches
    
    improved_matches = []
    for match in all_matches:
        if match["size"] >= 3:
            improved_cycle = local_optimizer.improve_cycle(match["participants"])
            if improved_cycle != match["participants"]:
                # Recrear match con ciclo mejorado
                match["participants"] = improved_cycle
                match["type"] = "optimized_circular"
        
        improved_matches.append(match)
    
    # Calcular métricas
    total_matched = len(matched_users)
    match_rate = total_matched / len(users) if users else 0
    
    total_value = sum(m.get("total_value", 0) * m.get("size", 0) for m in improved_matches)
    avg_value_per_user = total_value / total_matched if total_matched > 0 else 0
    
    elapsed = time.time() - start_time
    
    print(f"\n{'='*80}")
    print("RESULTADOS DE OPTIMIZACIÓN")
    print(f"{'='*80}")
    
    print(f"\n📊 MÉTRICAS FINALES:")
    print(f"  • Usuarios totales: {len(users)}")
    print(f"  • Usuarios emparejados: {total_matched} ({match_rate:.1%})")
    print(f"  • Ruedas encontradas: {len(improved_matches)}")
    print(f"  • Valor total intercambiado: €{total_value:.0f}")
    print(f"  • Valor promedio por usuario: €{avg_value_per_user:.0f}")
    print(f"  • Tiempo ejecución: {elapsed:.3f}s")
    print(f"  • Tamaño máximo rueda: {target_k}")
    
    print(f"\n🎯 EFECTIVIDAD POR TAMAÑO:")
    size_counts = defaultdict(int)
    for match in improved_matches:
        size_counts[match.get("size", 0)] += 1
    
    for size in sorted(size_counts.keys()):
        count = size_counts[size]
        print(f"  • k={size}: {count} ruedas")
    
    print(f"\n⚡ ALGORITMOS UTILIZADOS:")
    algo_counts = defaultdict(int)
    for match in improved_matches:
        algo_counts[match.get("type", "unknown")] += 1
    
    for algo in sorted(algo_counts.keys()):
        count = algo_counts[algo]
        print(f"  • {algo}: {count} matches")
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    
    if elapsed > time_limit:
        print(f"  ⚠️  Tiempo excedido ({elapsed:.1f}s > {time_limit}s)")
        print(f"     Considerar reducir target_k o aumentar time_limit")
    
    if match_rate < 0.4:
        print(f"  ⚠️  Tasa de matching baja ({match_rate:.1%} < 40%)")
        print(f"     Considerar algoritmos más agresivos o reducir k")
    
    if target_k >= 5 and elapsed < 2.0:
        print(f"  ✅ Buen rendimiento para k={target_k}")
        print(f"     Se puede considerar k={target_k+1} en siguiente iteración")
    
    print(f"\n  🎯 Para producción:")
    print(f"     • Usar greedy para k=2-3 (rápido y exacto)")
    print(f"     • Usar genético para k=4-5 (calidad vs tiempo)")
    print(f"     • Limitar k=6 a casos especiales")
    print(f"     • Cachear resultados para usuarios frecuentes")
    
    return improved_matches

# ========== FUNCIÓN DE DEMOSTRACIÓN ==========

def create_demo_scenario(n_users: int = 50, item_categories: List[str] = None) -> List[User]:
    """Crea escenario de demostración"""
    if item_categories is None:
        item_categories = ["Electronics", "Clothing", "Books", "Home", "Sports"]
    
    items_pool = []
    item_id = 1
    
    # Crear items de ejemplo
    for category in item_categories:
        for _ in range(20):
            value = random.uniform(20, 500)
            items_pool.append(
                Item(f"I{item_id}", f"{category} Item {item_id}", value, category)
            )
            item_id += 1
    
    users = []
    for i in range(n_users):
        # Nivel aleatorio
        level = random.choice(list(UserLevel))
        
        # Reputación basada en nivel
        base_reputation = {
            UserLevel.NOVATO: random.uniform(0, 200),
            UserLevel.MIEMBRO: random.uniform(200, 500),
            UserLevel.CONFIABLE: random.uniform(500, 800),
            UserLevel.ELITE: random.uniform(800, 1000)
        }[level]
        
        # Items ofrecidos (1-3)
        offered = random.sample(items_pool, random.randint(1, 3))
        
        # Items deseados (1-3, excluyendo los ofrecidos)
        available = [item for item in items_pool if item not in offered]
        desired = random.sample(available, random.randint(1, 3))
        
        user = User(
            id=f"U{i+1}",
            name=f"User{i+1}",
            level=level,
            reputation=base_reputation,
            offered_items=offered,
            desired_items=desired
        )
        users.append(user)
    
    return users

def run_demo():
    """Ejecuta demostración completa"""
    print("="*80)
    print("DEMOSTRACIÓN: ALGORITMO OPTIMIZADO TREQE")
    print("="*80)
    
    # Crear escenario
    print("\n📊 CREANDO ESCENARIO DE PRUEBA...")
    users = create_demo_scenario(n_users=50)
    print(f"  • Usuarios creados: {len(users)}")
    print(f"  • Niveles: {', '.join([f'{l.name}: {sum(1 for u in users if u.level == l)}' for l in UserLevel])}")
    
    # Ejecutar optimización para diferentes k
    results = {}
    
    for k in [3, 4, 5, 6]:
        print(f"\n{'='*60}")
        print(f"OPTIMIZANDO PARA k={k}")
        print(f"{'='*60}")
        
        matches = optimize_treqe_matching(users, target_k=k, time_limit=15.0)
        results[k] = {
            "matches": len(matches),
            "matched_users": sum(len(m["participants"]) for m in matches),
            "total_value": sum(m.get("total_value", 0) * m.get("size", 0) for m in matches)
        }
    
    # Comparativa
    print(f"\n{'='*80}")
    print("COMPARATIVA POR TAMAÑO k")
    print(f"{'='*80}")
    
    print(f"\n  k | Ruedas | Usuarios Match | Valor Total | Valor/User | Eficiencia")
    print(f"  " + "-"*70)
    
    for k in [3, 4, 5, 6]:
        r = results[k]
        matched = r["matched_users"]
        total_users = len(users)
        match_rate = matched / total_users if total_users > 0 else 0
        value_per_user = r["total_value"] / matched if matched > 0 else 0
        
        # Eficiencia estimada (decrece con k)
        efficiency = 1.0 - (k - 3) * 0.15
        efficiency = max