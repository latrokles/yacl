import dataclasses
import traceback

from yavm import Stack


@dataclasses.dataclass
class CallFrame:
    code: list = dataclasses.field(default_factory=list)
    ip: int = 0

    @property
    def length(self):
        return len(self.code)

    def has_next(self):
        return self.ip < self.length

    def is_finished(self):
        return self.ip >= self.length

    def next(self):
        if self.ip >= self.length:
            raise RuntimeError('there is no more code to evaluate in current call frame!')

        value = self.code[self.ip]
        self.ip += 1
        return value


class NullCallFrame:
    def has_next(self):
        return False

    def is_finished(self):
        return True

    def next(self):
        raise RuntimeError('cannot get value from null callframe')


@dataclasses.dataclass
class Interpreter:
    executing: bool = False
    callframe: CallFrame = dataclasses.field(default_factory=NullCallFrame)

    callstack: Stack = dataclasses.field(default_factory=Stack)
    datastack: Stack = dataclasses.field(default_factory=Stack)
    retainstack: Stack = dataclasses.field(default_factory=Stack)

    def d_push(self, value):
        self.datastack.push(value)

    def d_pop(self):
        return self.datastack.pop()

    def d_peek(self):
        return self.datastack.peek()

    def call(self):
        quote = self.d_peek()
        if not isinstance(quote, list):
            raise RuntimeError(f'`call` expected `[ ]`, but got `{type(quote)}`!')

        if self.callframe.has_next():
            self.callstack.push(self.callframe)

        self.callframe = CallFrame(code=self.d_pop())

    def run(self):
        self.executing = True
        while self.executing:
            try:
                if self.callframe.is_finished():
                    if self.callstack.is_empty():
                        # nothing left to execute
                        break

                    self.callframe = self.callstack.pop()
                    continue

                next_evaluation = self.callframe.next()
                self.eval(next_evaluation)
            except Exception as e:
                if self.handle_error(e):
                    return

        self.callframe = NullCallFrame()

    def eval(self, value):
        # TODO handle words
        self.d_push(value)

    def handle_error(self, error):
        if not self.executing:
            # interpreter error-ed out before starting execution loop
            # print stacktrace and bail out.
            traceback.print_exc()
            self.reset()
            return True

        # attempt to handle the error using the errors vocab handler
        self.d_push(error)
        try:
            throw = self.get_from_vocab('throw', 'errors')
            self.eval(throw)
            return False
        except Exception as e:
            print(f'there was an error executing `throw`, error={e}')
            traceback.print_exc()
            self.reset()
            return True

    def reset(self):
        self.executing = False
        self.callframe = NullCallFrame()

        self.callstack = Stack()
        self.datastack = Stack()
        self.retainstack = Stack()
