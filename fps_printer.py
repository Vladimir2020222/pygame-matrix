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
        if now - self.second_start > 1:
            self.fps = self.tick
            if self.fps < self.min_fps:
                self.min_fps = self.fps
            self.tick = 0
            self.second_start = now
        self.avg_fps = self.total_ticks / (now - self.start)

    def print(self):
        print(f'\rFPS: {self.fps}; AVG FPS: {self.avg_fps:.2f}; MIN FPS: {self.min_fps}', end='')
