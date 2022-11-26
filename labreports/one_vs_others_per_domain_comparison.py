from downward.reports import PlanningReport

class OneVsOthersPerDomainComparison(PlanningReport):
    def __init__(self, algorithm, **kwargs):
        PlanningReport.__init__(self, **kwargs)
        self.algorithm = algorithm

    def get_markup(self):
        domain_and_algorithm_to_coverage = defaultdict(int)
        for (domain, problem), runs in self.problem_runs.items():
            for run in runs:
                domain_and_algorithm_to_coverage[(run["domain"], get_algorithm(run))] += run["coverage"]

        domain_groups = sorted(set([group for group, algo in domain_and_algorithm_to_coverage.keys()]))

        summary_table = Table("Summary")
        summary_table.set_column_order(self.algorithms)
        for algo in self.algorithms:
            num_better = 0
            num_worse = 0
            num_equal = 0
            for domain in domain_groups:
                coverage1 = domain_and_algorithm_to_coverage[(domain, self.algorithm)]
                coverage2 = domain_and_algorithm_to_coverage[(domain, algo)]
                if coverage1 > coverage2:
                    num_better += 1
                elif coverage1 < coverage2:
                    num_worse += 1
                else:
                    assert coverage1 == coverage2
                    num_equal += 1
            assert num_better + num_equal + num_worse == len(domain_groups)
            coverage = sum(domain_and_algorithm_to_coverage[(domain, algo)] for domain in domain_groups)
            summary_table.add_cell("Coverage", algo, coverage)
            summary_table.add_cell("Better", algo, num_better)
            summary_table.add_cell("Worse", algo, num_worse)
            summary_table.set_row_order(["Coverage", "Better", "Worse"])

        return str(summary_table)
