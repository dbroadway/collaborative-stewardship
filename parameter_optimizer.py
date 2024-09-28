from collaborative_stewardship import CollaborativeStewardship
from scipy.optimize import differential_evolution
import numpy as np
import argparse

def objective_function(params):
    num_hubs, num_days = int(params[0]), int(params[1])
    society = CollaborativeStewardship(num_hubs)
    results = society.simulate(num_days)
    
    total_happiness = sum(data["happiness"][-1] for data in results.values())
    total_resources = sum(data["resources"][-1] for data in results.values())
    avg_gini = np.mean([data["gini"][-1] for data in results.values()])
    
    return -(total_happiness + total_resources * 0.01 - avg_gini * 1000)

def optimize_parameters(maxiter, popsize):
    bounds = [(2, 10), (30, 730)]  # (num_hubs, num_days)
    result = differential_evolution(objective_function, bounds, maxiter=maxiter, popsize=popsize)
    
    print("Optimized parameters:")
    print(f"Number of hubs: {int(result.x[0])}")
    print(f"Number of days: {int(result.x[1])}")
    print(f"Objective function value: {-result.fun}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimize Collaborative Stewardship simulation parameters")
    parser.add_argument("--maxiter", type=int, default=10, help="Maximum number of iterations for differential evolution")
    parser.add_argument("--popsize", type=int, default=5, help="Population size for differential evolution")
    args = parser.parse_args()

    optimize_parameters(args.maxiter, args.popsize)