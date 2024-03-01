from dolphin import memory

# Memory locations of required values, found using Dolphin Memory Engine
# https://github.com/aldelaro5/Dolphin-memory-engine

SPEED_LOCATION = 0x80E4C8B8
RACE_COMPLETION_LOCATION = 0x80E43748
MT_LOCATION = 0x80E4C796

# Returns the current speed of the kart
def getCurrentSpeed() -> float:
    return round(memory.read_f32(SPEED_LOCATION), 3)

# Returns the value of the players current race completion (Race%)
def getCurrentRaceCompletion() -> float:
    return round(memory.read_f32(RACE_COMPLETION_LOCATION), 4)

# Returns the value of the player's current miniturbo charge (MT)
def getCurrentMT() -> int:
    return memory.read_u16(MT_LOCATION)
    
# Returns a tuple of the Speed, Race% and MT
def getRaceInfo() -> tuple:
    return getCurrentSpeed(), getCurrentRaceCompletion(), getCurrentMT()

def printRaceInfo():
    print(f'MT: {getCurrentMT()}')
    print(f'Race%: {getCurrentRaceCompletion()}')
    print(f'Speed: {getCurrentSpeed()}')

#event.on_frameadvance(printRaceInfo)