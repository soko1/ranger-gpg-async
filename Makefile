PLUGIN_DIR=$(if $(XDG_CONFIG_HOME),$(XDG_CONFIG_HOME),$(HOME)/.config)/ranger/plugins

install:
	install -Dm644 encrypt.py $(PLUGIN_DIR)/encrypt.py
	install -Dm644 decrypt.py $(PLUGIN_DIR)/decrypt.py

uninstall:
	$(RM) $(PLUGIN_DIR)/encrypt.py
	$(RM) $(PLUGIN_DIR)/decrypt.py

