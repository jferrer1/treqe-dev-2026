#!/usr/bin/env python3
"""
Comprehensive Algorithm Testing for Treqe Matching
Simplified version with all test types
"""

import json
import random
import time
import statistics
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum

print("="*70)
print("🧪 COMPREHENSIVE ALGORITHM TESTING - TREQE MATCHING")
print("="*70)

# ========== CORE DATA STRUCTURES ==========

class UserLevel(Enum):
    NOVATO = 1
    MIEMBRO = 2
    CONFIABLE = 3
    ELITE = 4

@dataclass
class Item:
    id: str
    name: str
    value: float
    category: str
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Item) and self.id == other.id

@dataclass 
class User:
    id: str
    name: str
    level: UserLevel
    reputation: float
    offered_items: List[Item]
    desired_items: List[Item]
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id
    
    def total_offered_value(self) -> float:
        return sum(item.value for item in self.offered_items)
    
    def total_desired_value(self) -> float:
        return sum(item.value for item in self.desired_items)
    
    def commission_rate(self) -> float:
        rates = {
            UserLevel.NOVATO: 0.01,
            UserLevel.MIEMBRO: 0.01,
            UserLevel.CONFIABLE: 0.009,
            UserLevel.ELITE: 0.008
        }
        return rates.get(self.level, 0.01)
    
    def reputation_multiplier(self) -> float:
        return 1.0 + (self.reputation / 1000) * 0.1

# ========== ALGORITHM IMPLEMENTATION ==========

def greedy_matching_algorithm(users: List[User]) -> List[Dict]:
    """Greedy matching algorithm with comprehensive testing"""
    wheels = []
    matched_user_ids = set()
    matched_item_ids = set()
    
    # Sort by reputation (higher first)
    sorted_users = sorted(users, key=lambda u: u.reputation, reverse=True)
    
    # Direct 1:1 exchanges
    for i, user1 in enumerate(sorted_users):
        if user1.id in matched_user_ids:
            continue
            
        for user2 in sorted_users[i+1:]:
            if user2.id in matched_user_ids:
                continue
            
            for item1 in user1.offered_items:
                if item1.id in matched_item_ids:
                    continue
                    
                for item2 in user2.offered_items:
                    if item2.id in matched_item_ids:
                        continue
                    
                    if (item1 in user2.desired_items and 
                        item2 in user1.desired_items):
                        
                        # Calculate compensation
                        value_diff = item2.value - item1.value
                        if value_diff > 0:
                            # User1 receives less value, gets compensation
                            compensation = value_diff * (1 - user1.commission_rate()) * user1.reputation_multiplier()
                            payment = value_diff * (1 + user2.commission_rate()) / user2.reputation_multiplier()
                        else:
                            compensation = abs(value_diff) * (1 - user2.commission_rate()) * user2.reputation_multiplier()
                            payment = abs(value_diff) * (1 + user1.commission_rate()) / user1.reputation_multiplier()
                        
                        wheel = {
                            "participants": [user1.id, user2.id],
                            "exchanges": [
                                {"from": user1.id, "to": user2.id, "item": item1.id, "value": item1.value},
                                {"from": user2.id, "to": user1.id, "item": item2.id, "value": item2.value}
                            ],
                            "compensations": {
                                user1.id: compensation if value_diff > 0 else -payment,
                                user2.id: -payment if value_diff > 0 else compensation
                            },
                            "total_value": (item1.value + item2.value) / 2
                        }
                        wheels.append(wheel)
                        
                        matched_user_ids.add(user1.id)
                        matched_user_ids.add(user2.id)
                        matched_item_ids.add(item1.id)
                        matched_item_ids.add(item2.id)
                        break
                
                if user1.id in matched_user_ids:
                    break
            
            if user1.id in matched_user_ids:
                break
    
    return wheels

# ========== TEST DATA GENERATORS ==========

def create_simple_test_scenario() -> List[User]:
    """Create simple test scenario"""
    items = [
        Item("I1", "Smartphone", 300.0, "Electronics"),
        Item("I2", "Laptop", 600.0, "Electronics"),
        Item("I3", "Bicycle", 200.0, "Sports"),
        Item("I4", "Jacket", 150.0, "Clothing"),
        Item("I5", "Bookshelf", 120.0, "Furniture"),
    ]
    
    users = [
        User("U1", "Ana", UserLevel.NOVATO, 50.0, [items[0]], [items[3]]),
        User("U2", "Carlos", UserLevel.MIEMBRO, 300.0, [items[3]], [items[1]]),
        User("U3", "Beatriz", UserLevel.CONFIABLE, 700.0, [items[1]], [items[0]]),
        User("U4", "David", UserLevel.ELITE, 950.0, [items[2]], [items[4]]),
        User("U5", "Elena", UserLevel.CONFIABLE, 650.0, [items[4]], [items[2]]),
    ]
    
    return users

def create_random_test_scenario(n_users: int = 10) -> List[User]:
    """Create random test scenario"""
    items_pool = [
        Item(f"I{i}", f"Item_{i}", random.uniform(50, 500), 
             random.choice(["Electronics", "Clothing", "Sports", "Home"]))
        for i in range(50)
    ]
    
    users = []
    for i in range(n_users):
        level = random.choice(list(UserLevel))
        reputation = random.uniform(0, 1000)
        
        offered_items = random.sample(items_pool, random.randint(1, 2))
        available_items = [item for item in items_pool if item not in offered_items]
        desired_items = random.sample(available_items, random.randint(1, 2))
        
        user = User(
            id=f"U{i+1}",
            name=f"User_{i+1}",
            level=level,
            reputation=reputation,
            offered_items=offered_items,
            desired_items=desired_items
        )
        users.append(user)
    
    return users

# ========== TEST SUITES ==========

def run_unit_tests():
    """Unit tests for core functionality"""
    print("\n[1] 🔬 UNIT TESTS")
    print("-"*50)
    
    tests = []
    
    # Test 1: Item equality
    item1 = Item("I1", "Test", 100.0, "Test")
    item2 = Item("I1", "Test", 100.0, "Test")
    item3 = Item("I2", "Different", 100.0, "Test")
    tests.append(("Item equality", item1 == item2 and item1 != item3))
    
    # Test 2: Commission rates
    user_novato = User("U1", "Test", UserLevel.NOVATO, 100.0, [], [])
    user_elite = User("U2", "Test", UserLevel.ELITE, 1000.0, [], [])
    tests.append(("Commission rates", 
                  abs(user_novato.commission_rate() - 0.01) < 0.001 and
                  abs(user_elite.commission_rate() - 0.008) < 0.001))
    
    # Test 3: Reputation multiplier
    user_low = User("U3", "Test", UserLevel.NOVATO, 0.0, [], [])
    user_high = User("U4", "Test", UserLevel.NOVATO, 1000.0, [], [])
    tests.append(("Reputation multiplier",
                  abs(user_low.reputation_multiplier() - 1.0) < 0.001 and
                  abs(user_high.reputation_multiplier() - 1.1) < 0.001))
    
    # Display results
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for name, result in tests:
        print(f"   {'✅' if result else '❌'} {name}")
    
    print(f"\n📊 Unit Tests: {passed}/{total} passed ({passed/total*100:.0f}%)")
    return passed, total

def run_functional_tests():
    """Functional tests for matching algorithm"""
    print("\n[2] 🔧 FUNCTIONAL TESTS")
    print("-"*50)
    
    tests = []
    
    # Test 1: Simple matching works
    users = create_simple_test_scenario()
    wheels = greedy_matching_algorithm(users)
    tests.append(("Simple scenario matching", len(wheels) > 0))
    
    # Test 2: No matches for incompatible users
    item1 = Item("I1", "Item1", 100.0, "Test")
    item2 = Item("I2", "Item2", 100.0, "Test")
    user1 = User("U1", "Test1", UserLevel.NOVATO, 100.0, [item1], [])
    user2 = User("U2", "Test2", UserLevel.NOVATO, 100.0, [item2], [])
    wheels = greedy_matching_algorithm([user1, user2])
    tests.append(("No matches for incompatible", len(wheels) == 0))
    
    # Test 3: Perfect match
    user3 = User("U3", "Test3", UserLevel.NOVATO, 100.0, [item1], [item2])
    user4 = User("U4", "Test4", UserLevel.NOVATO, 100.0, [item2], [item1])
    wheels = greedy_matching_algorithm([user3, user4])
    tests.append(("Perfect 1:1 match", len(wheels) == 1))
    
    # Display results
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for name, result in tests:
        print(f"   {'✅' if result else '❌'} {name}")
    
    print(f"\n📊 Functional Tests: {passed}/{total} passed ({passed/total*100:.0f}%)")
    return passed, total

def run_performance_tests():
    """Performance and scalability tests"""
    print("\n[3] ⚡ PERFORMANCE TESTS")
    print("-"*50)
    
    results = []
    
    # Test different scales
    scales = [5, 10, 20, 30]
    
    for scale in scales:
        users = create_random_test_scenario(scale)
        
        start_time = time.time()
        wheels = greedy_matching_algorithm(users)
        exec_time = time.time() - start_time
        
        matched_users = sum(len(w["participants"]) for w in wheels)
        match_rate = matched_users / scale if scale > 0 else 0
        
        results.append({
            "scale": scale,
            "time": exec_time,
            "wheels": len(wheels),
            "match_rate": match_rate,
            "time_per_user": exec_time / scale if scale > 0 else 0
        })
        
        print(f"   • {scale} users: {exec_time:.3f}s, {len(wheels)} wheels, {match_rate:.1%} match rate")
    
    # Analyze scalability
    print("\n📈 Scalability Analysis:")
    print("   Users | Time (s) | Wheels | Match Rate")
    print("   " + "-"*40)
    for r in results:
        print(f"   {r['scale']:6d} | {r['time']:8.3f} | {r['wheels']:6d} | {r['match_rate']:10.1%}")
    
    return results

def run_edge_case_tests():
    """Edge case and stress tests"""
    print("\n[4] 🧪 EDGE CASE TESTS")
    print("-"*50)
    
    tests = []
    
    # Test 1: Empty user list
    wheels = greedy_matching_algorithm([])
    tests.append(("Empty user list", wheels == []))
    
    # Test 2: Single user
    users = create_random_test_scenario(1)
    wheels = greedy_matching_algorithm(users)
    tests.append(("Single user", wheels == []))
    
    # Test 3: Extreme value difference
    expensive = Item("I1", "Diamond", 10000.0, "Jewelry")
    cheap = Item("I2", "Pen", 1.0, "Office")
    user1 = User("U1", "Rich", UserLevel.ELITE, 1000.0, [expensive], [cheap])
    user2 = User("U2", "Poor", UserLevel.NOVATO, 10.0, [cheap], [expensive])
    wheels = greedy_matching_algorithm([user1, user2])
    tests.append(("Extreme value difference", len(wheels) == 1))
    
    # Test 4: Zero reputation
    user3 = User("U3", "ZeroRep", UserLevel.NOVATO, 0.0, [expensive], [cheap])
    user4 = User("U4", "Normal", UserLevel.NOVATO, 500.0, [cheap], [expensive])
    wheels = greedy_matching_algorithm([user3, user4])
    tests.append(("Zero reputation handling", len(wheels) == 1))
    
    # Display results
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for name, result in tests:
        print(f"   {'✅' if result else '❌'} {name}")
    
    print(f"\n📊 Edge Case Tests: {passed}/{total} passed ({passed/total*100:.0f}%)")
    return passed, total

def run_acceptance_tests():
    """Acceptance tests - real-world scenarios"""
    print("\n[5] 🎯 ACCEPTANCE TESTS")
    print("-"*50)
    
    scenarios = [
        {
            "name": "Perfect circular exchange",
            "users": create_simple_test_scenario(),
            "min_wheels": 2,
            "min_match_rate": 0.6
        },
        {
            "name": "Random medium scenario",
            "users": create_random_test_scenario(15),
            "min_wheels": 3,
            "min_match_rate": 0.4
        }
    ]
    
    passed = 0
    total = len(scenarios)
    
    for scenario in scenarios:
        wheels = greedy_matching_algorithm(scenario["users"])
        
        matched_users = sum(len(w["participants"]) for w in wheels)
        match_rate = matched_users / len(scenario["users"])
        
        success = (len(wheels) >= scenario["min_wheels"] and 
                   match_rate >= scenario["min_match_rate"])
        
        print(f"   {'✅' if success else '❌'} {scenario['name']}:")
        print(f"     • Wheels: {len(wheels)} (min: {scenario['min_wheels']})")
        print(f"     • Match rate: {match_rate:.1%} (min: {scenario['min_match_rate']:.0%})")
        
        if success:
            passed += 1
    
    print(f"\n📊 Acceptance Tests: {passed}/{total} passed ({passed/total*100:.0f}%)")
    return passed, total

def run_algorithm_analysis():
    """Algorithm behavior analysis"""
    print("\n[6] 📊 ALGORITHM ANALYSIS")
    print("-"*50)
    
    insights = []
    
    # Analyze reputation impact
    print("\n🔍 Reputation Impact Analysis:")
    
    item1 = Item("I1", "Item", 100.0, "Test")
    item2 = Item("I2", "Item", 150.0, "Test")
    
    # Same exchange, different reputations
    test_cases = [
        ("Both average", 500.0, 500.0),
        ("High vs Low", 900.0, 100.0),
        ("Elite vs Novato", 1000.0, 50.0),
    ]
    
    for name, rep1, rep2 in test_cases:
        user1 = User("U1", "User1", UserLevel.CONFIABLE, rep1, [item1], [item2])
        user2 = User("U2", "User2", UserLevel.CONFIABLE, rep2, [item2], [item1])
        
        wheels = greedy_matching_algorithm([user1, user2])
        if wheels:
            comp = wheels[0]["compensations"]
            payment1 = abs(comp.get("U1", 0))
            payment2 = abs(comp.get("U2", 0))
            
            print(f"   • {name}: User1 pays €{payment1:.2f}, User2 pays €{