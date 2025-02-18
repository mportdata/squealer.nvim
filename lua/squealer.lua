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

					-- Save selected dialect in a Neovim variable for Python to read
					vim.api.nvim_set_var("squealer_selected_dialect", selection[1])
				end)
				return true
			end,
		})
		:find()
end

vim.api.nvim_create_user_command("SquealerPickDialect", function()
	M.pick_dialect()
end, {})

return M
