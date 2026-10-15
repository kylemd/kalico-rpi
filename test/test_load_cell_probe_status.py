from klippy.extras.load_cell.load_cell_probe import TappingMove


class FakeConfig:
    def __init__(self, printer):
        self._printer = printer

    def get_printer(self):
        return self._printer


class FakePrinter:
    class Reactor:
        @staticmethod
        def monotonic():
            return 2.0

    def get_reactor(self):
        return self.Reactor()


class FakeCollector:
    @staticmethod
    def collect_until(print_time):
        return (["sample"], None)


class FakeMcu:
    @staticmethod
    def estimated_print_time(eventtime):
        return eventtime


class FakePrimitives:
    def probing_move(self, tapping_move, pos, speed, gcmd):
        return [10.0, 20.0, 0.5], FakeCollector()

    @staticmethod
    def get_status(eventtime):
        return {"last_trigger_time": 1.0}

    @staticmethod
    def get_mcu():
        return FakeMcu()

    add_stepper = None
    get_steppers = None
    home_wait = None
    query_endstop = None


class FakeConfigHelper:
    @staticmethod
    def is_pullback_move_disabled():
        return False

    @staticmethod
    def get_trigger_force_grams(gcmd):
        return 75.0


class FakeAnalysis:
    @staticmethod
    def is_valid():
        return True

    @staticmethod
    def get_tap_pos():
        return [10.0, 20.0, 0.25]


class FakeAnalysisHelper:
    @staticmethod
    def analyze(samples, trigger_force, collection_time, gcmd):
        return FakeAnalysis()


def test_status_reports_z_result_from_last_valid_tap():
    move = TappingMove(
        FakeConfig(FakePrinter()),
        FakePrimitives(),
        FakeAnalysisHelper(),
        FakeConfigHelper(),
    )
    move.pullback_move = lambda gcmd: 1.0

    position, is_valid = move.probing_move(
        [10.0, 20.0, -3.0], 1.0, object()
    )

    assert is_valid is True
    assert position[2] == 0.25
    assert move.get_status(2.0)["last_z_result"] == 0.25


if __name__ == "__main__":
    test_status_reports_z_result_from_last_valid_tap()
