import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
from collaborative_stewardship import CollaborativeStewardship

try:
    from tqdm import tqdm
    use_tqdm = True
except ImportError:
    use_tqdm = False
    print("tqdm library not found. Progress bar will not be shown.")

def run_simulation(params):
    total_population, num_hubs, num_days = map(int, params)
    society = CollaborativeStewardship(total_population, num_hubs)
    results = society.simulate(num_days)
    
    avg_final_happiness = np.mean([data["happiness"][-1] for data in results.values()])
    total_final_resources = sum(sum(hub.resources.values()) for hub in society.hubs)
    avg_environmental_health = np.mean([data["environmental_health"][-1] for data in results.values()])
    avg_sustainability = np.mean([data["sustainability_practices"][-1] for data in results.values()])
    
    return -(avg_final_happiness + total_final_resources * 0.01 + avg_environmental_health + avg_sustainability)

def optimize_and_run(total_population):
    bounds = [(total_population, total_population), (2, 20), (30, 3650)]  # (total_population, num_hubs, num_days)
    
    def callback(xk, convergence):
        print(f"Current best: Hubs = {int(xk[1])}, Days = {int(xk[2])}, Objective = {-run_simulation(xk):.2f}")

    print("Optimizing parameters...")
    result = differential_evolution(run_simulation, bounds, maxiter=10, popsize=5, callback=callback)
    
    optimized_params = list(map(int, result.x))
    print(f"\nOptimized parameters: Population = {optimized_params[0]}, Hubs = {optimized_params[1]}, Days = {optimized_params[2]}")
    print(f"Objective function value: {-result.fun:.2f}")

    print("\nRunning final simulation with optimized parameters...")
    society = CollaborativeStewardship(optimized_params[0], optimized_params[1])
    final_results = simulate_with_progress(society, optimized_params[2])

    plot_results(final_results)

def simulate_with_progress(society, num_days):
    if use_tqdm:
        day_range = tqdm(range(num_days), desc="Simulating", unit="day")
    else:
        day_range = range(num_days)
        print(f"Simulating {num_days} days...")

    return society.simulate(num_days)

def plot_results(history):
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(15, 20))

    for hub_name, data in history.items():
        ax1.plot(data["resources"], label=f"{hub_name} Resources")
        ax2.plot(data["happiness"], label=f"{hub_name} Happiness")
        ax3.plot(data["environmental_health"], label=f"{hub_name} Env. Health")
        ax4.plot(data["social_cohesion"], label=f"{hub_name} Social Cohesion")
        ax5.plot(data["population"], label=f"{hub_name} Population")
        ax6.plot(data["sustainability_practices"], label=f"{hub_name} Sustainability")

    ax1.set_title("Total Resources Over Time")
    ax1.set_xlabel("Days")
    ax1.set_ylabel("Total Resources")
    ax1.legend()

    ax2.set_title("Happiness Over Time")
    ax2.set_xlabel("Days")
    ax2.set_ylabel("Happiness")
    ax2.legend()

    ax3.set_title("Environmental Health Over Time")
    ax3.set_xlabel("Days")
    ax3.set_ylabel("Environmental Health")
    ax3.legend()

    ax4.set_title("Social Cohesion Over Time")
    ax4.set_xlabel("Days")
    ax4.set_ylabel("Social Cohesion")
    ax4.legend()

    ax5.set_title("Population Over Time")
    ax5.set_xlabel("Days")
    ax5.set_ylabel("Population")
    ax5.legend()

    ax6.set_title("Sustainability Practices Over Time")
    ax6.set_xlabel("Days")
    ax6.set_ylabel("Sustainability Practices")
    ax6.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    total_population = int(input("Enter the total population for the simulation: "))
    optimize_and_run(total_population)