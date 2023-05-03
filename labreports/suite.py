from lab import tools

from downward.reports import PlanningReport


class SuiteReport(PlanningReport):
    """Write a list of problems to a Python file.

    The data can be filtered by the filter functions passed to the constructor.
    All the runs are checked whether they pass the filters and the remaining
    runs are sorted, the duplicates are removed and the resulting list of
    problems is written to the output file.

    Write a suite with solved problems: ::

        exp.add_report(SuiteReport(filter_coverage=1), outfile="solved.py")
    """
    def __init__(self, **kwargs):
        kwargs.setdefault('format', 'py')
        PlanningReport.__init__(self, **kwargs)

    def get_text(self):
        """
        We do not need any markup processing or loop over attributes here,
        so we directly implement the get_text() method.
        """
        print(dir(self))
        tasks = [f"{domain}:{problem}" for domain, problems in self.domains.items() for problem in problems]
        lines = [f'        "{task}",' for task in tools.natural_sort(tasks)]
        text = "\n".join(lines)
        return f'def suite():\n    return [\n{text}\n]\n'
