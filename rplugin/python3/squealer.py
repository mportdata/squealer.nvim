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
        if not args or not args[0]:  # If no dialect is provided, pick one
            self.select_dialect_then_transpile()
        else:
            self._run_transpiler(args[0])

    def _run_transpiler(self, target_dialect):
        """Handles SQL transpilation"""
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

    def select_dialect_then_transpile(self):
        """Triggers the Telescope picker and captures the selected dialect"""
        self.nvim.command("SquealerPickDialect")  # Calls the Lua function

        # Listen for the user's selection (Telescope picker sets a Neovim variable)
        @self.nvim.async_call
        def check_dialect():
            selected_dialect = self.nvim.vars.get("squealer_selected_dialect", None)
            if selected_dialect:
                self._run_transpiler(selected_dialect)

        # Delay checking for the selected dialect
        self.nvim.call("timer_start", 500, check_dialect)

