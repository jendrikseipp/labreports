from collections import defaultdict

from downward.reports import PlanningReport

class CactusPlot(PlanningReport):
    """Example plotting coverage over time:

        CactusPlot(attributes=["coverage", "planner_time"])

    """
    def __init__(self, attributes=None, **kwargs):
        try:
            self.cumulative_attribute, self.time_attribute = attributes
        except ValueError:
            raise ValueError("CactusPlot needs exactly two attributes.") from None
        super().__init__(attributes=attributes, **kwargs)

    def write(self):
        for algo in self.algorithms:
            runtimes = []
            for run in self.runs.values():
                if run["algorithm"] != algo:
                    continue
                if run.get(self.cumulative_attribute):
                    runtimes.append(int(run[self.time_attribute]))
            runtimes.sort()
            cumulative_value = len(runtimes)
            coords = []
            last_runtime = None
            for runtime in reversed(runtimes):
                if last_runtime is None or runtime < last_runtime:
                    x = runtime
                    y = cumulative_value
                    coords.append((x, y))
                cumulative_value -= 1
                last_runtime = runtime
            coords = list(reversed(coords))

            # Prepend cumulative value of 0 at the first coordinate value.
            first_coord = coords[0]
            x, y = first_coord
            if x != 0:
                coords.insert(0, (x, 0))

            # Repeat last cumulative value at 1800s.
            cumulative_value = len(runtimes)
            coord = (1800, cumulative_value)
            if coords[-1] != coord:
                coords.append(coord)

            print("\\addplot coordinates {")
            for x, y in coords:
                print(f"({x}, {y})", end=" ")
            print("};")
            print(f"\\addlegendentry{{{algo}}}")
            print()
