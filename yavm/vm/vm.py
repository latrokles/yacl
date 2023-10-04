import enum

from dataclasses import dataclasses, field
from yavm import Stack


class Opcode(enum.IntEnum):
    LOAD_CONST   = 0x00
    SET_GLOBAL   = enum.auto()
    GET_GLOBAL   = enum.auto()
    SYS_CALL     = enum.auto()
    ...


class Types(enum.IntEnum):
    INT    = 0x00
    FLOAT  = enum.auto()
    STRING = enum.auto()


@dataclass
class MemoryBlock:
    data: bytearray = field(default_factory=bytearray)

    def push_bytes(self, value_bytes):
        self.data.extend(value_bytes)


@dataclass
class VirtualMachine:
    executing: bool = False

    code: MemoryBlock = field(default_factory=MemoryBlock)
    heap: MemoryBlock = field(default_factory=MemoryBlock)
    types: list = field(default_factory=list)

    datastack: Stack = field(default_factory=Stack)
    retainstack: Stack = field(default_factory=Stack)
