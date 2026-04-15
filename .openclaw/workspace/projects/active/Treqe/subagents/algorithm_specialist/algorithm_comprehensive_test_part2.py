payment2:.2f}")
            
            # Higher reputation should pay less
            if rep1 > rep2 and payment1 < payment2:
                insights.append(f"Reputation reduces payments: {name}")
    
    # Analyze commission impact
    print("\n🔍 Commission Structure Analysis:")
    
    commission_by_level = {}
    for level in UserLevel:
        user = User("U1", "Test", level, 500.0, [], [])
        commission_by_level[level.name] = user.commission_rate()
    
    for level, rate in commission_by_level.items():
        print(f"   • {level}: {rate*100:.1f}% commission")
    
    insights.append(f"Commission ranges from {commission_by_level['NOVATO']*100:.1f}% to {commission_by_level['ELITE']*100:.1f}%")
    
    # Analyze matching efficiency
    print("\n🔍 Matching Efficiency Analysis:")
    
    test_sizes = [10, 20, 30]
    for size in test_sizes:
        users = create_random_test_scenario(size)
        wheels = greedy_matching_algorithm(users)
        
        matched_users = sum(len(w["participants"]) for w in wheels)
        efficiency = matched_users / size if size > 0 else 0
        
        total_value = sum(w["total_value"] for w in wheels)
        avg_value = total_value / len(wheels) if wheels else 0
        
        print(f"   • {size} users: {efficiency:.1%} matched, €{avg_value:.0f} avg wheel value")
        
        if efficiency > 0.4:
            insights.append(f"Good efficiency ({efficiency:.1%}) with {size} users")
    
    print(f"\n📊 Algorithm Insights: {len(insights)} key findings")
    for i, insight in enumerate(insights[:5], 1):
        print(f"   {i}. {insight}")
    
    return insights

def generate_comprehensive_report():
    """Generate comprehensive test report"""
    print("\n" + "="*70)
    print("📋 COMPREHENSIVE TEST REPORT")
    print("="*70)
    
    print("\n🏃‍♂️ RUNNING ALL TEST SUITES...")
    
    # Run all test suites
    unit_passed, unit_total = run_unit_tests()
    functional_passed, functional_total = run_functional_tests()
    performance_results = run_performance_tests()
    edge_passed, edge_total = run_edge_case_tests()
    acceptance_passed, acceptance_total = run_acceptance_tests()
    insights = run_algorithm_analysis()
    
    # Calculate totals
    total_passed = unit_passed + functional_passed + edge_passed + acceptance_passed
    total_tests = unit_total + functional_total + edge_total + acceptance_total
    success_rate = total_passed / total_tests if total_tests > 0 else 0
    
    # Summary
    print("\n" + "="*70)
    print("📊 FINAL SUMMARY")
    print("="*70)
    
    print(f"\n✅ Overall Success Rate: {success_rate:.1%} ({total_passed}/{total_tests} tests passed)")
    
    print("\n📈 Test Suite Results:")
    print(f"   • Unit Tests: {unit_passed}/{unit_total} ({unit_passed/unit_total*100:.0f}%)")
    print(f"   • Functional Tests: {functional_passed}/{functional_total} ({functional_passed/functional_total*100:.0f}%)")
    print(f"   • Edge Case Tests: {edge_passed}/{edge_total} ({edge_passed/edge_total*100:.0f}%)")
    print(f"   • Acceptance Tests: {acceptance_passed}/{acceptance_total} ({acceptance_passed/acceptance_total*100:.0f}%)")
    
    print("\n⚡ Performance Metrics:")
    if performance_results:
        last = performance_results[-1]
        print(f"   • Max scale tested: {last['scale']} users")
        print(f"   • Max execution time: {last['time']:.3f}s")
        print(f"   • Time per user: {last['time_per_user']:.3f}s")
        print(f"   • Match rate at scale: {last['match_rate']:.1%}")
    
    print("\n🚀 Key Algorithm Insights:")
    for i, insight in enumerate(insights[:3], 1):
        print(f"   {i}. {insight}")
    
    print("\n⚠️ Areas for Improvement:")
    improvement_areas = []
    
    if unit_passed < unit_total:
        improvement_areas.append("Fix unit test failures")
    
    if functional_passed < functional_total:
        improvement_areas.append("Improve functional test coverage")
    
    if edge_passed < edge_total:
        improvement_areas.append("Enhance edge case handling")
    
    if acceptance_passed < acceptance_total:
        improvement_areas.append("Meet all acceptance criteria")
    
    if not improvement_areas:
        improvement_areas.append("All test areas satisfactory")
    
    for i, area in enumerate(improvement_areas, 1):
        print(f"   {i}. {area}")
    
    print("\n🎯 Recommendations for Production:")
    recommendations = [
        "Algorithm ready for MVP deployment",
        "Monitor real-world match rates and adjust thresholds",
        "Implement caching for performance at scale",
        "Add A/B testing for algorithm variations",
        "Track user satisfaction and fairness metrics"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    # Final verdict
    print("\n" + "="*70)
    if success_rate >= 0.9:
        print("✅ VERDICT: EXCELLENT - READY FOR PRODUCTION")
        print("   Algorithm exceeds quality standards.")
    elif success_rate >= 0.7:
        print("✅ VERDICT: GOOD - READY FOR MVP")
        print("   Algorithm meets MVP requirements.")
    elif success_rate >= 0.5:
        print("⚠️ VERDICT: FAIR - NEEDS IMPROVEMENT")
        print("   Algorithm works but requires fixes.")
    else:
        print("❌ VERDICT: POOR - NOT READY")
        print("   Significant improvements needed.")
    
    print("="*70)
    
    # Save report
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "test_results": {
            "unit_tests": {"passed": unit_passed, "total": unit_total},
            "functional_tests": {"passed": functional_passed, "total": functional_total},
            "edge_case_tests": {"passed": edge_passed, "total": edge_total},
            "acceptance_tests": {"passed": acceptance_passed, "total": acceptance_total},
            "overall": {"passed": total_passed, "total": total_tests, "success_rate": success_rate}
        },
        "performance": performance_results,
        "insights": insights,
        "improvement_areas": improvement_areas,
        "recommendations": recommendations,
        "verdict": "EXCELLENT" if success_rate >= 0.9 else "GOOD" if success_rate >= 0.7 else "FAIR" if success_rate >= 0.5 else "POOR"
    }
    
    report_path = "algorithm_test_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Comprehensive test report saved to: {report_path}")
    
    return report

# ========== MAIN EXECUTION ==========

if __name__ == "__main__":
    print("🧪 COMPREHENSIVE ALGORITHM TESTING")
    print("Testing Treqe Matching Algorithm with 6 test suites")
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    try:
        report = generate_comprehensive_report()
        
        print("\n🎯 NEXT STEPS:")
        print("1. Review the comprehensive test report")
        print("2. Address any identified improvement areas")
        print("3. Integrate algorithm into Treqe backend")
        print("4. Set up production monitoring")
        print("5. Plan iterative improvements based on real data")
        
        print(f"\n✅ Testing completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
        import traceback
        traceback.print_exc()