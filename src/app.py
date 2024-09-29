#!/usr/bin/env python3

import pygame
import datetime

from pygame import Vector2
import random
from convex_hull import quick_hull, jarvis_march, graham_scan


def take_screenshot(surface):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    pygame.image.save(surface, filename)
    print(f"Screenshot saved as {filename}")
    
    
def gift_wrapping(points:list) -> list:
    hull = []
    
    # most left point
    start_point = min(points)
    hull.append(start_point)
    
    # find the next most left point them the last point in hull
    while True:
        maybe_next = random.choice(points)
        if start_point == maybe_next:
            continue
        
        for point in points:
            # check if point is "more" left than the maybe_nexr point
            if (Vector2(maybe_next) - Vector2(start_point)).cross(Vector2(point) - Vector2(start_point)) < 0:
                maybe_next = point
        
        hull.append(maybe_next)
        if maybe_next == hull[0]: break
        start_point = maybe_next
    
    return hull 


def main():
    pygame.init()

    window_dimensions = width, height = 1800, 900
    max_points = 50
    points = [(random.randrange(width), random.randrange(height)) for _ in range(max_points)]

    surface = pygame.display.set_mode(window_dimensions)
    pygame.display.set_caption("Pygame App")
    surface.fill('white')

    running = True

    while running:
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q: running = False
                    case pygame.K_SPACE: take_screenshot(surface)
                    
        # background
        surface.fill("black")
        
        # draw points
        for point in points:
            pygame.draw.circle(surface, "white", point, 5)
            
        # hull_points
        # quick_hull, jarvis_march, graham_scan
        hull_points = gift_wrapping(points)
        for point in hull_points:
            pygame.draw.circle(surface, "red", point, 10)
            
        pygame.draw.lines(surface, "red", True, hull_points, 2)
                    
        # App
        pygame.display.flip()


if __name__ == "__main__":
    main()
