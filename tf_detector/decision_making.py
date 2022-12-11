_MAX_SPEED = 20 #km/h


_DESICION_TABLE = {
    "free": "0",
    "brake": "1",
    "5kph": "2",
    "10kph": "3",
    "15kph": "4",
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
            return "15kph", _DESICION_TABLE["15kph"]
        elif danger_area == 2:
            return "15kph", _DESICION_TABLE["15kph"]
        else:
            return "10kph", _DESICION_TABLE["10kph"]
    elif speed > 10 and speed <= 15:
        if danger_area == 1:
            return "10kph", _DESICION_TABLE["10kph"]
        elif danger_area == 2:
            return "10kph", _DESICION_TABLE["10kph"]
        else:
            return "10kph", _DESICION_TABLE["5kph"]
    elif speed <= 10:
        if danger_area == 1:
            return "brake", _DESICION_TABLE["brake"]
        elif danger_area == 2:
            return "5kph", _DESICION_TABLE["5kph"]
        else:
            return "free", _DESICION_TABLE["free"]
    return "free", _DESICION_TABLE["free"]
