from dolphin import memory
# This script contains

def getGameID():
    # 6-byte string at address 0x80000000
    # For the version I am using this will always be 'RMCE01'
    id = hex(memory.read_u64(0x80000000))[2:14]
    id = bytes.fromhex(id).decode('utf-8')
    return id

# getPointerCHain: read a series of pointers and add an offset at each read
# Essentially follow a pointer chain through memory
def getPointerChain(pointer, offsets):
    for offset in offsets:
        pointer = memory.read_u32(pointer) + offset
        if pointer == 0 or pointer == offset:
            pointer = 0
            break
    return pointer

def getCurrentCheckpointPointer(Offset):
    pointer = 0x80000000
    pointer += 0x9B8F70
    return getPointerChain(pointer, [0xC, Offset, 0x24])
    
print(getGameID())
print(memory.read_u16(getCurrentCheckpointPointer(0x0)))