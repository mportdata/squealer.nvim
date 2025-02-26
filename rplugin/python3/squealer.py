import pynvim
import sqlglot
import os

@pynvim.plugin
class SqlTranspiler:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command('TranspileSQL', nargs='?', sync=True)
    def transpile_sql(self, args):
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

            try:
                # Read from buffer instead of file for latest changes
                sql = "\n".join(self.nvim.current.buffer[:])
                transpiled_sql = sqlglot.transpile(
                    sql, 
                    read=source_dialect, 
                    write=target_dialect,
                    pretty=True
                )[0]

                self.nvim.current.buffer[:] = transpiled_sql.splitlines()
                self.nvim.command("redraw!")
                self.nvim.out_write(f"SQL transpiled from {source_dialect} to {target_dialect} in-place.\n")
            except Exception as e:
                self.nvim.err_write(f"Unexpected error: {e}\n")

