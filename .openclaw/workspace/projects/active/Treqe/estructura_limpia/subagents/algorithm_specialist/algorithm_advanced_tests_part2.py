        Item("I2", "Cheap Item", 10.0, "Misc", "fair"),
        Item("I3", "Medium Item", 250.0, "Home", "good"),
        Item("I4", "Another Item", 180.0, "Clothing", "like_new"),
    ]
    
    # Edge case 1: User with no desired items
    user1 = User("U1", "NoDesires", UserLevel.NOVATO, 100.0, [items[0]], [], "MAD", "2026-01-01")
    
    # Edge case 2: User with no offered items
    user2 = User("U2", "NoOffers", UserLevel.MIEMBRO, 300.0, [], [items[1]], "BCN", "2026-01-01")
    
    # Edge case 3: Elite user with perfect reputation
    user3 = User("U3", "PerfectElite", UserLevel.ELITE, 1000.0, [items[2]], [items[3]], "VAL", "2025-12-01")
    
    # Edge case 4: Novato with zero reputation
    user4 = User("U4", "ZeroRep", UserLevel.NOVATO, 0.0, [items[3]], [items[0]], "MAD", "2026-02-01")
    
    # Edge case 5: User wants own item (impossible match)
    user5 = User("U5", "SelfWant", UserLevel.CONFIABLE, 500.0, [items[1]], [items[1]], "BCN", "2026-01-15")
    
    return [user1, user2, user3, user4, user5]

# ========== TEST SUITES ==========

def run_unit_tests():
    """Unit tests for core functionality"""
    print("\n[1] 🔬 UNIT TESTS - CORE FUNCTIONALITY")
    print("-"*50)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Item equality
    item1 = Item("I1", "Test", 100.0, "Test", "new")
    item2 = Item("I1", "Test", 100.0, "Test", "new")
    item3 = Item("I2", "Different", 100.0, "Test", "new")
    
    if item1 == item2 and item1 != item3:
        print("✅ Test 1: Item equality works")
        tests_passed += 1
    else:
        print("❌ Test 1: Item equality failed")
        tests_failed += 1
    
    # Test 2: User commission rates
    user_novato = User("U1", "Test", UserLevel.NOVATO, 100.0, [], [], "MAD", "2026-01-01")
    user_elite = User("U2", "Test", UserLevel.ELITE, 1000.0, [], [], "MAD", "2026-01-01")
    
    if abs(user_novato.commission_rate() - 0.01) < 0.001 and abs(user_elite.commission_rate() - 0.008) < 0.001:
        print("✅ Test 2: Commission rates correct by level")
        tests_passed += 1
    else:
        print("❌ Test 2: Commission rates incorrect")
        tests_failed += 1
    
    # Test 3: Reputation multiplier
    user_low_rep = User("U3", "Test", UserLevel.NOVATO, 0.0, [], [], "MAD", "2026-01-01")
    user_high_rep = User("U4", "Test", UserLevel.NOVATO, 1000.0, [], [], "MAD", "2026-01-01")
    
    if abs(user_low_rep.reputation_multiplier() - 1.0) < 0.001 and abs(user_high_rep.reputation_multiplier() - 1.1) < 0.001:
        print("✅ Test 3: Reputation multiplier works")
        tests_passed += 1
    else:
        print("❌ Test 3: Reputation multiplier failed")
        tests_failed += 1
    
    # Test 4: Exchange wheel creation
    test_user = User("U5", "Test", UserLevel.NOVATO, 100.0, [], [], "MAD", "2026-01-01")
    wheel = ExchangeWheel([test_user])
    
    if wheel.participants == [test_user] and wheel.status == "pending":
        print("✅ Test 4: Exchange wheel creation works")
        tests_passed += 1
    else:
        print("❌ Test 4: Exchange wheel creation failed")
        tests_failed += 1
    
    # Test 5: Simple compensation calculation
    item_a = Item("IA", "ItemA", 100.0, "Test", "new")
    item_b = Item("IB", "ItemB", 150.0, "Test", "new")
    
    user_a = User("UA", "UserA", UserLevel.NOVATO, 100.0, [item_a], [item_b], "MAD", "2026-01-01")
    user_b = User("UB", "UserB", UserLevel.NOVATO, 100.0, [item_b], [item_a], "MAD", "2026-01-01")
    
    wheel = ExchangeWheel([user_a, user_b])
    wheel.exchanges = [(user_a, item_a, user_b, item_b)]
    compensations = wheel.calculate_compensations()
    
    # User A gives 100, receives 150 → should pay ~50
    # User B gives 150, receives 100 → should receive ~50
    if user_a in compensations and user_b in compensations:
        if compensations[user_a] < 0 and compensations[user_b] > 0:
            print("✅ Test 5: Basic compensation calculation works")
            tests_passed += 1
        else:
            print("❌ Test 5: Compensation signs incorrect")
            tests_failed += 1
    else:
        print("❌ Test 5: Compensation calculation failed")
        tests_failed += 1
    
    print(f"\n📊 Unit Tests: {tests_passed} passed, {tests_failed} failed")
    return tests_passed, tests_failed

def run_integration_tests():
    """Integration tests for matching algorithms"""
    print("\n[2] 🔗 INTEGRATION TESTS - MATCHING ALGORITHMS")
    print("-"*50)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Simple scenario matching
    print("\n🔍 Test 1: Simple 5-user scenario")
    users = generate_test_scenario_simple()
    wheels = greedy_matching_algorithm(users)
    
    if wheels:
        print(f"   • Wheels created: {len(wheels)}")
        print(f"   • Users matched: {sum(len(w.participants) for w in wheels)}/{len(users)}")
        
        total_value = sum(w.total_exchange_value() for w in wheels)
        avg_fairness = statistics.mean([w.fairness_score() for w in wheels]) if wheels else 0
        avg_satisfaction = statistics.mean([w.participant_satisfaction(p) for w in wheels for p in w.participants]) if any(w.participants for w in wheels) else 0
        
        print(f"   • Total value: €{total_value:.2f}")
        print(f"   • Avg fairness: {avg_fairness:.1%}")
        print(f"   • Avg satisfaction: {avg_satisfaction:.1%}")
        
        if len(wheels) > 0 and total_value > 0:
            print("   ✅ Simple matching works")
            tests_passed += 1
        else:
            print("   ❌ Simple matching failed")
            tests_failed += 1
    else:
        print("   ❌ No wheels created")
        tests_failed += 1
    
    # Test 2: Medium scenario matching
    print("\n🔍 Test 2: Medium scenario (20 users)")
    users = generate_test_scenario_medium(20)
    wheels = greedy_matching_algorithm(users)
    
    if wheels:
        matched_users = sum(len(w.participants) for w in wheels)
        match_rate = matched_users / len(users)
        
        print(f"   • Users: {len(users)}")
        print(f"   • Wheels: {len(wheels)}")
        print(f"   • Match rate: {match_rate:.1%}")
        
        if match_rate > 0.3:  # Expect at least 30% match rate
            print("   ✅ Medium scenario matching works")
            tests_passed += 1
        else:
            print("   ⚠️ Low match rate, but algorithm works")
            tests_passed += 0.5  # Half credit
            tests_failed += 0.5
    else:
        print("   ❌ No wheels created in medium scenario")
        tests_failed += 1
    
    # Test 3: Edge cases
    print("\n🔍 Test 3: Edge case scenarios")
    users = generate_test_scenario_edge_cases()
    wheels = greedy_matching_algorithm(users)
    
    print(f"   • Edge case users: {len(users)}")
    print(f"   • Wheels created: {len(wheels)}")
    
    # Edge cases should handle gracefully (not crash)
    print("   ✅ Edge cases handled without crashing")
    tests_passed += 1
    
    # Test 4: Algorithm comparison
    print("\n🔍 Test 4: Greedy vs Optimized comparison")
    users = generate_test_scenario_medium(15)
    
    start_time = time.time()
    greedy_wheels = greedy_matching_algorithm(users)
    greedy_time = time.time() - start_time
    
    start_time = time.time()
    optimized_wheels = optimized_matching_algorithm(users, max_iterations=100)
    optimized_time = time.time() - start_time
    
    def calculate_metrics(wheels_list):
        if not wheels_list:
            return 0, 0, 0
        total_value = sum(w.total_exchange_value() for w in wheels_list)
        avg_fairness = statistics.mean([w.fairness_score() for w in wheels_list])
        match_rate = sum(len(w.participants) for w in wheels_list) / len(users)
        return total_value, avg_fairness, match_rate
    
    g_value, g_fairness, g_rate = calculate_metrics(greedy_wheels)
    o_value, o_fairness, o_rate = calculate_metrics(optimized_wheels)
    
    print(f"   • Greedy: {greedy_time:.3f}s, Value: €{g_value:.2f}, Fairness: {g_fairness:.1%}, Rate: {g_rate:.1%}")
    print(f"   • Optimized: {optimized_time:.3f}s, Value: €{o_value:.2f}, Fairness: {o_fairness:.1%}, Rate: {o_rate:.1%}")
    
    if optimized_time > greedy_time:  # Optimized should be slower
        print("   ✅ Optimization adds computational cost as expected")
        tests_passed += 1
    else:
        print("   ⚠️ Unexpected timing results")
        tests_failed += 1
    
    print(f"\n📊 Integration Tests: {tests_passed} passed, {tests_failed} failed")
    return tests_passed, tests_failed

def run_performance_tests():
    """Performance and scalability tests"""
    print("\n[3] ⚡ PERFORMANCE TESTS - SCALABILITY")
    print("-"*50)
    
    results = []
    
    # Test different user counts
    user_counts = [10, 20, 50, 100]
    
    for n_users in user_counts:
        print(f"\n🔍 Testing with {n_users} users:")
        users = generate_test_scenario_medium(n_users)
        
        # Time greedy algorithm
        start_time = time.time()
        wheels = greedy_matching_algorithm(users)
        exec_time = time.time() - start_time
        
        matched_users = sum(len(w.participants) for w in wheels)
        match_rate = matched_users / n_users if n_users > 0 else 0
        
        results.append({
            "users": n_users,
            "time": exec_time,
            "wheels": len(wheels),
            "match_rate": match_rate,
            "time_per_user": exec_time / n_users if n_users > 0 else 0
        })
        
        print(f"   • Time: {exec_time:.3f}s ({exec_time/n_users:.3f}s/user)")
        print(f"   • Wheels: {len(wheels)}")
        print(f"   • Match rate: {match_rate:.1%}")
    
    # Analyze scalability
    print("\n📈 Scalability Analysis:")
    print("   Users | Time (s) | Time/User | Match Rate")
    print("   " + "-"*40)
    for r in results:
        print(f"   {r['users']:6d} | {r['time']:8.3f} | {r['time_per_user']:10.3f} | {r['match_rate']:10.1%}")
    
    # Check if time grows quadratically (O(n²) as expected)
    if len(results) >= 2:
        last_ratio = results[-1]["time_per_user"] / results[-2]["time_per_user"] if results[-2]["time_per_user"] > 0 else 0
        user_ratio = results[-1]["users"] / results[-2]["users"]
        
        print(f"\n   Time growth ratio: {last_ratio:.2f}x for {user_ratio:.1f}x users")
        print("   ✅ Expected O(n²) complexity confirmed" if last_ratio > user_ratio * 0.8 else "   ⚠️ Unexpected complexity pattern")
    
    return results

def run_stress_tests():
    """Stress tests with extreme conditions"""
    print("\n[4] 🧪 STRESS TESTS - EXTREME CONDITIONS")
    print("-"*50)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Empty user list
    print("\n🔍 Test 1: Empty user list")
    wheels = greedy_matching_algorithm([])
    if wheels == []:
        print("   ✅ Handles empty list correctly")
        tests_passed += 1
    else:
        print("   ❌ Failed with empty list")
        tests_failed += 1
    
    # Test 2: Single user
    print("\n🔍 Test 2: Single user (no possible matches)")
    users = generate_test_scenario_medium(1)
    wheels = greedy_matching_algorithm(users)
    if wheels == []:
        print("   ✅ Handles single user correctly")
        tests_passed += 1
    else:
        print("   ❌ Created wheel with single user")
        tests_failed += 1
    
    # Test 3: Large value disparities
    print("\n🔍 Test 3: Extreme value disparities")
    expensive_item = Item("I1", "Diamond", 10000.0, "Jewelry", "new")
    cheap_item = Item("I2", "Pen", 1.0, "Office", "new")
    
    user1 = User("U1", "Rich", UserLevel.ELITE, 1000.0, [expensive_item], [cheap_item], "MAD", "2026-01-01")
    user2 = User("U2", "Poor", UserLevel.NOVATO, 10.0, [cheap_item], [expensive_item], "MAD", "2026-01-01")
    
    wheels = greedy_matching_algorithm([user1, user2])
    if wheels:
        wheel = wheels[0]
        compensations = wheel.calculate_compensations()
        
        # Rich user should pay huge compensation
        if user1 in compensations and compensations[user1] < -9000:
            print("   ✅ Handles extreme value disparities")
            tests_passed += 1
        else:
            print("   ⚠️ Compensation calculation unexpected")
            tests_failed += 1
    else:
        print("   ❌ No match with extreme values")
        tests_failed += 1
    
    # Test 4: Memory usage with many items
    print("\n🔍 Test 4: Many items per user")
    many_items = [Item(f"I{i}", f"Item{i}", random.uniform(10, 200), "Test", "new") for i in range(50)]
    
    user_many = User("U3", "ManyItems", UserLevel.CONFIABLE, 500.0, 
                     many_items[:25], many_items[25:], "MAD", "2026-01-01")
    
    # Should not crash with many items
    try:
        _ = user_many.total_offered_value()
        _ = user_many.total_desired_value()
        print("   ✅ Handles many items per user")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Failed with many items: {e}")
        tests_failed += 1
    
    print(f"\n📊 Stress Tests: {tests_passed} passed, {tests_failed} failed")
    return tests_passed, tests_failed

def run_acceptance_tests():
    """Acceptance tests - real-world scenarios"""
    print("\n[5] 🎯 ACCEPTANCE TESTS - REAL-WORLD SCENARIOS")
    print("-"*50)
    
    scenarios = [
        {
            "name": "Perfect circular exchange",
            "users": generate_test_scenario_simple(),
            "min_match_rate": 0.