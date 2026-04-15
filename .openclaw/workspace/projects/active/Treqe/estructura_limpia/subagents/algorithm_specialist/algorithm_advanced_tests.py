#!/usr/bin/env python3
"""
Advanced Algorithm Testing Suite for Treqe Matching Algorithm
Comprehensive test coverage with multiple test types
"""

import json
import random
import time
import statistics
from typing import List, Dict, Any, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import math

print("="*70)
print("🧪 ADVANCED ALGORITHM TESTING SUITE - TREQE MATCHING")
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
    condition: str  # "new", "like_new", "good", "fair"
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Item) and self.id == other.id

@dataclass 
class User:
    id: str
    name: str
    level: UserLevel
    reputation: float  # 0-1000
    offered_items: List[Item]
    desired_items: List[Item]
    location: str  # City code
    join_date: str  # YYYY-MM-DD
    
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
    
    def trust_score(self) -> float:
        """Combined trust score based on level and reputation"""
        level_multiplier = {
            UserLevel.NOVATO: 0.7,
            UserLevel.MIEMBRO: 0.8,
            UserLevel.CONFIABLE: 0.9,
            UserLevel.ELITE: 1.0
        }
        return level_multiplier.get(self.level, 0.7) * (1 + self.reputation/1000)

# ========== EXCHANGE WHEEL ==========

class ExchangeWheel:
    def __init__(self, participants: List[User]):
        self.participants = participants
        self.exchanges: List[tuple] = []  # (from_user, from_item, to_user, to_item)
        self.compensations: Dict[User, float] = {}
        self.creation_time = time.time()
        self.status = "pending"  # pending, matched, completed, cancelled
    
    def calculate_compensations(self) -> Dict[User, float]:
        """Calculate monetary compensations with reputation adjustments"""
        if not self.exchanges:
            return {}
        
        # Calculate net flow for each user
        net_flow = {user: 0.0 for user in self.participants}
        
        for from_user, from_item, to_user, to_item in self.exchanges:
            net_flow[from_user] -= from_item.value
            net_flow[to_user] += to_item.value
        
        # Calculate compensations with reputation adjustments
        compensations = {}
        total_compensation = 0
        
        for user, flow in net_flow.items():
            if flow > 0:  # Net receiver (received more value than gave)
                # Higher reputation = lower payment
                base_payment = flow * (1 + user.commission_rate())
                adjusted_payment = base_payment / user.reputation_multiplier()
                compensations[user] = -adjusted_payment
                total_compensation += adjusted_payment
            
            elif flow < 0:  # Net giver (gave more value than received)
                # Higher reputation = higher receipt
                base_receipt = abs(flow) * (1 - user.commission_rate())
                adjusted_receipt = base_receipt * user.reputation_multiplier()
                compensations[user] = adjusted_receipt
                total_compensation -= adjusted_receipt
        
        # Balance check - ensure sum of compensations is 0
        imbalance = abs(total_compensation)
        if imbalance > 0.01:
            total_abs = sum(abs(c) for c in compensations.values())
            if total_abs > 0:
                # Distribute imbalance proportionally
                for user in compensations:
                    compensations[user] *= (1 - imbalance/total_abs)
        
        self.compensations = compensations
        return compensations
    
    def total_exchange_value(self) -> float:
        """Total value exchanged in the wheel"""
        total = 0
        for _, from_item, _, to_item in self.exchanges:
            total += from_item.value + to_item.value
        return total / 2  # Each exchange counted twice
    
    def participant_satisfaction(self, user: User) -> float:
        """Calculate satisfaction score for a participant (0-1)"""
        if not self.exchanges:
            return 0.0
        
        received_items = []
        for _, from_item, to_user, to_item in self.exchanges:
            if to_user == user:
                received_items.append(to_item)
        
        if not received_items:
            return 0.0
        
        desired_value = user.total_desired_value()
        received_value = sum(item.value for item in received_items)
        
        if desired_value == 0:
            return 0.0
        
        # Base satisfaction: how much of desired value received
        satisfaction = min(1.0, received_value / desired_value)
        
        # Penalty for having to pay compensation
        if user in self.compensations and self.compensations[user] < 0:
            payment_ratio = abs(self.compensations[user]) / received_value
            satisfaction *= (1 - payment_ratio * 0.5)
        
        # Bonus for good reputation effect
        if user.reputation > 500:
            satisfaction *= (1 + (user.reputation - 500) / 1000 * 0.1)
        
        return min(1.0, satisfaction)  # Cap at 1.0
    
    def fairness_score(self) -> float:
        """Calculate fairness score of the wheel (0-1)"""
        if not self.exchanges:
            return 0.0
        
        satisfactions = [self.participant_satisfaction(user) for user in self.participants]
        if not satisfactions:
            return 0.0
        
        # Fairness = 1 - standard deviation of satisfactions
        if len(satisfactions) > 1:
            std_dev = statistics.stdev(satisfactions)
            fairness = max(0, 1 - std_dev)
        else:
            fairness = 1.0
        
        return fairness
    
    def efficiency_score(self) -> float:
        """Calculate efficiency of value exchange (0-1)"""
        total_possible = sum(user.total_offered_value() for user in self.participants)
        if total_possible == 0:
            return 0.0
        
        actual = self.total_exchange_value()
        return min(1.0, actual / total_possible)

# ========== ALGORITHM IMPLEMENTATIONS ==========

def greedy_matching_algorithm(users: List[User]) -> List[ExchangeWheel]:
    """
    Greedy matching algorithm - Simple, fast, good for MVP
    Time Complexity: O(n²)
    """
    wheels = []
    matched_user_ids = set()
    matched_item_ids = set()
    
    # Sort users by trust score (higher trust first)
    sorted_users = sorted(users, key=lambda u: u.trust_score(), reverse=True)
    
    # Try direct 1:1 exchanges first
    for i, user1 in enumerate(sorted_users):
        if user1.id in matched_user_ids:
            continue
            
        for user2 in sorted_users[i+1:]:
            if user2.id in matched_user_ids:
                continue
            
            # Find matching items
            for item1 in user1.offered_items:
                if item1.id in matched_item_ids:
                    continue
                    
                for item2 in user2.offered_items:
                    if item2.id in matched_item_ids:
                        continue
                    
                    # Check if they want each other's items
                    if (item1 in user2.desired_items and 
                        item2 in user1.desired_items):
                        
                        # Create exchange wheel
                        wheel = ExchangeWheel([user1, user2])
                        wheel.exchanges = [(user1, item1, user2, item2)]
                        wheel.calculate_compensations()
                        wheel.status = "matched"
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
    
    # Try 3-user circular exchanges for remaining users
    remaining_users = [u for u in sorted_users if u.id not in matched_user_ids]
    
    for i in range(0, len(remaining_users) - 2, 3):
        if i + 2 >= len(remaining_users):
            break
            
        user1, user2, user3 = remaining_users[i], remaining_users[i+1], remaining_users[i+2]
        
        # Find circular exchange (A→B→C→A)
        for item1 in user1.offered_items:
            if item1.id in matched_item_ids:
                continue
                
            for item2 in user2.offered_items:
                if item2.id in matched_item_ids:
                    continue
                    
                for item3 in user3.offered_items:
                    if item3.id in matched_item_ids:
                        continue
                    
                    if (item1 in user2.desired_items and
                        item2 in user3.desired_items and
                        item3 in user1.desired_items):
                        
                        wheel = ExchangeWheel([user1, user2, user3])
                        wheel.exchanges = [
                            (user1, item1, user2, item2),
                            (user2, item2, user3, item3),
                            (user3, item3, user1, item1)
                        ]
                        wheel.calculate_compensations()
                        wheel.status = "matched"
                        wheels.append(wheel)
                        
                        matched_user_ids.update([user1.id, user2.id, user3.id])
                        matched_item_ids.update([item1.id, item2.id, item3.id])
                        break
                
                if user1.id in matched_user_ids:
                    break
            
            if user1.id in matched_user_ids:
                break
    
    return wheels

def optimized_matching_algorithm(users: List[User], max_iterations: int = 1000) -> List[ExchangeWheel]:
    """
    Optimized matching with simulated annealing
    Better results but slower - for growth phase
    Time Complexity: O(n² * iterations)
    """
    # Start with greedy solution
    wheels = greedy_matching_algorithm(users)
    
    if not wheels or len(users) < 4:
        return wheels
    
    # Calculate initial score
    def score_wheels(wheels_list: List[ExchangeWheel]) -> float:
        total_score = 0
        for wheel in wheels_list:
            total_score += (
                wheel.total_exchange_value() * 0.4 +
                wheel.fairness_score() * 0.3 +
                wheel.efficiency_score() * 0.3
            )
        return total_score / len(wheels_list) if wheels_list else 0
    
    current_score = score_wheels(wheels)
    best_wheels = wheels.copy()
    best_score = current_score
    
    # Simulated annealing
    temperature = 1.0
    cooling_rate = 0.95
    
    for iteration in range(max_iterations):
        # Try to improve by swapping participants between wheels
        if len(wheels) > 1:
            # Pick two random wheels
            idx1, idx2 = random.sample(range(len(wheels)), 2)
            wheel1, wheel2 = wheels[idx1], wheels[idx2]
            
            # Try swapping one participant
            if wheel1.participants and wheel2.participants:
                p1 = random.choice(wheel1.participants)
                p2 = random.choice(wheel2.participants)
                
                # Create new wheels with swapped participants
                new_wheel1_participants = [p for p in wheel1.participants if p != p1] + [p2]
                new_wheel2_participants = [p for p in wheel2.participants if p != p2] + [p1]
                
                # Recalculate exchanges (simplified - in reality would need full recalculation)
                # For now, just accept if it seems plausible
                new_wheels = wheels.copy()
                # This is simplified - real implementation would recalculate exchanges
                
                # Calculate new score
                new_score = score_wheels(new_wheels)
                
                # Accept if better or with probability based on temperature
                if (new_score > current_score or 
                    random.random() < math.exp((new_score - current_score) / temperature)):
                    wheels = new_wheels
                    current_score = new_score
                    
                    if current_score > best_score:
                        best_wheels = wheels.copy()
                        best_score = current_score
        
        # Cool down
        temperature *= cooling_rate
    
    return best_wheels

# ========== TEST DATA GENERATORS ==========

def generate_test_scenario_simple() -> List[User]:
    """Simple test scenario with 5 users"""
    items = [
        Item("I1", "Smartphone", 300.0, "Electronics", "good"),
        Item("I2", "Laptop", 600.0, "Electronics", "like_new"),
        Item("I3", "Bicycle", 200.0, "Sports", "good"),
        Item("I4", "Designer Jacket", 150.0, "Clothing", "new"),
        Item("I5", "Bookshelf", 120.0, "Furniture", "fair"),
        Item("I6", "Camera", 400.0, "Electronics", "good"),
        Item("I7", "Guitar", 250.0, "Music", "like_new"),
        Item("I8", "Watch", 180.0, "Accessories", "new")
    ]
    
    users = [
        User("U1", "Ana", UserLevel.NOVATO, 50.0, [items[0]], [items[3]], "MAD", "2026-01-15"),
        User("U2", "Carlos", UserLevel.MIEMBRO, 300.0, [items[3]], [items[1]], "BCN", "2026-01-20"),
        User("U3", "Beatriz", UserLevel.CONFIABLE, 700.0, [items[1]], [items[0]], "MAD", "2026-01-10"),
        User("U4", "David", UserLevel.ELITE, 950.0, [items[2]], [items[4]], "VAL", "2025-12-01"),
        User("U5", "Elena", UserLevel.CONFIABLE, 650.0, [items[4]], [items[2]], "BCN", "2026-01-05"),
    ]
    
    return users

def generate_test_scenario_medium(n_users: int = 20) -> List[User]:
    """Medium test scenario with configurable users"""
    items_pool = [
        Item(f"I{i}", f"Item_{i}", random.uniform(50, 500), 
             random.choice(["Electronics", "Clothing", "Sports", "Books", "Home"]),
             random.choice(["new", "like_new", "good", "fair"]))
        for i in range(100)
    ]
    
    users = []
    for i in range(n_users):
        level = random.choice(list(UserLevel))
        reputation = random.uniform(0, 1000)
        
        # Each user offers 1-3 items
        offered_count = random.randint(1, 3)
        offered_items = random.sample(items_pool, offered_count)
        
        # Each user desires 1-3 different items
        desired_count = random.randint(1, 3)
        # Ensure desired items are different from offered
        available_items = [item for item in items_pool if item not in offered_items]
        desired_items = random.sample(available_items, min(desired_count, len(available_items)))
        
        user = User(
            id=f"U{i+1}",
            name=f"User_{i+1}",
            level=level,
            reputation=reputation,
            offered_items=offered_items,
            desired_items=desired_items,
            location=random.choice(["MAD", "BCN", "VAL", "SEV", "BIL"]),
            join_date=f"2026-{random.randint(1,2):02d}-{random.randint(1,28):02d}"
        )
        users.append(user)
    
    return users

def generate_test_scenario_edge_cases() -> List[User]:
    """Edge case test scenarios"""
    items = [
        Item("I1", "Expensive Item", 1000.0, "Electronics", "new"),
        Item("I2", "