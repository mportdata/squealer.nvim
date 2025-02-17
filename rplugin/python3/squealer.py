import pynvim
import sqlglot
import os

@pynvim.plugin
class SqlTranspiler:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command('TranspileSQL', nargs='1', sync=True)
    def transpile_sql(self, args):
        target_dialect = args[0]
        current_file = self.nvim.current.buffer.name

        if not current_file:
            self.nvim.err_write("No file open.\n")
            return

        try:
            with open(current_file, "r") as f:
                sql = f.read()

            detected_dialect = None  # You can improve detection logic
            transpiled_sql = sqlglot.transpile(sql, read=detected_dialect, write=target_dialect)[0]

            output_file = f"{os.path.splitext(current_file)[0]}_{target_dialect}.sql"
            with open(output_file, "w") as f:
                f.write(transpiled_sql)

            self.nvim.out_write(f"Transpiled SQL saved to {output_file}\n")
        except Exception as e:
            self.nvim.err_write(f"Error: {e}\n")
