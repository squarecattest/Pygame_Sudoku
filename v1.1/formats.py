from time import time, localtime

def save_format(save: dict, index: int):
    '''
    "original": `list[list[int * 9] * 9]`

    "inputs": `list[list[int, int, int]]`

    "undos": `list[list[tuple[int, int], int, bool]]`

    "moves": `int`

    "used_hints": `int`

    "time": `float`

    "guesses": `list[list[int, int]]`
    '''
    if not isinstance(save, dict): return None
    original = save.get("original")
    fixed = []
    if not isinstance(original, list) or not len(original) == 9: return None
    for i in range(9):
        if not isinstance(original[i], list) or not len(original[i]) == 9: return None
        for j in range(9):
            if not isinstance(original[i][j], int) or not 0 <= original[i][j] <= 9: return None
            if original[i][j]: fixed.append((i, j))
    inputs = save.get("inputs")
    if not isinstance(inputs, list): return None
    for input in inputs:
        if not isinstance(input, list) or not len(input) == 3: return None
        i, j, num = input
        if not isinstance(i, int) or not isinstance(j, int) or not isinstance(num, int) \
            or not 0 <= i <= 8 or not 0 <= j <= 8 or (i, j) in fixed or not 1 <= num <= 9:
            return None
    undos = save.get("undos")
    if not isinstance(undos, list): return None
    for undo in undos:
        if not isinstance(undo, list) or not len(undo) == 3: return None
        block, num, reverse = undo
        if not isinstance(block, list) or not len(block) == 2 or not isinstance(block[0], int) \
            or not isinstance(block[1], int) or not 0 <= block[0] <= 8 or not 0 <= block[1] <= 8 \
            or ((not isinstance(num, int) or not 0 <= num <= 9) and num != None)  \
            or not isinstance(reverse, bool) or tuple(block) in fixed: return None
        undo[0] = tuple(block)
    moves = save.get("moves")
    if not isinstance(moves, int) or not moves >= 0: return None
    used_hints = save.get("used_hints")
    if not isinstance(used_hints, int) or not used_hints >= 0: return None
    gametime = save.get("time")
    if not isinstance(gametime, (int, float)) or gametime > time(): return None
    guesses = save.get("guesses")
    if not isinstance(guesses, list): return None
    for guess in guesses:
        if not isinstance(guess, list) or not len(guess) == 2: return None
        i, j = guess
        if not isinstance(i, int) or not isinstance(j, int) or not 0 <= i <= 8 or not 0 <= j <= 8:
            return None
    guesses = [tuple(guess) for guess in guesses]

    save.update({"difficulty": index + 1})
    save.update({"fixed": fixed})
    save.update({"undos": undos})
    save.update({"guesses": guesses})
    return save

def log_format(log: dict):
    '''
    "difficulty": `Literal[1, 2, 3]`
    "game_time": `int`
    "time": `int | float`
    "moves": `int`
    '''
    if not isinstance(log, dict): return None
    difficulty = log.get("difficulty")
    if not difficulty in [1, 2, 3]: return None
    game_time = log.get("game_time")
    if not isinstance(game_time, int) or not game_time >= 0: return None
    date_time = log.get("time")
    if not isinstance(date_time, (int, float)) or not date_time >= 0: return None
    moves = log.get("moves")
    if not isinstance(moves, int) or not moves > 0: return None

    difficulty = ["Easy", "Normal", "Hard"][difficulty - 1]
    if game_time < 6000:
        game_time = f"{game_time // 60:02}:{game_time % 60:02}"
    else:
        game_time = "99:59"
    date_time = localtime(date_time)
    date_time = f"{date_time.tm_year}-{date_time.tm_mon:02}-{date_time.tm_mday:02} {date_time.tm_hour:02}:{date_time.tm_min:02}"
    moves = f"{moves:03}"
    return (difficulty, game_time, moves, date_time)

def settings_format(settings: dict | None):
    '''
    "volumn_BGM": `int`, 0~100
    "volumn_SE": `int`, 0~100
    "night_mode": `bool`
    "snow_type": `int`, 0~2
    '''
    default = (100, 100, False, 1) # {"volume_BGM": 100, "volumn_SE": 100, "night_mode": False, "snow_type": 1}
    if not isinstance(settings, dict): return default
    volumn_BGM = settings.get("volumn_BGM")
    if not isinstance(volumn_BGM, int) or not 0 <= volumn_BGM <= 100:
        volumn_BGM = default[0]
    volumn_SE = settings.get("volumn_SE")
    if not isinstance(volumn_SE, int) or not 0 <= volumn_SE <= 100:
        volumn_SE = default[1]
    night_mode = settings.get("night_mode")
    if not isinstance(night_mode, bool):
        night_mode = default[2]
    snow_type = settings.get("snow_type")
    if not isinstance(snow_type, int) or not 0 <= snow_type <= 2:
        snow_type = default[3]
    return (volumn_BGM, volumn_SE, night_mode, snow_type)