import pandas as pd

class Diagnostics:
    def __init__(self, level=3, enabled=True):
        self.level = level
        self.enabled = enabled
        self.tables = {}
        self.context = {}

    def set_context(self, **kwargs):
        self.context.update(kwargs)

    def log(self, table, **fields):
        if not self.enabled:
            return
        row = {**self.context, **fields}
        self.tables.setdefault(table, []).append(row)

    def save(self, output_dir):
        if not self.enabled:
            return
        for name, rows in self.tables.items():
            pd.DataFrame(rows).to_csv(f'{output_dir}/{name}.csv', index=False)