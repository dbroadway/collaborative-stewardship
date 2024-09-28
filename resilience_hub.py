import random
import math

class ResilienceHub:
    def __init__(self, name, population, resources, technology_level):
        self.name = name
        self.initial_population = population
        self.population = population
        self.resources = resources
        self.technology_level = technology_level
        self.happiness = 75
        self.environmental_health = 100
        self.social_cohesion = 75
        self.sustainability_practices = 50
        self.long_term_goal = random.uniform(80, 100)

    def produce(self, global_resources):
        for resource in self.resources:
            efficiency = self.technology_level * (1 + self.sustainability_practices / 200)
            production = (
                self.population 
                * efficiency
                * random.uniform(0.8, 1.2) 
                * (self.environmental_health / 100)
            )
            max_production = global_resources[resource] * 0.01 * efficiency
            production = min(production, max_production)
            self.resources[resource] += production
            global_resources[resource] -= production

    def consume(self):
        for resource in self.resources:
            efficiency = 1 - (self.sustainability_practices / 200)
            consumption = self.population * random.uniform(0.8, 1.2) * efficiency
            if self.resources[resource] >= consumption:
                self.resources[resource] -= consumption
                self.happiness += random.uniform(0, 1)
            else:
                deficit = consumption - self.resources[resource]
                self.resources[resource] = 0
                self.happiness -= (deficit / consumption) * random.uniform(1, 5)
        
        self.environmental_health -= random.uniform(0, 0.1) * (1 - self.sustainability_practices / 100)
        self.environmental_health += random.uniform(0, 0.05) * (self.sustainability_practices / 100)
        self.environmental_health = max(0, min(self.environmental_health, 100))
        
        self.social_cohesion += random.uniform(-0.2, 0.2)
        self.social_cohesion = max(0, min(self.social_cohesion, 100))
        
        self.happiness = (
            0.3 * self.happiness +
            0.3 * self.environmental_health +
            0.2 * self.social_cohesion +
            0.2 * (self.sustainability_practices / 100)
        )
        self.happiness = max(0, min(self.happiness, 100))

    def trade(self, other_hub):
        for resource in self.resources:
            if self.resources[resource] > other_hub.resources[resource]:
                amount = (self.resources[resource] - other_hub.resources[resource]) / 4
                self.resources[resource] -= amount
                other_hub.resources[resource] += amount

    def apply_random_event(self):
        events = [
            "natural_disaster", "technological_breakthrough", "social_movement",
            "resource_discovery", "environmental_initiative", "education_program"
        ]
        weights = [1, 1, 1, 1, 1 + (self.sustainability_practices / 100), 1 + (self.sustainability_practices / 100)]
        event = random.choices(events, weights=weights)[0]

        if event == "natural_disaster":
            impact = random.uniform(0.05, 0.15) * (1 - self.sustainability_practices / 200)
            self.resources = {k: v * (1 - impact) for k, v in self.resources.items()}
            self.environmental_health -= random.uniform(2, 8) * (1 - self.sustainability_practices / 200)
        elif event == "technological_breakthrough":
            self.technology_level *= random.uniform(1.05, 1.15)
        elif event == "social_movement":
            self.social_cohesion += random.uniform(2, 8)
            self.sustainability_practices += random.uniform(1, 5)
        elif event == "resource_discovery":
            resource = random.choice(list(self.resources.keys()))
            self.resources[resource] *= random.uniform(1.1, 1.3)
        elif event == "environmental_initiative":
            self.environmental_health += random.uniform(2, 5)
            self.sustainability_practices += random.uniform(1, 3)
        elif event == "education_program":
            self.sustainability_practices += random.uniform(2, 5)
            self.social_cohesion += random.uniform(1, 3)
            self.technology_level *= random.uniform(1.01, 1.05)
        
        self.environmental_health = max(0, min(self.environmental_health, 100))
        self.social_cohesion = max(0, min(self.social_cohesion, 100))
        self.sustainability_practices = max(0, min(self.sustainability_practices, 100))

    def update_population(self):
        resource_factor = min(1, sum(self.resources.values()) / (self.population * 50))
        growth_rate = (
            0.001 * (self.happiness / 100)
            * resource_factor
            * (self.environmental_health / 100)
            * (1 - abs(self.population - self.initial_population) / self.initial_population)
        )
        self.population *= (1 + growth_rate)
        self.population = max(self.initial_population * 0.1, min(self.population, self.initial_population * 2))

    def plan_long_term(self):
        goal_difference = self.long_term_goal - self.sustainability_practices
        self.sustainability_practices += goal_difference * 0.01
        if abs(goal_difference) < 1:
            self.long_term_goal = min(100, self.long_term_goal + random.uniform(0, 5))