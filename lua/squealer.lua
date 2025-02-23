local M = {}

local pickers = require("telescope.pickers")
local finders = require("telescope.finders")
local actions = require("telescope.actions")
local action_state = require("telescope.actions.state")

local dialects = { "snowflake", "hive", "trino", "spark", "bigquery", "duckdb" }

function M.pick_source_dialect()
	pickers
		.new({}, {
			prompt_title = "Select Source SQL Dialect",
			finder = finders.new_table(dialects),
			sorter = require("telescope.config").values.generic_sorter({}),
			attach_mappings = function(_, map)
				local source_selection = map("i", "<CR>", function(bufnr)
					local source_selection = action_state.get_selected_entry()
					actions.close(bufnr)
					return source_selection
				end)
				return source_selection
			end,
		})
		:find()
end

function M.pick_target_dialect()
	pickers
		.new({}, {
			prompt_title = "Select Target SQL Dialect",
			finder = finders.new_table(dialects),
			sorter = require("telescope.config").values.generic_sorter({}),
			attach_mappings = function(_, map)
				local target_selection = map("i", "<CR>", function(bufnr)
					local target_selection = action_state.get_selected_entry()
					actions.close(bufnr)
					return target_selection
				end)
				return target_selection
			end,
		})
		:find()
end

function M.transpile_sql()
	local source_selection = M.pick_source_dialect()[1]
	local target_selection = M.pick_target_dialect()[1]
	if not source_selection then
		print("Source selection missing!")
	else
		if not target_selection then
			print("Target selection missing!")
		else
			vim.api.nvim_command("TranspileSQL " .. source_selection .. target_selection)
		end
	end
	return true
end

function M.setup()
	vim.api.nvim_create_user_command("SquealerPickDialect", M.transpile_sql(), {})
	print("Squealer plugin loaded successfully!")
end

return M
