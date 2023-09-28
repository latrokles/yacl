from dataclasses import dataclasses
from pathlib import Path

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


@dataclass
class Assembler:
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
                # TODO put string in data memory
                return
