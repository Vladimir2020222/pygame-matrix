from time import perf_counter


class FpsCounter:
    def __init__(self):
        self.second_start = perf_counter()
        self.tick = 0
        self.fps = 0
        self.start = perf_counter()
        self.total_ticks = 0
        self.avg_fps = 0
        self.min_fps = 99999999

    def update(self):
        self.tick += 1
        self.total_ticks += 1
        now = perf_counter()

        self.avg_fps = self.total_ticks / (now - self.start)

        time_elapsed = now - self.second_start

        self.fps = self.tick / time_elapsed
        if self.fps < self.min_fps:
            self.min_fps = self.fps
        if time_elapsed > 1:
            self.tick = 0
            self.second_start = now

    def print(self):
        print(f'\rFPS: {self.fps:.2f}; AVG FPS: {self.avg_fps:.2f}; MIN FPS: {self.min_fps:.2f}', end='')
