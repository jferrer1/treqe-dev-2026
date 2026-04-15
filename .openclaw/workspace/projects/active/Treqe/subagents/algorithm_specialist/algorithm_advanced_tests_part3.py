        },
        {
            "name": "Mixed user types",
            "users": generate_test_scenario_medium(10),
            "min_match_rate": 0.4,
            "min_fairness": 0.6
        },
        {
            "name": "Location-based (same city)",
            "users": [
                User("U1", "Madrid1", UserLevel.NOVATO, 100.0, 
                     [Item("I1", "Book", 20.0, "Books", "good")],
                     [Item("I2", "Game", 30.0, "Games", "good")],
                     "MAD", "2026-01-01"),
                User("U2", "Madrid2", UserLevel.MIEMBRO, 300.0,
                     [Item("I2", "Game", 30.0, "Games", "good")],
                     [Item("I1", "Book", 20.0, "Books", "good")],
                     "MAD", "2026-01-01"),
                User("U3", "Barcelona", UserLevel.CONFIABLE, 500.0,
                     [Item("I3", "Jacket", 50.0, "Clothing", "like_new")],
                     [Item("I4", "Shoes", 40.0, "Clothing", "good")],
                     "BCN", "2026-01-01"),
            ],
            "min_match_rate": 0.5,
            "min_fairness": 0.7
        }
    ]
    
    tests_passed = 0
    tests_total = len(scenarios)
    
    for scenario in scenarios:
        print(f"\n🔍 Scenario: {scenario['name']}")
        wheels = greedy_matching_algorithm(scenario["users"])
        
        if wheels:
            matched_users = sum(len(w.participants) for w in wheels)
            match_rate = matched_users / len(scenario["users"])
            
            fairness_scores = [w.fairness_score() for w in wheels]
            avg_fairness = statistics.mean(fairness_scores) if fairness_scores else 0
            
            print(f"   • Users: {len(scenario['users'])}")
            print(f"   • Match rate: {match_rate:.1%} (min: {scenario['min_match_rate']:.0%})")
            print(f"   • Avg fairness: {avg_fairness:.1%} (min: {scenario['min_fairness']:.0%})")
            
            if match_rate >= scenario["min_match_rate"] and avg_fairness >= scenario["min_fairness"]:
                print("   ✅ Acceptance criteria met")
                tests_passed += 1
            else:
                print("   ⚠️ Below acceptance criteria")
        else:
            print("   • No wheels created")
            print("   ❌ Failed acceptance test")
    
    print(f"\n📊 Acceptance Tests: {tests_passed}/{tests_total} passed")
    return tests_passed, tests_total

def run_algorithm_improvement_tests():
    """Tests for algorithm improvements and optimizations"""
    print("\n[6] 🚀 ALGORITHM IMPROVEMENT TESTS")
    print("-"*50)
    
    improvements = []
    
    # Test 1: Reputation impact on compensations
    print("\n🔍 Test 1: Reputation impact analysis")
    item1 = Item("I1", "Item", 100.0, "Test", "new")
    item2 = Item("I2", "Item", 150.0, "Test", "new")
    
    # Same exchange, different reputations
    scenarios = [
        ("Both Novato", UserLevel.NOVATO, 100.0, UserLevel.NOVATO, 100.0),
        ("Elite vs Novato", UserLevel.ELITE, 1000.0, UserLevel.NOVATO, 100.0),
        ("High vs Low Rep", UserLevel.CONFIABLE, 800.0, UserLevel.CONFIABLE, 200.0),
    ]
    
    for name, level1, rep1, level2, rep2 in scenarios:
        user1 = User("U1", "User1", level1, rep1, [item1], [item2], "MAD", "2026-01-01")
        user2 = User("U2", "User2", level2, rep2, [item2], [item1], "MAD", "2026-01-01")
        
        wheel = ExchangeWheel([user1, user2])
        wheel.exchanges = [(user1, item1, user2, item2)]
        compensations = wheel.calculate_compensations()
        
        if user1 in compensations and user2 in compensations:
            payment1 = abs(compensations[user1]) if compensations[user1] < 0 else 0
            payment2 = abs(compensations[user2]) if compensations[user2] < 0 else 0
            
            print(f"   • {name}: User1 pays €{payment1:.2f}, User2 pays €{payment2:.2f}")
            
            # Higher reputation should pay less
            if rep1 > rep2 and payment1 < payment2:
                improvements.append(f"Reputation reduces payments (confirmed)")
    
    # Test 2: Commission impact
    print("\n🔍 Test 2: Commission structure analysis")
    item = Item("I1", "Item", 200.0, "Test", "new")
    
    commission_rates = {}
    for level in UserLevel:
        user = User("U1", "Test", level, 500.0, [item], [], "MAD", "2026-01-01")
        commission_rates[level.name] = user.commission_rate()
    
    print("   • Commission rates by level:")
    for level, rate in commission_rates.items():
        print(f"     {level}: {rate*100:.1f}%")
    
    # Test 3: Algorithm efficiency improvements
    print("\n🔍 Test 3: Greedy vs Optimized comparison")
    
    test_sizes = [10, 15, 20]
    results = []
    
    for size in test_sizes:
        users = generate_test_scenario_medium(size)
        
        # Greedy
        start = time.time()
        greedy_wheels = greedy_matching_algorithm(users)
        greedy_time = time.time() - start
        greedy_value = sum(w.total_exchange_value() for w in greedy_wheels)
        
        # Optimized (limited iterations for speed)
        start = time.time()
        optimized_wheels = optimized_matching_algorithm(users, max_iterations=50)
        optimized_time = time.time() - start
        optimized_value = sum(w.total_exchange_value() for w in optimized_wheels)
        
        improvement = ((optimized_value - greedy_value) / greedy_value * 100) if greedy_value > 0 else 0
        
        results.append({
            "size": size,
            "greedy_value": greedy_value,
            "optimized_value": optimized_value,
            "improvement": improvement,
            "time_cost": optimized_time / greedy_time if greedy_time > 0 else 0
        })
    
    print("   • Value improvement from optimization:")
    for r in results:
        print(f"     {r['size']} users: +{r['improvement']:.1f}% value, {r['time_cost']:.1f}x time")
        
        if r["improvement"] > 0:
            improvements.append(f"Optimization adds +{r['improvement']:.1f}% value for {r['size']} users")
    
    # Test 4: Fairness improvements
    print("\n🔍 Test 4: Fairness analysis")
    
    users = generate_test_scenario_medium(12)
    wheels = greedy_matching_algorithm(users)
    
    if wheels:
        fairness_scores = [w.fairness_score() for w in wheels]
        avg_fairness = statistics.mean(fairness_scores)
        min_fairness = min(fairness_scores) if fairness_scores else 0
        
        print(f"   • Avg fairness: {avg_fairness:.1%}")
        print(f"   • Min fairness: {min_fairness:.1%}")
        
        if avg_fairness > 0.7:
            improvements.append(f"Good average fairness: {avg_fairness:.1%}")
        if min_fairness > 0.5:
            improvements.append(f"Acceptable minimum fairness: {min_fairness:.1%}")
    
    print(f"\n📊 Algorithm Improvements Identified: {len(improvements)}")
    for i, imp in enumerate(improvements[:5], 1):  # Show first 5
        print(f"   {i}. {imp}")
    
    return improvements

def generate_test_report():
    """Generate comprehensive test report"""
    print("\n" + "="*70)
    print("📋 COMPREHENSIVE TEST REPORT - TREQE MATCHING ALGORITHM")
    print("="*70)
    
    # Run all test suites
    print("\n🏃‍♂️ RUNNING TEST SUITES...")
    
    # Unit tests
    unit_passed, unit_failed = run_unit_tests()
    
    # Integration tests  
    integration_passed, integration_failed = run_integration_tests()
    
    # Performance tests
    performance_results = run_performance_tests()
    
    # Stress tests
    stress_passed, stress_failed = run_stress_tests()
    
    # Acceptance tests
    acceptance_passed, acceptance_total = run_acceptance_tests()
    
    # Algorithm improvement tests
    improvements = run_algorithm_improvement_tests()
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    total_passed = (unit_passed + integration_passed + stress_passed + acceptance_passed)
    total_tests = (unit_passed + unit_failed + integration_passed + integration_failed + 
                   stress_passed + stress_failed + acceptance_total)
    
    print(f"\n✅ Tests Passed: {total_passed}/{total_tests} ({total_passed/total_tests*100:.1f}%)")
    
    print("\n📈 Performance Metrics:")
    if performance_results:
        last_result = performance_results[-1]
        print(f"   • Max users tested: {last_result['users']}")
        print(f"   • Max time: {last_result['time']:.3f}s")
        print(f"   • Time per user: {last_result['time_per_user']:.3f}s")
        print(f"   • Match rate at scale: {last_result['match_rate']:.1%}")
    
    print("\n🚀 Algorithm Improvements Identified:")
    for i, imp in enumerate(improvements[:3], 1):
        print(f"   {i}. {imp}")
    
    print("\n⚠️ Areas for Improvement:")
    improvement_areas = []
    
    if unit_failed > 0:
        improvement_areas.append("Fix unit test failures")
    
    if integration_failed > 0:
        improvement_areas.append("Improve integration test coverage")
    
    if stress_failed > 0:
        improvement_areas.append("Enhance stress test handling")
    
    if acceptance_passed < acceptance_total:
        improvement_areas.append("Meet acceptance criteria in all scenarios")
    
    if not improvement_areas:
        improvement_areas.append("All areas satisfactory - ready for production")
    
    for i, area in enumerate(improvement_areas, 1):
        print(f"   {i}. {area}")
    
    print("\n🎯 Recommendations:")
    recommendations = [
        "Use greedy algorithm for MVP (proven, fast, reliable)",
        "Implement optimized algorithm for growth phase",
        "Add location-based matching for better logistics",
        "Implement caching for repeated matching calculations",
        "Add real-time matching updates with WebSockets",
        "Create A/B testing framework for algorithm variations"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    print("\n🔧 Technical Implementation Notes:")
    notes = [
        "Algorithm complexity: O(n²) for greedy, acceptable for <1000 users",
        "Memory usage: Linear with users and items",
        "Thread safety: Algorithm is stateless, can be parallelized",
        "Database integration: Needs efficient user/item querying",
        "Real-time requirements: Matching can be batched (hourly/daily)",
        "Monitoring: Track match rates, satisfaction, fairness metrics"
    ]
    
    for i, note in enumerate(notes, 1):
        print(f"   {i}. {note}")
    
    # Final verdict
    print("\n" + "="*70)
    if total_passed / total_tests >= 0.8:
        print("✅ VERDICT: ALGORITHM READY FOR PRODUCTION")
        print("   The matching algorithm meets quality standards for MVP deployment.")
    elif total_passed / total_tests >= 0.6:
        print("⚠️ VERDICT: ALGORITHM NEEDS IMPROVEMENT")
        print("   The algorithm works but requires fixes before production.")
    else:
        print("❌ VERDICT: ALGORITHM NOT READY")
        print("   Significant improvements needed before deployment.")
    
    print("="*70)
    
    # Save report to file
    report_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "test_summary": {
            "unit_tests": {"passed": unit_passed, "failed": unit_failed},
            "integration_tests": {"passed": integration_passed, "failed": integration_failed},
            "stress_tests": {"passed": stress_passed, "failed": stress_failed},
            "acceptance_tests": {"passed": acceptance_passed, "total": acceptance_total},
            "total_passed": total_passed,
            "total_tests": total_tests,
            "success_rate": total_passed / total_tests if total_tests > 0 else 0
        },
        "performance_metrics": performance_results,
        "improvements_identified": improvements,
        "recommendations": recommendations,
        "verdict": "READY" if total_passed / total_tests >= 0.8 else "NEEDS_IMPROVEMENT" if total_passed / total_tests >= 0.6 else "NOT_READY"
    }
    
    report_path = "algorithm_test_report.json"
    with open(report_path, "w") as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📄 Test report saved to: {report_path}")
    
    return report_data

# ========== MAIN EXECUTION ==========

if __name__ == "__main__":
    print("🧪 ADVANCED ALGORITHM TESTING SUITE")
    print("Testing Treqe Matching Algorithm with comprehensive test coverage")
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    try:
        report = generate_test_report()
        
        print("\n🎯 NEXT STEPS:")
        print("1. Review test report for any failures")
        print("2. Implement recommended improvements")
        print("3. Integrate algorithm into Treqe backend")
        print("4. Set up monitoring for production metrics")
        print("5. Plan A/B tests for algorithm variations")
        
        print(f"\n✅ Testing completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
        import traceback
        traceback.print_exc()