import collections
import dataclasses
import enum


from jacl import Stack


class Opcode(enum.IntEnum):
    LOAD_CONST   = 0x00
    SET_GLOBAL   = enum.auto()
    GET_GLOBAL   = enum.auto()

    ...


@dataclasses.dataclass
class MemoryBlock:
    data: bytearray = dataclasses.field(default_factory=bytearray)



@dataclasses.dataclass
class VirtualMachine:
    executing: bool = False

    code: MemoryBlock = dataclasses.field(default_factory=MemoryBlock)
    heap: MemoryBlock = dataclasses.field(default_factory=MemoryBlock)

    datastack: Stack = dataclasses.field(default_factory=Stack)
    retainstack: Stack = dataclasses.field(default_factory=Stack)
