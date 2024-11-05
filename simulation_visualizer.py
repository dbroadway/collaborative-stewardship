import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def run_with_visualization(society, num_days):
    """
    Run simulation with live plotting
    """
    # Set up the figure and subplots with extra space for title
    plt.style.use('default')
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])
    
    fig.suptitle('Collaborative Stewardship Simulation', fontsize=16, y=0.95)
    
    # Initialize data storage
    data = {hub.name: {
        'resources': [],
        'happiness': [],
        'environmental_health': [],
        'population': []
    } for hub in society.hubs}
    
    # Initialize lines for each hub
    lines = {}
    hub_names = [hub.name for hub in society.hubs]
    colors = plt.cm.tab20(np.linspace(0, 1, len(hub_names)))
    
    # Create lines for each metric and hub
    for hub_name, color in zip(hub_names, colors):
        lines[hub_name] = {
            'resources': ax1.plot([], [], label=hub_name, color=color)[0],
            'happiness': ax2.plot([], [], label=hub_name, color=color)[0],
            'environmental': ax3.plot([], [], label=hub_name, color=color)[0],
            'population': ax4.plot([], [], label=hub_name, color=color)[0]
        }
    
    # Set up the axes
    ax1.set_title('Resources')
    ax2.set_title('Happiness')
    ax3.set_title('Environmental Health')
    ax4.set_title('Population')
    
    for ax in [ax1, ax2, ax3, ax4]:
        ax.set_xlabel('Days')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    def init():
        # Initialize empty lines
        for hub_lines in lines.values():
            for line in hub_lines.values():
                line.set_data([], [])
        return [line for hub_lines in lines.values() for line in hub_lines.values()]
    
    def update(frame):
        # Run one day of simulation
        for hub in society.hubs:
            hub.produce(society.global_resources)
            hub.consume()
            hub.update_population()
            hub.plan_long_term()
            
            # Store the day's data
            data[hub.name]['resources'].append(sum(hub.resources.values()))
            data[hub.name]['happiness'].append(hub.happiness)
            data[hub.name]['environmental_health'].append(hub.environmental_health)
            data[hub.name]['population'].append(hub.population)
        
        society.inter_hub_resource_sharing()
        society.knowledge_transfer()
        
        # Update the plots
        for hub_name in hub_names:
            x = list(range(len(data[hub_name]['resources'])))
            lines[hub_name]['resources'].set_data(x, data[hub_name]['resources'])
            lines[hub_name]['happiness'].set_data(x, data[hub_name]['happiness'])
            lines[hub_name]['environmental'].set_data(x, data[hub_name]['environmental_health'])
            lines[hub_name]['population'].set_data(x, data[hub_name]['population'])
        
        # Adjust axis limits
        for ax in [ax1, ax2, ax3, ax4]:
            ax.relim()
            ax.autoscale_view()
        
        # Print progress
        if frame % 100 == 0:
            print(f"Day {frame} of {num_days}")
        
        return [line for hub_lines in lines.values() for line in hub_lines.values()]
    
    # Create animation
    anim = FuncAnimation(
        fig, 
        update,
        init_func=init,
        frames=num_days,
        interval=1,  # Update every 1ms for faster simulation
        blit=True
    )
    
    plt.show()
    
    return data