#!/usr/bin/env python3
"""
Enhanced Algorithm with Circular Matching and Reputation
"""

import json
import random
import time
from typing import List, Dict, Any, Tuple, Set
from dataclasses import dataclass
from enum import Enum

print("="*70)
print("ENHANCED ALGORITHM - CIRCULAR MATCHING + REPUTATION")
print("="*70)

# ========== ENHANCED DATA STRUCTURES ==========

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

@dataclass 
class User:
    id: str
    name: str
    level: UserLevel
    reputation: float  # 0-1000
    offered_items: List[Item]
    desired_items: List[Item]
    
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

# ========== ENHANCED ALGORITHM ==========

def find_direct_matches(users: List[User]) -> List[Dict]:
    """Find direct 1:1 matches"""
    matches = []
    matched_users = set()
    matched_items = set()
    
    for i, user1 in enumerate(users):
        if user1.id in matched_users:
            continue
            
        for user2 in users[i+1:]:
            if user2.id in matched_users:
                continue
            
            for item1 in user1.offered_items:
                if item1.id in matched_items:
                    continue
                    
                for item2 in user2.offered_items:
                    if item2.id in matched_items:
                        continue
                    
                    # Direct match found
                    if (item1 in user2.desired_items and 
                        item2 in user1.desired_items):
                        
                        # Calculate compensation with reputation
                        value_diff = item2.value - item1.value
                        
                        if value_diff > 0:
                            # User1 receives less value, gets compensation
                            compensation = value_diff * (1 - user1.commission_rate()) * user1.reputation_multiplier()
                            payment = value_diff * (1 + user2.commission_rate()) / user2.reputation_multiplier()
                        else:
                            compensation = abs(value_diff) * (1 - user2.commission_rate()) * user2.reputation_multiplier()
                            payment = abs(value_diff) * (1 + user1.commission_rate()) / user1.reputation_multiplier()
                        
                        match_data = {
                            "type": "direct",
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
                        matches.append(match_data)
                        
                        matched_users.add(user1.id)
                        matched_users.add(user2.id)
                        matched_items.add(item1.id)
                        matched_items.add(item2.id)
                        break
                
                if user1.id in matched_users:
                    break
            
            if user1.id in matched_users:
                break
    
    return matches

def find_circular_matches(users: List[User], max_cycle: int = 3) -> List[Dict]:
    """Find circular matches (A→B→C→A)"""
    matches = []
    matched_users = set()
    matched_items = set()
    
    # Try to find 3-user cycles
    for i in range(len(users)):
        user1 = users[i]
        if user1.id in matched_users:
            continue
            
        for j in range(i+1, len(users)):
            user2 = users[j]
            if user2.id in matched_users:
                continue
                
            for k in range(j+1, len(users)):
                user3 = users[k]
                if user3.id in matched_users:
                    continue
                
                # Check for circular exchange
                found_cycle = False
                cycle_items = []
                
                for item1 in user1.offered_items:
                    if item1.id in matched_items:
                        continue
                        
                    for item2 in user2.offered_items:
                        if item2.id in matched_items:
                            continue
                            
                        for item3 in user3.offered_items:
                            if item3.id in matched_items:
                                continue
                            
                            # Check circular desire: user1 wants item2, user2 wants item3, user3 wants item1
                            if (item1 in user2.desired_items and
                                item2 in user3.desired_items and
                                item3 in user1.desired_items):
                                
                                cycle_items = [(user1, item1, user2, item2),
                                              (user2, item2, user3, item3),
                                              (user3, item3, user1, item1)]
                                found_cycle = True
                                break
                        
                        if found_cycle:
                            break
                    
                    if found_cycle:
                        break
                
                if found_cycle and cycle_items:
                    # Calculate net flows and compensations
                    net_flow = {user1.id: 0.0, user2.id: 0.0, user3.id: 0.0}
                    
                    for from_user, from_item, to_user, to_item in cycle_items:
                        net_flow[from_user.id] -= from_item.value
                        net_flow[to_user.id] += to_item.value
                    
                    # Calculate compensations
                    compensations = {}
                    for user_id, flow in net_flow.items():
                        user = next((u for u in [user1, user2, user3] if u.id == user_id), None)
                        if user and flow > 0:  # Net receiver
                            payment = flow * (1 + user.commission_rate()) / user.reputation_multiplier()
                            compensations[user_id] = -payment
                        elif user and flow < 0:  # Net giver
                            receipt = abs(flow) * (1 - user.commission_rate()) * user.reputation_multiplier()
                            compensations[user_id] = receipt
                    
                    match_data = {
                        "type": "circular",
                        "participants": [user1.id, user2.id, user3.id],
                        "exchanges": [
                            {"from": fu.id, "to": tu.id, "item": fi.id, "value": fi.value}
                            for fu, fi, tu, ti in cycle_items
                        ],
                        "compensations": compensations,
                        "total_value": sum(fi.value for _, fi, _, _ in cycle_items) / len(cycle_items)
                    }
                    matches.append(match_data)
                    
                    matched_users.update([user1.id, user2.id, user3.id])
                    for _, fi, _, _ in cycle_items:
                        matched_items.add(fi.id)
    
    return matches

def enhanced_matching_algorithm(users: List[User]) -> List[Dict]:
    """Enhanced algorithm with both direct and circular matching"""
    all_matches = []
    
    # First try circular matches (more value)
    circular_matches = find_circular_matches(users)
    all_matches.extend(circular_matches)
    
    # Get users not matched in circular exchanges
    matched_in_circular = set()
    for match in circular_matches:
        matched_in_circular.update(match["participants"])
    
    remaining_users = [u for u in users if u.id not in matched_in_circular]
    
    # Then try direct matches for remaining users
    direct_matches = find_direct_matches(remaining_users)
    all_matches.extend(direct_matches)
    
    return all_matches

# ========== TEST WITH ORIGINAL SCENARIO ==========

def test_enhanced_algorithm():
    """Test the enhanced algorithm with the original scenario"""
    print("\nTESTING ENHANCED ALGORITHM")
    print("-"*50)
    
    # Original scenario that failed with simple algorithm
    phone = Item("I1", "Smartphone", 300.0, "Electronics")
    laptop = Item("I2", "Laptop", 600.0, "Electronics")
    bike = Item("I3", "Bicycle", 200.0, "Sports")
    jacket = Item("I4", "Designer Jacket", 150.0, "Clothing")
    bookshelf = Item("I5", "Bookshelf", 120.0, "Furniture")
    
    users = [
        User("U1", "Ana", UserLevel.NOVATO, 50.0, [phone], [jacket]),
        User("U2", "Carlos", UserLevel.MIEMBRO, 300.0, [jacket], [laptop]),
        User("U3", "Beatriz", UserLevel.CONFIABLE, 700.0, [laptop], [phone]),
        User("U4", "David", UserLevel.ELITE, 950.0, [bike], [bookshelf]),
        User("U5", "Elena", UserLevel.CONFIABLE, 650.0, [bookshelf], [bike]),
    ]
    
    print("Original Scenario (5 users):")
    print("  Ana: Phone -> Jacket")
    print("  Carlos: Jacket -> Laptop")
    print("  Beatriz: Laptop -> Phone")
    print("  David: Bike -> Bookshelf")
    print("  Elena: Bookshelf -> Bike")
    
    print("\nRunning enhanced algorithm...")
    matches = enhanced_matching_algorithm(users)
    
    print(f"\nResults:")
    print(f"  Total matches found: {len(matches)}")
    
    total_value = 0
    total_participants = 0
    
    for i, match in enumerate(matches, 1):
        print(f"\n  Match {i} ({match['type']}):")
        print(f"    Participants: {', '.join(match['participants'])}")
        print(f"    Total value: EUR{match['total_value']:.2f}")
        
        for exchange in match["exchanges"]:
            print(f"    {exchange['from']} -> {exchange['to']}: Item {exchange['item']} (EUR{exchange['value']:.2f})")
        
        if match["compensations"]:
            print(f"    Compensations:")
            for user_id, amount in match["compensations"].items():
                if amount > 0:
                    print(f"      {user_id} receives: EUR{amount:.2f}")
                elif amount < 0:
                    print(f"      {user_id} pays: EUR{abs(amount):.2f}")
        
        total_value += match["total_value"]
        total_participants += len(match["participants"])
    
    print(f"\nSummary:")
    print(f"  Users matched: {total_participants}/{len(users)} ({total_participants/len(users):.0%})")
    print(f"  Total value exchanged: EUR{total_value:.2f}")
    
    # Test with random larger scenario
    print("\n" + "-"*50)
    print("Testing with random scenario (20 users):")
    
    # Generate random users
    items_pool = [
        Item(f"I{i}", f"Item{i}", random.uniform(50, 500), 
             random.choice(["Electronics", "Clothing", "Sports", "Home"]))
        for i in range(100)
    ]
    
    random_users = []
    for i in range(20):
        level = random.choice(list(UserLevel))
        reputation = random.uniform(0, 1000)
        
        offered = random.sample(items_pool, random.randint(1, 2))
        available = [item for item in items_pool if item not in offered]
        desired = random.sample(available, random.randint(1, 2))
        
        user = User(
            id=f"RU{i+1}",
            name=f"RandomUser{i+1}",
            level=level,
            reputation=reputation,
            offered_items=offered,
            desired_items=desired
        )
        random_users.append(user)
    
    start_time = time.time()
    random_matches = enhanced_matching_algorithm(random_users)
    exec_time = time.time() - start_time
    
    random_matched = sum(len(m["participants"]) for m in random_matches)
    random_value = sum(m["total_value"] for m in random_matches)
    
    print(f"  Execution time: {exec_time:.3f}s")
    print(f"  Matches found: {len(random_matches)}")
    print(f"  Users matched: {random_matched}/{len(random_users)} ({random_matched/len(random_users):.0%})")
    print(f"  Total value: EUR{random_value:.2f}")
    
    # Analyze match types
    direct_count = sum(1 for m in random_matches if m["type"] == "direct")
    circular_count = sum(1 for m in random_matches if m["type"] == "circular")
    
    print(f"  Direct matches: {direct_count}")
    print(f"  Circular matches: {circular_count}")
    
    return len(matches) > 0

# ========== COMPREHENSIVE VALIDATION ==========

def validate_algorithm():
    """Comprehensive validation of enhanced algorithm"""
    print("\n" + "="*70)
    print("COMPREHENSIVE VALIDATION")
    print("="*70)
    
    validation_tests = []
    
    # Test 1: Original scenario should now work
    print("\n[1] TEST: Original Scenario (previously failed)")
    success = test_enhanced_algorithm()
    validation_tests.append(("Original scenario works", success))
    
    # Test 2: Edge cases
    print("\n[2] TEST: Edge Cases")
    
    # Empty list
    matches = enhanced_matching_algorithm([])
    validation_tests.append(("Empty list", matches == []))
    
    # Single user
    item = Item("I1", "Test", 100.0, "Test")
    user = User("U1", "Test", UserLevel.NOVATO, 100.0, [item], [item])
    matches = enhanced_matching_algorithm([user])
    validation_tests.append(("Single user", matches == []))
    
    # Perfect direct match
    item1 = Item("I1", "Item1", 100.0, "Test")
    item2 = Item("I2", "Item2", 100.0, "Test")
    user1 = User("U1", "User1", UserLevel.NOVATO, 100.0, [item1], [item2])
    user2 = User("U2", "User2", UserLevel.NOVATO, 100.0, [item2], [item1])
    matches = enhanced_matching_algorithm([user1, user2])
    validation_tests.append(("Perfect direct match", len(matches) == 1))
    
    # Test 3: Reputation impact
    print("\n[3] TEST: Reputation Impact")
    
    expensive = Item("I1", "Expensive", 300.0, "Test")
    cheap = Item("I2", "Cheap", 100.0, "Test")
    
    # Same exchange, different reputations
    user_low = User("U1", "LowRep", UserLevel.NOVATO, 100.0, [che