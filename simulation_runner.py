import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
from collaborative_stewardship import CollaborativeStewardship
import sys

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

def visualize_sustainability(history):
    """
    Create visualizations demonstrating system sustainability
    """
    plt.style.use('default')
    
    # Create a 2x2 subplot layout
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('System Sustainability Analysis', fontsize=16, y=0.95)
    
    # Color palette for different hubs
    colors = plt.cm.viridis(np.linspace(0, 0.8, len(history)))
    
    # 1. Resource Sustainability
    for (hub_name, data), color in zip(history.items(), colors):
        resources = data['resources']
        ax1.plot(resources, color=color, alpha=0.6, label=hub_name)
        # Add trend line
        z = np.polyfit(range(len(resources)), resources, 1)
        p = np.poly1d(z)
        ax1.plot(p(range(len(resources))), '--', color=color, alpha=0.3)
    
    ax1.set_title('Resource Stability Over Time')
    ax1.set_xlabel('Days')
    ax1.set_ylabel('Total Resources')
    ax1.grid(True, alpha=0.3)
    
    # 2. Happiness Levels
    for (hub_name, data), color in zip(history.items(), colors):
        ax2.plot(data['happiness'], color=color, alpha=0.6, label=hub_name)
    
    ax2.set_title('Community Happiness')
    ax2.set_xlabel('Days')
    ax2.set_ylabel('Happiness Level')
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)
    
    # 3. Environmental Health
    for (hub_name, data), color in zip(history.items(), colors):
        ax3.plot(data['environmental_health'], color=color, alpha=0.6, label=hub_name)
    
    ax3.set_title('Environmental Health')
    ax3.set_xlabel('Days')
    ax3.set_ylabel('Health Level')
    ax3.set_ylim(0, 100)
    ax3.grid(True, alpha=0.3)
    
    # 4. Population Stability
    for (hub_name, data), color in zip(history.items(), colors):
        ax4.plot(data['population'], color=color, alpha=0.6, label=hub_name)
    
    ax4.set_title('Population Stability')
    ax4.set_xlabel('Days')
    ax4.set_ylabel('Population')
    ax4.grid(True, alpha=0.3)
    
    # Add overall legend
    lines, labels = ax1.get_legend_handles_labels()
    fig.legend(lines, labels, loc='center right', bbox_to_anchor=(0.98, 0.5))
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    
    # Add sustainability analysis text
    sustainability_metrics = analyze_sustainability(history)
    fig.text(0.02, 0.02, sustainability_metrics, fontsize=10, 
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    plt.show()

def analyze_sustainability(history):
    """Calculate key sustainability metrics"""
    
    # Calculate metrics across all hubs
    final_days = {metric: [] for metric in ['happiness', 'environmental_health', 'resources', 'population']}
    stability = {metric: [] for metric in ['happiness', 'environmental_health', 'resources', 'population']}
    
    for hub_data in history.values():
        for metric in final_days:
            if metric in hub_data:
                # Get final value
                final_days[metric].append(hub_data[metric][-1])
                # Calculate stability (coefficient of variation over last 20% of simulation)
                last_period = hub_data[metric][int(len(hub_data[metric])*0.8):]
                stability[metric].append(np.std(last_period) / np.mean(last_period) * 100)
    
    # Create analysis text
    metrics_text = "Sustainability Analysis:\n\n"
    
    # Happiness
    metrics_text += f"Happiness:\n"
    metrics_text += f"  • Final Average: {np.mean(final_days['happiness']):.1f}\n"
    metrics_text += f"  • Stability: {np.mean(stability['happiness']):.1f}% variation\n\n"
    
    # Resources
    metrics_text += f"Resources:\n"
    metrics_text += f"  • Final Average: {np.mean(final_days['resources']):.1f}\n"
    metrics_text += f"  • Stability: {np.mean(stability['resources']):.1f}% variation\n\n"
    
    # Environmental Health
    metrics_text += f"Environmental Health:\n"
    metrics_text += f"  • Final Average: {np.mean(final_days['environmental_health']):.1f}\n"
    metrics_text += f"  • Stability: {np.mean(stability['environmental_health']):.1f}% variation\n\n"
    
    # Population
    metrics_text += f"Population:\n"
    metrics_text += f"  • Final Average: {np.mean(final_days['population']):.1f}\n"
    metrics_text += f"  • Stability: {np.mean(stability['population']):.1f}% variation"
    
    return metrics_text

def optimize_and_run(total_population):
    bounds = [(total_population, total_population), (2, 20), (30, 3650)]
    
    print("Phase 1: Optimizing Parameters")
    print("-" * 50)
    
    def callback(xk, convergence):
        current_hubs = int(xk[1])
        current_days = int(xk[2])
        objective = -run_simulation(xk)
        print(f"Testing: {current_hubs} hubs over {current_days} days | Score: {objective:.2f}")

    result = differential_evolution(
        run_simulation, 
        bounds, 
        maxiter=10, 
        popsize=5, 
        callback=callback,
        updating='deferred'
    )
    
    optimized_params = list(map(int, result.x))
    
    print("\nPhase 2: Optimization Results")
    print("-" * 50)
    print(f"Optimal configuration found:")
    print(f"• Population: {optimized_params[0]:,}")
    print(f"• Number of hubs: {optimized_params[1]}")
    print(f"• Simulation days: {optimized_params[2]:,}")
    print(f"• Fitness score: {-result.fun:.2f}")
    
    print("\nPhase 3: Final Simulation")
    print("-" * 50)
    print("Running optimized simulation with visualization...")
    
    society = CollaborativeStewardship(optimized_params[0], optimized_params[1])
    history = society.simulate(optimized_params[2])
    visualize_sustainability(history)
    return history

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
    if len(sys.argv) > 1:
        try:
            population = int(sys.argv[1])
            if population <= 0:
                print("Population must be positive")
            else:
                history = optimize_and_run(population)
        except ValueError:
            print("Please provide a valid number for population")
    else:
        print("Usage: python simulation_runner.py <population>")
        print("Example: python simulation_runner.py 1000")