from collections import defaultdict

from downward.reports import PlanningReport

class CactusPlot(PlanningReport):
    def write(self):
        data = defaultdict(list)
        for algo in self.algorithms:
            runtimes = []
            for run in self.runs.values():
                if run["algorithm"] != algo:
                    continue
                if run["coverage"]:
                    runtimes.append(int(run["planner_time"]))
            runtimes.sort()
            coverage = len(runtimes)
            coords = []
            last_runtime = None
            for runtime in reversed(runtimes):
                if last_runtime is None or runtime < last_runtime:
                    x = runtime
                    y = coverage
                    coords.append((x, y))
                coverage -= 1
                last_runtime = runtime
            coords = list(reversed(coords))

            # Prepend coverage of 0 at the first coordinate value.
            first_coord = coords[0]
            x, y = first_coord
            if x != 0:
                coords.insert(0, (x, 0))

            # Repeat last coverage value at 1800s.
            coverage = len(runtimes)
            coord = (1800, coverage)
            if coords[-1] != coord:
                coords.append(coord)

            print("\\addplot coordinates {")
            for x, y in coords:
                print(f"({x}, {y})", end=" ")
            print("};")
            print(f"\\addlegendentry{{{algo.split(':')[-1]}}}")
            print()
