

def check_overlap(box1, box2):
    
    x1_a, y1_a, x2_a, y2_a = box1
    x1_b, y1_b, x2_b, y2_b = box2
    
    # Check if boxes intersect
    if x1_a > x2_b or x2_a < x1_b or y1_a > y2_b or y2_a < y1_b:
        return False
    return True


def point_in_box(point, box):
    
    px, py = point
    x1, y1, x2, y2 = box
    return x1 <= px <= x2 and y1 <= py <= y2
