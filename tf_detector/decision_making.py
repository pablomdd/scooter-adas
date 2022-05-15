
_MAX_SPEED = 20 #km/h


_DESICION_TABLE = {
    25: "down20",
    20: "down15",
    15: "down10",
    10: "down5",
    5: "down5",
    0: "brake"
}

def make(danger_area: int=1, speed: float=10) -> str:
    """Receives speed and detected object danger area.
    Decides what preventive action to take based on the DECISION_TABLE.

    Args:
        danger_area:int 1-3 
        speed: float
    """
    if speed > 15:
        if danger_area == 1:
            return _DESICION_TABLE[20]
        elif danger_area == 2:
            return _DESICION_TABLE[20]
        else:
            return _DESICION_TABLE[15]
    elif speed > 10 and speed <= 15:
        if danger_area == 1:
            return _DESICION_TABLE[15]
        elif danger_area == 2:
            return _DESICION_TABLE[15]
        else:
            return _DESICION_TABLE[10]
    elif speed <= 10:
        if danger_area == 1:
            return _DESICION_TABLE[0]
        elif danger_area == 2:
            return _DESICION_TABLE[5]
        else:
            return _DESICION_TABLE[10]
    return "none"