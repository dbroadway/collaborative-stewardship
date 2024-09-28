import random
from resilience_hub import ResilienceHub

class CollaborativeStewardship:
    def __init__(self, total_population, num_hubs):
        self.hubs = []
        self.global_resources = {
            "food": total_population * 100,
            "water": total_population * 100,
            "energy": total_population * 100
        }
        avg_population = total_population // num_hubs
        for i in range(num_hubs):
            name = f"Hub-{i+1}"
            population = max(10, int(random.gauss(avg_population, avg_population/4)))
            resources = {
                "food": population * random.randint(5, 15),
                "water": population * random.randint(5, 15),
                "energy": population * random.randint(5, 15)
            }
            technology_level = random.uniform(0.5, 1.5)
            self.hubs.append(ResilienceHub(name, population, resources, technology_level))
        self.initial_total_population = total_population
        self.initial_global_resources = self.global_resources.copy()

    def simulate(self, num_days):
        history = {hub.name: {
            "resources": [], 
            "happiness": [], 
            "environmental_health": [],
            "social_cohesion": [],
            "population": [],
            "sustainability_practices": []
        } for hub in self.hubs}

        for _ in range(num_days):
            self.regenerate_resources()
            for hub in self.hubs:
                hub.produce(self.global_resources)
                hub.consume()
                hub.update_population()
                hub.plan_long_term()
                if random.random() < 0.01:
                    hub.apply_random_event()

            self.inter_hub_resource_sharing()
            self.knowledge_transfer()

            for hub in self.hubs:
                history[hub.name]["resources"].append(sum(hub.resources.values()))
                history[hub.name]["happiness"].append(hub.happiness)
                history[hub.name]["environmental_health"].append(hub.environmental_health)
                history[hub.name]["social_cohesion"].append(hub.social_cohesion)
                history[hub.name]["population"].append(hub.population)
                history[hub.name]["sustainability_practices"].append(hub.sustainability_practices)

        return history

    def regenerate_resources(self):
        avg_env_health = sum(hub.environmental_health for hub in self.hubs) / len(self.hubs)
        avg_sustainability = sum(hub.sustainability_practices for hub in self.hubs) / len(self.hubs)
        total_population = sum(hub.population for hub in self.hubs)
        for resource in self.global_resources:
            regeneration_rate = 0.002 * (avg_env_health / 100) * (1 + avg_sustainability / 200)
            consumption_rate = 0.001 * (total_population / self.initial_total_population)
            net_rate = regeneration_rate - consumption_rate
            self.global_resources[resource] *= (1 + net_rate)
            self.global_resources[resource] = max(self.global_resources[resource], self.initial_global_resources[resource] * 0.1)

    def inter_hub_resource_sharing(self):
        for resource in self.global_resources:
            total_resource = sum(hub.resources[resource] for hub in self.hubs)
            avg_resource = total_resource / len(self.hubs)
            for hub in self.hubs:
                if hub.resources[resource] < avg_resource:
                    deficit = avg_resource - hub.resources[resource]
                    for donor_hub in self.hubs:
                        if donor_hub.resources[resource] > avg_resource:
                            donation = min(deficit, (donor_hub.resources[resource] - avg_resource) * 0.2)
                            hub.resources[resource] += donation
                            donor_hub.resources[resource] -= donation
                            deficit -= donation
                            if deficit <= 0:
                                break

    def knowledge_transfer(self):
        best_practices = max(self.hubs, key=lambda h: h.sustainability_practices).sustainability_practices
        for hub in self.hubs:
            if hub.sustainability_practices < best_practices:
                hub.sustainability_practices += (best_practices - hub.sustainability_practices) * 0.1