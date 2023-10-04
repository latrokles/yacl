from dataclasses import dataclass
from pathlib import Path
from struct import pack

from yavm.vm import MemoryBlock


@dataclass
class SourceInput:
    src: str
    idx: int = 0
    row: int = 0
    col: int = 0

    def is_at_eof(self):
        return self.idx >= len(self.src)

    def peek(self):
        if self.is_at_eof():
            return '\0'
        return self.src[self.idx]

    def consume(self):
        if self.is_at_eof():
            # TODO set parse error
            raise RuntimeError('reached end of input')

        char = self.src[self.idx];
        self.idx += 1;

        if char == '\n':
            self.row += 1;
            self.col = 1;
        else:
            self.col += 1;

        return char

    def parse_string(self):
        start = self.consume()
        chars = []

        while True:
            char = self.consume()
            if char == start:
                break

            if self.is_at_eof():
                # TODO handle parse error
                return

            chars.append(char)

        return ''.join(chars).encode('utf-8')

    def parse_word(self):
        chars = []
        while True:
            char = self.consume()
            if char in (' '):
                return ''.join(chars)

            if self.is_at_eof():
                return ''.join(chars)
            chars.append(char)


@dataclass
class Assembler:
    code: MemoryBlock = field(default_factory=MemoryBlock)
    data: MemoryBlock = field(default_factory=MemoryBlock)
    types: list = field(default_factory=list)

    def assemble_file(self, source_file):
        src_input = SourceInput(Path(source_file).read_text())
        self.parse_input(src_input)

    def parse_input(self, src_input):
        while True:
            if src_input.is_at_eof():
                break

            self.parse_line(src_input)

    def parse_line(self, src_input):
        char = src_input.peek()

        match char:
            case '\n':
                src_input.consume()
                return

            case '\'':
                val = src_input.parse_string()
                self.data.push_bytes(val.encode('utf-8'))
                self.types.push(Type.STRING)
                return

            case str() if char in '0123456789':
                val, val_type = src_input.parse_number()
                match val_type:
                    case int():
                        self.data.push_bytes(pack('<l', val))
                        self.types.append(Types.INT)
                        return
                    case float():
                        self.data.push_bytes(pack('<d', val))
                        self.types.append(Types.FLOAT)
                        return
                    case _:
                        # TODO set proper parse error
                        raise RuntimeError('oops')

            case str():
                word = src_input.parse_word()
