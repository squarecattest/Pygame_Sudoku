from pygame import Surface

def default(screen: Surface, object: Surface, pos: tuple[int]):
    screen.blit(object, pos)

def center(screen: Surface, object: Surface, center: tuple[int]):
    size = object.get_size()
    pos = (center[0] - (size[0] + 1) // 2, center[1] - (size[1] + 1) // 2)
    screen.blit(object, pos)
    
def left(screen: Surface, object: Surface, left_center: tuple[int]):
    size = object.get_size()
    pos = (left_center[0], left_center[1] - (size[1] + 1) // 2)
    screen.blit(object, pos)

def right(screen: Surface, object: Surface, right_center: tuple[int]):
    size = object.get_size()
    pos = (right_center[0] - size[0], right_center[1] - (size[1] + 1) // 2)
    screen.blit(object, pos)

def in_centered_object(pos: tuple[int], object: Surface, center: tuple[int]):
    size = object.get_size()
    if center[0] - (size[0] + 1) // 2 <= pos[0] <= center[0] + (size[0] - 3) // 2 \
        and center[1] - (size[1] + 1) // 2 <= pos[1] <= center[1] + (size[1] - 3) // 2:
        return True
    return False

def in_left_centered_object(pos: tuple[int], object: Surface, left_center: tuple[int]):
    size = object.get_size()
    if left_center[0] <= pos[0] <= left_center[0] + size[0] - 1 \
        and left_center[1] - (size[1] + 1) // 2 <= pos[1] <= left_center[1] + (size[1] - 3) // 2:
        return True
    return False

def in_right_centered_object(pos: tuple[int], object: Surface, right_center: tuple[int]):
    size = object.get_size()
    if right_center[0] - size[0] + 1 <= pos[0] <= right_center[0] \
        and right_center[1] - (size[1] + 1) // 2 <= pos[1] <= right_center[1] + (size[1] - 3) // 2:
        return True
    return False