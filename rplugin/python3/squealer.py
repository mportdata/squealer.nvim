import pynvim
import sqlglot
import os

@pynvim.plugin
class SqlTranspiler:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command('TranspileSQL', nargs='?', sync=True)
    def transpile_sql(self, args):
        """Transpiles SQL to the given dialect"""
        if not args or not args[0]:  # If no dialect is provided, trigger picker
            self.nvim.command("SquealerPickDialect")
        else:
            self._run_transpiler(args[0])

    def _run_transpiler(self, target_dialect):
        """Handles SQL transpilation"""
        current_file = self.nvim.current.buffer.name
        if not current_file:
            self.nvim.err_write("No file open.\n")
            return

        try:
            # Read from buffer instead of file for latest changes
            sql = "\n".join(self.nvim.current.buffer[:])
            transpiled_sql = sqlglot.transpile(sql, read=None, write=target_dialect)[0]

            output_file = f"{os.path.splitext(current_file)[0]}.sql"
            with open(output_file, "w") as f:
                f.write(transpiled_sql)

            self.nvim.out_write(f"Transpiled SQL saved to {output_file}\n")
        except Exception as e:
            self.nvim.err_write(f"Unexpected error: {e}\n")

