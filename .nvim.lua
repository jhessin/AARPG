-- .nvim.lua (Place in your Godot project root folder)

-- Force Pyright to index the local py4godot addon files for typings
-- local local_py4godot_path = vim.fn.getcwd() .. "/addons/py4godot"

-- Inject it into the Pyright LSP initialization sequence
-- vim.api.nvim_create_autocmd("LspAttach", {
-- 	callback = function(args)
-- 		local client = vim.lsp.get_client_by_id(args.data.client_id)
-- 		if client and client.name == "pyright" then
-- 			if client.config.settings.python.analysis.extraPaths then
-- 				table.insert(client.config.settings.python.analysis.extraPaths, local_py4godot_path)
-- 			else
-- 				client.config.settings.python.analysis.extraPaths = { local_py4godot_path }
-- 			end
-- 			-- Notify Pyright that the configuration changed so it re-scans the workspace
-- 			client.notify("workspace/didChangeConfiguration", { settings = client.config.settings })
-- 		end
-- 	end,
-- })
