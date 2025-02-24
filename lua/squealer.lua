local M = {}

local pickers = require("telescope.pickers")
local finders = require("telescope.finders")
local actions = require("telescope.actions")
local action_state = require("telescope.actions.state")

local dialects = { "snowflake", "hive", "trino", "spark", "bigquery", "duckdb" }

function M.pick_source_dialect(callback)
	pickers
		.new({}, {
			prompt_title = "Select Source SQL Dialect",
			finder = finders.new_table(dialects),
			sorter = require("telescope.config").values.generic_sorter({}),
			attach_mappings = function(_, map)
				map("i", "<CR>", function(bufnr)
					local source_selection = action_state.get_selected_entry()[1]
					actions.close(bufnr)
					callback(source_selection)
				end)
				return true
			end,
		})
		:find()
end

function M.pick_target_dialect(source_dialect)
	pickers
		.new({}, {
			prompt_title = "Select Target SQL Dialect",
			finder = finders.new_table(dialects),
			sorter = require("telescope.config").values.generic_sorter({}),
			attach_mappings = function(_, map)
				map("i", "<CR>", function(bufnr)
					local target_selection = action_state.get_selected_entry()[1]
					actions.close(bufnr)
					vim.api.nvim_command(
						"TranspileSQL '"
							.. vim.fn.shellescape(source_dialect)
							.. "' '"
							.. vim.fn.shellescape(target_selection)
							.. "'"
					)
				end)
				return true
			end,
		})
		:find()
end

function M.transpile_sql()
	M.pick_source_dialect(function(source_dialect)
		M.pick_target_dialect(source_dialect)
	end)
end

function M.setup()
	vim.api.nvim_create_user_command("SquealerPickDialect", M.transpile_sql, {}) -- Pass function reference, not call
	print("Squealer plugin loaded successfully!")
end

return M
