from dolphin import memory

# Memory locations of required values, found using Dolphin Memory Engine
# https://github.com/aldelaro5/Dolphin-memory-engine

SPEED_LOCATION = 0x80E4C8B8
RACE_COMPLETION_LOCATION = 0x80E43748
X_POS_LOCATION = 0x80E4DAE8
Z_POS_LOCATION = 0x80E4DAF0
MT_LOCATION = 0x80E4C796
CP_LOCATION = 0x80E43746
WHEELIE_LOCATION = 0x90284F04
ROAD_TYPE_LOCATION = 0x80E51CE8


# Returns the current speed of the kart
def getCurrentSpeed() -> float:
    return round(memory.read_f32(SPEED_LOCATION))

# Returns the value of the players current race completion (Race%)
def getCurrentRaceCompletion() -> float:
    return round(memory.read_f32(RACE_COMPLETION_LOCATION), 2)

# Rounds a nunber to the nearest 100
def factorPositions(position) -> float:
    return round(position / 100)

# Returnsth current X and Z coordinate
def getCurrentXZPos() -> tuple:
    return factorPositions(memory.read_f32(X_POS_LOCATION)), factorPositions(memory.read_f32(Z_POS_LOCATION))

# Returns the value of the player's current miniturbo charge (MT)
def getCurrentMT() -> int:
    return memory.read_u16(MT_LOCATION)
    
# Returns the current CP value
def getCurrentCP() -> float:
    return memory.read_u16(CP_LOCATION)
    
# Returns the current CP value
def getCurrentWheelie() -> bool:
    return bool(memory.read_u16(WHEELIE_LOCATION))
    
# Returns a tuple of the Speed, Race% and MT
def getRaceInfo() -> tuple:
    return getCurrentSpeed(), getCurrentRaceCompletion(), getCurrentMT(),getCurrentWheelie(), getCurrentCP()

def getCurrentRoadType() -> int:
    return memory.read_u16(ROAD_TYPE_LOCATION)

def printRaceInfo():
    print(f'MT: {getCurrentMT()}')
    print(f'Race%: {getCurrentRaceCompletion()}')
    print(f'Speed: {getCurrentSpeed()}')

#event.on_frameadvance(printRaceInfo)