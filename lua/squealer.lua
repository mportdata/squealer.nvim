local M = {}

function M.pick_dialect()
	local pickers = require("telescope.pickers")
	local finders = require("telescope.finders")
	local actions = require("telescope.actions")
	local action_state = require("telescope.actions.state")

	local dialects = { "snowflake", "hive", "trino", "spark", "bigquery", "duckdb" }

	pickers
		.new({}, {
			prompt_title = "Select SQL Dialect",
			finder = finders.new_table(dialects),
			sorter = require("telescope.config").values.generic_sorter({}),
			attach_mappings = function(_, map)
				map("i", "<CR>", function(bufnr)
					local selection = action_state.get_selected_entry()
					actions.close(bufnr)
					-- Directly call the Python command with the selected dialect
					vim.api.nvim_command("TranspileSQL " .. selection[1])
				end)
				return true
			end,
		})
		:find()
end

function M.setup()
	vim.api.nvim_create_user_command("SquealerPickDialect", M.pick_dialect, {})
	print("Squealer plugin loaded successfully!")
end

return M
