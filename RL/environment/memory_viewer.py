from dolphin import memory

# Memory locations of required values, found using Dolphin Memory Engine
# https://github.com/aldelaro5/Dolphin-memory-engine

RACE_COMPLETION_LOCATION = 0x80E43708
MT_LOCATION = 0x80E4C756
SPEED_LOCATION = 0x80E4C678

# Returns the current speed of the kart
def getCurrentSpeed() -> float:
    return round(memory.read_f32(SPEED_LOCATION), 3)

# Returns the value of the players current race completion (Race%)
def getCurrentRaceCompletion() -> float:
    return round(memory.read_f32(RACE_COMPLETION_LOCATION), 3)

# Returns the value of the player's current miniturbo charge (MT)
def getCurrentMT() -> int:
    return memory.read_u16(MT_LOCATION)
    
# Returns a tuple of the Speed, Race% and MT
def getRaceInfo() -> (float, float, int):
    return getCurrentSpeed(), getCurrentRaceCompletion(), getCurrentMT()

def printRaceInfo():
    print(f'MT: {getCurrentMT()}')
    print(f'Race%: {getCurrentRaceCompletion()}')
    print(f'Speed: {getCurrentSpeed()}')

#event.on_frameadvance(printRaceInfo)