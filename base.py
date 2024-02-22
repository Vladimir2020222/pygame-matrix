class SymbolChanger:
    symbol_state_keys: list[str] = []

    def save_symbol_state(self, symbol: 'Symbol') -> None:
        for key in self.symbol_state_keys:
            foreign_key = self.get_key(key)
            symbol.foreign_data[foreign_key] = getattr(symbol, key)

    def restore_symbol_state(self, symbol, ignore_key_error=True, clear_state=True) -> None:
        for key in self.symbol_state_keys:
            try:
                foreign_key = self.get_key(key)
                setattr(symbol, key, symbol.foreign_data[foreign_key])
                if clear_state:
                    del symbol.foreign_data[foreign_key]
            except KeyError:
                if not ignore_key_error:
                    raise

    @property
    def prefix(self):
        return f'{self.__class__.__name__}-'

    def get_key(self, key) -> str:
        return self.prefix + key


class GetAccelerationCoefficientMixin:
    acceleration_time: float

    def get_acceleration_coefficient(self):
        time_to_end = self.duration - self.time_passed
        time_passed = self.time_passed
        res = min(time_to_end, time_passed, self.acceleration_time) * (1 / self.acceleration_time)
        return max(res, 0)

