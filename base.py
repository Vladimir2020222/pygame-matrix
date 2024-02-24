from line_profiler_pycharm import profile


class SymbolChanger:
    symbol_state_keys: list[str] = []

    def save_symbol_state(self, symbol: 'Symbol') -> None:
        for key in self.symbol_state_keys:
            foreign_key = self.get_key(key)
            symbol.foreign_data[foreign_key] = getattr(symbol, key)

    def restore_symbol_state(self, symbol, ignore_key_error=True, clear_state=True) -> None:
        for key in self.symbol_state_keys:
            self.restore_symbol_state_key(symbol, key, ignore_key_error, clear_state)

    def restore_symbol_state_key(self, symbol, key: str, ignore_key_error=True, clear_state=True) -> None:
        try:
            foreign_key = self.get_key(key)
            setattr(symbol, key, symbol.foreign_data[foreign_key])
            if clear_state:
                del symbol.foreign_data[foreign_key]
        except KeyError:
            if not ignore_key_error:
                raise

    def get_key(self, key) -> str:
        return f'{self.__class__.__name__}-{key}'


class GetAccelerationCoefficientMixin:
    acceleration_time: float

    def __init_subclass__(cls, **kwargs):
        cls._1_divided_by_acceleration_time = 1 / cls.acceleration_time

    def get_acceleration_coefficient(self):
        time_passed = self.time_passed
        return max(
            min(
                self.duration - time_passed,
                time_passed,
                self.acceleration_time
            ) * self._1_divided_by_acceleration_time,
            0
        )
