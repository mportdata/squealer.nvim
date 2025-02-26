# squealer.nvim

A [neovim](https://github.com/neovim/neovim) plugin that uses [SQLGlot](https://github.com/tobymao/sqlglot) to transpile between SQL dialects.

## Install

### Using [lazy.nvim](https://github.com/folke/lazy.nvim)

#### Configure Python Virtual Environment

##### Install Python and Rust then create the Python virtual environment to be used by [lazy.nvim](https://github.com/folke/lazy.nvim)

###### MacOS
```
brew install rust
brew install python
mkdir -p ~/.local/venv
python3 -m venv ~/.local/venv/nvim
```
##### Add the below to [lazy.nvim](https://github.com/folke/lazy.nvim) options file in the config directory
```
-- config/options.lua
vim.g.python3_host_prog = "~/.local/venv/nvim/bin/python"
```

#### Add squealer.nvim to [lazy.nvim](https://github.com/folke/lazy.nvim) plugins directory
```
-- plugins/squealer.lua
return {
  {
    "mportdata/squealer.nvim",
    lazy = true,
    ft = { "sql" },
    dependencies = { "nvim-telescope/telescope.nvim" },
    keys = {
      { "<leader>tp", "<cmd>TranspileSQL<CR>", desc = "Pick SQL Dialect & Transpile" },
    },
    config = function()
      local plugin_path = vim.fn.stdpath("data") .. "/lazy/squealer.nvim"
      local requirements_file = plugin_path .. "/requirements.txt"
      local rplugin_manifest = vim.fn.stdpath("data") .. "/rplugin.vim"

      -- Ensure Python is available
      if vim.fn.executable("python3") == 0 then
        print("Error: python3 is not installed or not in PATH.")
        return
      end

      -- Install Python dependencies if requirements.txt exists
      if vim.fn.filereadable(requirements_file) == 1 then
        local pip_cmd = "pip install --user -r " .. vim.fn.shellescape(requirements_file)
        print("Running: " .. pip_cmd)
        local result = vim.fn.system(pip_cmd)
        print("pip install result: " .. result)
      else
        print("Warning: requirements.txt not found at " .. requirements_file)
      end

      -- Register the Python remote plugin if needed
      if vim.fn.filereadable(rplugin_manifest) == 0 then
        print("rplugin.vim not found. Running UpdateRemotePlugins...")
        vim.cmd("UpdateRemotePlugins")
      else
        print("Remote plugins already registered.")
      end

      require("squealer").setup()
    end,
  },
}
```
