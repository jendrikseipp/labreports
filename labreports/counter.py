from collections import defaultdict

from downward.reports import PlanningReport
from lab.reports import Table


class PerAlgorithmCounterReport(PlanningReport):
    """
    Generate per-algorithm table counting the number of times each algorithm yields which attribute value.

    This is especially useful for counting the number of times a planner solves a task,
    runs out of time, etc.

    """
    def __init__(self, **kwargs):
        PlanningReport.__init__(self, **kwargs)
        if len(self.attributes) != 1:
            raise ValueError("Report needs exactly one attribute")
        self.attribute = self.attributes[0]

    def get_markup(self):
        # {"ff": {"solved": 1, "out of time": 2, ...}, ...}
        algo_to_counts = defaultdict(lambda: defaultdict(int))
        for (domain, problem), runs in sorted(self.problem_runs.items()):
            for run in runs:
                algo = run["algorithm"]
                if self.attribute in run:
                    algo_to_counts[algo][run[self.attribute]] += 1

        table = Table()
        for algo, counts in algo_to_counts.items():
            for result, count in counts.items():
                table.add_cell(result, algo, count)
        table.add_summary_function("sum", sum)

        return str(table)


class PerDomainCounterReport(PlanningReport):
    """
    Generate per-domain table counting the number of times each attribute value occurs.

    This is especially useful for counting the number of times a planner solves a task,
    runs out of time, etc.

    """
    def __init__(self, **kwargs):
        PlanningReport.__init__(self, **kwargs)
        if len(self.attributes) != 1:
            raise ValueError("Report needs exactly one attribute")
        self.attribute = self.attributes[0]

    def get_markup(self):
        # {"gripper": {"solved": 1, "out of time": 2, ...}, ...}
        domains_to_counts = defaultdict(lambda: defaultdict(int))
        for (domain, problem), runs in sorted(self.problem_runs.items()):
            if len(runs) != 1:
                raise ValueError("Use filter_algorithm=['myalgo'] to select exactly one algorithm")
            domains_to_counts[domain][runs[0][self.attribute]] += 1

        table = Table()
        for domain, counts in domains_to_counts.items():
            for result, count in counts.items():
                table.add_cell(domain, result, count)
        table.add_summary_function("sum", sum)

        return str(table)
