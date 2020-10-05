INSTALL_PATH ?= /usr/local/nagios/libexec/
PROGRAM_NAME=check_bandwidth.py

install:
	@echo "Install plugin to directory: $(INSTALL_PATH)"	
	@install $(PROGRAM_NAME) $(INSTALL_PATH)/$(PROGRAM_NAME)
	@echo "$(PROGRAM_NAME): installed"
uninstall:
	@echo "Remove plugin from directory: $(INSTALL_PATH)"	
	@rm -f $(PROGRAM_NAME) $(INSTALL_PATH)/$(PROGRAM_NAME)
	@echo "$(PROGRAM_NAME): uninstalled"
