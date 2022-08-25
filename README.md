# Labreports

A collection of report classes for the [Downward Lab](https://lab.readthedocs.io/) toolkit.

## Installation

```console
    git clone https://github.com/jendrikseipp/labreports.git
    pip install --editable labreports/
```

## Usage

```python
from labreports import PerTaskComparison

exp.add_report(PerTaskComparison(attributes=["initial_h_value"]))
```

See the [source code](labreports/) for available report classes. Note that the
code in this repo is not necessarily kept in sync with Downward Lab. You may
need to make some adjustments before it runs. Pull requests welcome!
