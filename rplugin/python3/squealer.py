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
        if not args or not args[0] or not args[1]:  # If no dialect is provided, trigger picker
            self.nvim.command("SquealerPickDialect")
        else:
            self._run_transpiler(args[0], args[1])

    def _run_transpiler(self, source_dialect, target_dialect):
        """Handles SQL transpilation"""
        current_file = self.nvim.current.buffer.name
        if not current_file:
            self.nvim.err_write("No file open.\n")
            return

        try:
            # Read from buffer instead of file for latest changes
            sql = "\n".join(self.nvim.current.buffer[:])
            transpiled_sql = sqlglot.transpile(
                sql, 
                read=source_dialect, 
                write=target_dialect,
                pretty=True
            )[0]

            output_file = f"{os.path.splitext(current_file)[0]}.sql"
            with open(output_file, "w") as f:
                f.write(transpiled_sql)
            self.nvim.command("redraw!")
            self.nvim.out_write(f"SQL transpiled from {source_dialect} to {target_dialect}.\n")
        except Exception as e:
            self.nvim.err_write(f"Unexpected error: {e}\n")

