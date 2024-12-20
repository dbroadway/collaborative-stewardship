import pygame
import networkx as nx
import random
from scipy.spatial import Voronoi
import numpy as np
from shapely.geometry import Polygon, Point

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Collaborative Stewardship Model")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (50, 80, 120)
LIGHT_BLUE = (100, 150, 200)
DARK_GREEN = (30, 90, 50)
SOFT_YELLOW = (200, 180, 100)
GRAY = (150, 150, 150)
RESOURCE_COLOR = (255, 220, 80)  # Gold for resources

# Fonts
pygame.font.init()
font = pygame.font.SysFont("Arial", 18)

# Create a NetworkX graph for hubs
G = nx.Graph()
num_hubs = 12
positions = {}
regions = [
    "Aurora Valley", "Eclipse Plains", "Verdant Reach", "Azure Coast",
    "Summit Ridge", "Golden Steppe", "Crimson Expanse", "Twilight Basin",
    "Ivory Peaks", "Shadow Glade", "Cobalt Flats", "Emerald Canyon"
]

# Resource packets
packets = []

# Generate Voronoi diagram with screen boundary
def generate_voronoi():
    global vor, points
    # Generate points within screen boundaries
    points = [(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(num_hubs)]
    # Add screen corners as "dummy points" for boundary clipping
    boundary_points = [
        (0, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)
    ]
    vor = Voronoi(points + boundary_points)

# Place hubs inside Voronoi regions
def place_hubs():
    global positions
    positions.clear()

    for i, region_idx in enumerate(vor.point_region[:num_hubs]):
        region = vor.regions[region_idx]

        # Ensure the region is valid (no -1 indices)
        if -1 in region or len(region) == 0:
            continue

        # Construct the polygon for this region
        vertices = [vor.vertices[j] for j in region]
        polygon = Polygon(vertices)

        # Sample a random point within the polygon
        while True:
            # Generate a random point within the bounding box of the polygon
            minx, miny, maxx, maxy = polygon.bounds
            x = random.uniform(minx, maxx)
            y = random.uniform(miny, maxy)
            point = Point(x, y)

            # Check if the point is inside the polygon
            if polygon.contains(point):
                positions[i] = (int(x), int(y))
                break

        # Add the node to the graph
        if i not in G.nodes:
            G.add_node(i)

        # Update node attributes
        G.nodes[i]['region'] = f"Region {i}"
        G.nodes[i]['population'] = random.randint(1000, 50000)
        G.nodes[i]['resources'] = random.randint(50, 200)

# Add edges and initialize resource packets
def add_edges():
    G.clear_edges()
    packets.clear()
    for i in range(num_hubs):
        for j in range(i + 1, num_hubs):
            if random.random() < 0.4:  # 40% chance of connection
                G.add_edge(i, j, resource_flow=random.randint(2, 8))
                initialize_packets(i, j)

# Initialize resource packets between hubs
def initialize_packets(start, end):
    for _ in range(G.edges[start, end]['resource_flow']):
        packets.append({
            "start": start,
            "end": end,
            "progress": random.uniform(0, 1),  # Start at a random position along the line
            "direction": 1
        })

# Draw Voronoi regions and clip to the screen
def draw_voronoi():
    for region in vor.regions:
        if -1 not in region and len(region) > 0:
            polygon = [clip_to_screen(vor.vertices[i]) for i in region]
            if is_polygon_on_screen(polygon):
                pygame.draw.polygon(screen, DARK_GREEN, polygon, 0)
                pygame.draw.polygon(screen, GRAY, polygon, 2)

# Clip points to stay on the screen
def clip_to_screen(point):
    x = min(max(point[0], 0), WIDTH)
    y = min(max(point[1], 0), HEIGHT)
    return (x, y)

# Check if polygon is on screen
def is_polygon_on_screen(polygon):
    for x, y in polygon:
        if 0 <= x <= WIDTH and 0 <= y <= HEIGHT:
            return True
    return False

# Draw edges
def draw_edges():
    for edge in G.edges:
        x1, y1 = positions[edge[0]]
        x2, y2 = positions[edge[1]]
        pygame.draw.line(screen, GRAY, (int(x1), int(y1)), (int(x2), int(y2)), 2)

# Draw hubs
def draw_hubs():
    for node, (x, y) in positions.items():
        population = G.nodes[node]['population']
        radius = max(10, min(population // 1000, 50))  # Scale hub size based on population
        color = DARK_BLUE if population > 25000 else LIGHT_BLUE if population > 10000 else SOFT_YELLOW
        pygame.draw.circle(screen, color, (int(x), int(y)), radius)
        pygame.draw.circle(screen, GRAY, (int(x), int(y)), radius + 2, 2)  # Outer glow

        # Display region name
        text = font.render(G.nodes[node]['region'], True, WHITE)
        screen.blit(text, (x - 40, y - radius - 20))
        # Display population
        pop_text = font.render(f"Pop: {population}", True, LIGHT_BLUE)
        screen.blit(pop_text, (x - 30, y + radius + 5))

# Update and draw packets
def update_and_draw_packets():
    for packet in packets:
        start = positions[packet["start"]]
        end = positions[packet["end"]]
        
        # Calculate current position along the line
        progress = packet["progress"]
        x = start[0] + (end[0] - start[0]) * progress
        y = start[1] + (end[1] - start[1]) * progress

        # Draw packet
        pygame.draw.circle(screen, RESOURCE_COLOR, (int(x), int(y)), 5)

        # Update progress
        packet["progress"] += 0.005 * packet["direction"]  # Speed of packets
        if packet["progress"] >= 1.0 or packet["progress"] <= 0.0:
            packet["direction"] *= -1  # Reverse direction at endpoints

# Main simulation loop
def main():
    global WIDTH, HEIGHT, screen
    running = True
    clock = pygame.time.Clock()

    generate_voronoi()
    place_hubs()
    add_edges()

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                generate_voronoi()
                place_hubs()
                add_edges()

        # Draw everything
        draw_voronoi()
        draw_edges()
        draw_hubs()
        update_and_draw_packets()

        # Refresh the screen
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
