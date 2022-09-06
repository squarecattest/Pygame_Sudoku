from pygame import Surface

def default(screen: Surface, object: Surface, top_left: tuple[int]):
    screen.blit(object, top_left)

def abs(screen: Surface, object: Surface, center: tuple[int]):
    object_size = object.get_size()
    screen.blit(object, (center[0] - (object_size[0] + 1) // 2, center[1] - (object_size[1] + 1) // 2))

def scale(screen: Surface, object: Surface, scale: tuple[float]):
    '''
    Align the object at the scale, which is (0.0, 0.0) at top-left and (1.0, 1.0) at bottom-right.
    '''
    screen_size = screen.get_size()
    center = (int(screen_size[0] * scale[0]), int(screen_size[1] * scale[1]))
    abs(screen, object, center)

def rel_center(screen: Surface, object: Surface, shift: tuple[int]):
    '''
    If shift is (0, 0), the object will align at center of the screen.
    '''
    screen_size = screen.get_size()
    abs(screen, object, (screen_size[0] // 2 + shift[0], screen_size[1] // 2 + shift[1]))

def rel_left(screen: Surface, object: Surface, shift: tuple[int]):
    '''
    If shift is (0, 0), the object's left side will align with the screen's left side.
    '''
    screen_size = screen.get_size()
    object_size = object.get_size()
    abs(screen, object, ((object_size[0] + 1) // 2 + shift[0], screen_size[1] // 2 + shift[1]))

def rel_right(screen: Surface, object: Surface, shift: tuple[int]):
    '''
    If shift is (0, 0), the object's right side will align with the screen's right side.
    '''
    screen_size = screen.get_size()
    object_size = object.get_size()
    abs(screen, object, (screen_size[0] - object_size[0] // 2 + shift[0], screen_size[1] // 2 + shift[1]))

def rel_top(screen: Surface, object: Surface, shift: tuple[int]):
    '''
    If shift is (0, 0), the object's top side will align with the screen's top side.
    '''
    screen_size = screen.get_size()
    object_size = object.get_size()
    abs(screen, object, (screen_size[0] // 2 + shift[0], (object_size[1] + 1) // 2 + shift[1]))

def rel_bottom(screen: Surface, object: Surface, shift: tuple[int]):
    '''
    If shift is (0, 0), the object's bottom side will align with the screen's bottom side.
    '''
    screen_size = screen.get_size()
    object_size = object.get_size()
    abs(screen, object, (screen_size[0] // 2 + shift[0], screen_size[1] - object_size[1] // 2 + shift[1]))

def in_default_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], top_left: tuple[int]):
    if top_left[0] <= pos[0] < top_left[0] + object_size[0] \
        and top_left[1] <= pos[1] < top_left[1] + object_size[1]:
        return True
    return False

def in_abs_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], center: tuple[int]):
    if center[0] - (object_size[0] + 1) // 2 <= pos[0] < center[0] + object_size[0] // 2 \
        and center[1] - (object_size[1] + 1) // 2 <= pos[1] < center[1] + object_size[1] // 2:
        return True
    return False

def in_scaled_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], scale: tuple[float]):
    center = (int(screen_size[0] * scale[0]), int(screen_size[1] * scale[1]))
    return in_abs_object(screen_size, pos, object_size, center)

def in_rel_center_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], shift: tuple[int]):
    center = (screen_size[0] // 2 + shift[0], screen_size[1] // 2 + shift[1])
    return in_abs_object(screen_size, pos, object_size, center)

def in_rel_left_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], shift: tuple[int]):
    center = ((object_size[0] + 1) // 2 + shift[0], screen_size[1] // 2 + shift[1])
    return in_abs_object(screen_size, pos, object_size, center)

def in_rel_right_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], shift: tuple[int]):
    center = (screen_size[0] - object_size[0] // 2 + shift[0], screen_size[1] // 2 + shift[1])
    return in_abs_object(screen_size, pos, object_size, center)

def in_rel_top_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], shift: tuple[int]):
    center = (screen_size[0] // 2 + shift[0], (object_size[1] + 1) // 2 + shift[1])
    return in_abs_object(screen_size, pos, object_size, center)

def in_rel_bottom_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], shift: tuple[int]):
    center = (screen_size[0] // 2 + shift[0], screen_size[1] - object_size[1] // 2 + shift[1])
    return in_abs_object(screen_size, pos, object_size, center)

def scale_of_default_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], top_left: tuple[int]):
    return (pos[0] - top_left[0]) / object_size[0], (pos[1] - top_left[1]) / object_size[1]

def scale_of_abs_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], center: tuple[int]):
    return scale_of_default_object(screen_size, pos, object_size,
        (center[0] - (object_size[0] + 1) // 2, center[1] - (object_size[1] + 1) // 2)
    )

def scale_of_scaled_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], scale: tuple[float]):
    return scale_of_abs_object(screen_size, pos, object_size,
        (int(screen_size[0] * scale[0]), int(screen_size[1] * scale[1]))
    )

def scale_of_rel_center_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], shift: tuple[int]):
    return scale_of_abs_object(screen_size, pos, object_size, 
        (screen_size[0] // 2 + shift[0], screen_size[1] // 2 + shift[1])
    )

def scale_of_rel_left_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], shift: tuple[int]):
    return scale_of_abs_object(screen_size, pos, object_size,
        ((object_size[0] + 1) // 2 + shift[0], screen_size[1] // 2 + shift[1])
    )

def scale_of_rel_right_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], shift: tuple[int]):
    return scale_of_abs_object(screen_size, pos, object_size,
        (screen_size[0] - object_size[0] // 2 + shift[0], screen_size[1] // 2 + shift[1])
    )

def scale_of_rel_top_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], shift: tuple[int]):
    return scale_of_abs_object(screen_size, pos, object_size,
        (screen_size[0] // 2 + shift[0], (object_size[1] + 1) // 2 + shift[1])
    )

def scale_of_rel_bottom_object(screen_size: tuple[int], pos: tuple[int], object_size: tuple[int], shift: tuple[int]):
    return scale_of_abs_object(screen_size, pos, object_size,
        (screen_size[0] // 2 + shift[0], screen_size[1] - object_size[1] // 2 + shift[1])
    )

def pos_to_shift(screen_size: tuple[int], pos: tuple[int]):
    return (pos[0] - screen_size[0] // 2, pos[1] - screen_size[1] // 2)

def shift_to_pos(screen_size: tuple[int], shift: tuple[int]):
    return (screen_size[0] // 2 + shift[0], screen_size[1] // 2 + shift[1])

def pos_to_scale(screen_size: tuple[int], pos: tuple[int]):
    return (pos[0] / screen_size[0], pos[1] / screen_size[1])

def scale_to_pos(screen_size: tuple[int], scale: tuple[float]):
    return (int(screen_size[0] * scale[0]), int(screen_size[1] * scale[1]))

def shift_to_scale(screen_size: tuple[int], shift: tuple[int]):
    return pos_to_scale(screen_size, shift_to_pos(screen_size, shift))

def scale_to_shift(screen_size: tuple[int], scale: tuple[float]):
    return pos_to_shift(screen_size, scale_to_pos(screen_size, scale))