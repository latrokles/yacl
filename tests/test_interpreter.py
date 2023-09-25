import pytest

from yacl.interpreter import CallFrame, Interpreter


@pytest.fixture
def yacl(top_of_stack):
    yacl = Interpreter()
    yacl.datastack.push(top_of_stack)
    return yacl


@pytest.mark.parametrize('top_of_stack', [[1, 2, 3]])
def test_run_evalutes_code_in_callframe(yacl):
    yacl.call()
    yacl.run()

    assert yacl.d_pop() == 3
    assert yacl.d_pop() == 2
    assert yacl.d_pop() == 1


@pytest.mark.parametrize('top_of_stack', [[1, 2]])
def test_run_evaluates_next_frame_in_callstack(yacl):
    yacl.callstack.push(CallFrame(code=[3]))
    yacl.call()
    yacl.run()

    assert yacl.d_pop() == 3
    assert yacl.d_pop() == 2
    assert yacl.d_pop() == 1


@pytest.mark.parametrize('top_of_stack', [1])
def test_call_errors_if_top_of_stack_is_not_a_quotation(yacl):
    with pytest.raises(RuntimeError):
        yacl.call()


@pytest.mark.parametrize('top_of_stack', [[1]])
def test_reset_clears_all_stacks_and_callframe(yacl):
    yacl.call()
    yacl.reset()

    assert yacl.callframe.is_finished()
    assert yacl.callstack.is_empty()
    assert yacl.datastack.is_empty()
    assert yacl.retainstack.is_empty()
