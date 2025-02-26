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
        if not args:    
            self.nvim.command("SquealerPickDialect")
        else:
            self._run_transpiler(args[0]) 

    def _run_transpiler(self, dialects):
        dialects_array = dialects.split(' ')
        if len(dialects_array) < 2:
            self.nvim.err_write("Number of dialects detected less than 2")
        else:
            source_dialect = dialects_array[0]
            target_dialect = dialects_array[1]
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
                current_buffer[:] = transpiled_sql.splitlines()
                self.nvim.command("redraw!")
                self.nvim.out_write("Debug: Redraw done\n")
                self.nvim.out_write(f"SQL transpiled from {source_dialect} to {target_dialect} in-place.\n")
            except Exception as e:
                self.nvim.err_write(f"Unexpected error: {e}\n")

