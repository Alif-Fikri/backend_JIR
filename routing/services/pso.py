import numpy as np
from typing import List, Dict, Tuple
import random

class Particle:
    def __init__(self, bounds):
        self.position = np.array([
            random.uniform(bounds[0][0], bounds[0][1]), 
            random.uniform(bounds[1][0], bounds[1][1])   
        ])
        self.velocity = np.array([0.0, 0.0])
        self.best_position = self.position.copy()
        self.best_score = float('inf')

class PSO:
    def __init__(self, 
                 start: Tuple[float, float], 
                 end: Tuple[float, float],
                 flood_data: List[Dict],
                 n_particles: int = 30,
                 max_iter: int = 100,
                 w: float = 0.5,
                 c1: float = 0.8,
                 c2: float = 0.9):
        
        self.start = np.array(start)
        self.end = np.array(end)
        self.flood_data = flood_data
        self.n_particles = n_particles
        self.max_iter = max_iter
        self.w = w
        self.c1 = c1
        self.c2 = c2

        min_lat = min(start[0], end[0])
        max_lat = max(start[0], end[0])
        min_lon = min(start[1], end[1])
        max_lon = max(start[1], end[1])
        
        # area pencarian diperluas 20%
        lat_range = max_lat - min_lat
        lon_range = max_lon - min_lon
        self.bounds = [
            (min_lat - 0.2*lat_range, max_lat + 0.2*lat_range),
            (min_lon - 0.2*lon_range, max_lon + 0.2*lon_range)
        ]
        
        self.particles = [Particle(self.bounds) for _ in range(n_particles)]
        self.global_best_position = None
        self.global_best_score = float('inf')

    def flood_penalty(self, position: np.array) -> float:
        penalty = 0.0
        for flood in self.flood_data:
            try:
                flood_pos = np.array([float(flood["LATITUDE"]), float(flood["LONGITUDE"])])
                distance = np.linalg.norm(position - flood_pos)
                
                if distance < 0.01:
                    status_weight = int(flood["STATUS_SIAGA"]) + 1
                    penalty += (1000 / distance) * status_weight
            except (ValueError, TypeError):
                continue
        return penalty
    
    def fitness(self, position: np.array) -> float:
        # fungsi fitness untuk eval partikel
        start_dist = np.linalg.norm(position - self.start)
        end_dist = np.linalg.norm(self.end - position)
        total_distance = start_dist + end_dist
        flood_penalty = self.flood_penalty(position)
        return total_distance + flood_penalty
    
    def optimize(self) -> Tuple[float, float]:
        for _ in range(self.max_iter):
            for particle in self.particles:
                # eval fitness
                score = self.fitness(particle.position)
    
                # update pbest
                if score < particle.best_score:
                    particle.best_score = score
                    particle.best_position = particle.position.copy()
                
                # update gbest
                if score < self.global_best_score:
                    self.global_best_score = score
                    self.global_best_position = particle.position.copy()
            
            for particle in self.particles:
                # komponen inersia
                inertia = self.w * particle.velocity
                # komponen kognitif
                r1 = random.random()
                cognitive = self.c1 * r1 * (particle.best_position - particle.position)
                # komponen sosial
                r2 = random.random()
                social = self.c2 * r2 * (self.global_best_position - particle.position)
                # kecepatan
                particle.velocity = inertia + cognitive + social
                # posisi
                particle.position += particle.velocity

                for i in range(2):
                    if particle.position[i] < self.bounds[i][0]:
                        particle.position[i] = self.bounds[i][0]
                    if particle.position[i] > self.bounds[i][1]:
                        particle.position[i] = self.bounds[i][1]
        
        return tuple(self.global_best_position)

def calculate_waypoints(start: Tuple[float, float], 
                        end: Tuple[float, float], 
                        flood_data: List[Dict],
                        n_waypoints: int = 3) -> List[Tuple[float, float]]:
    waypoints = []
    
    # untuk setiap waypoint, PSOnya running
    for _ in range(n_waypoints):
        pso = PSO(
            start=start,
            end=end,
            flood_data=flood_data,
            n_particles=50,
            max_iter=100
        )
        waypoint = pso.optimize()
        waypoints.append(waypoint)
        start = waypoint
    
    return waypoints