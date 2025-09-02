import importlib
import os
from core.logger import log_info, log_error

MODULES_DIR = "modules"

class PentestEngine:
    def __init__(self, target):
        """
        Initialize the engine with a target (IP/domain)
        """
        self.target = target
        self.modules = {}

    def discover_modules(self):
        """
        Discover all Python modules in the modules/ folder
        """
        log_info("Discovering modules...")
        for file in os.listdir(MODULES_DIR):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]
                try:
                    module = importlib.import_module(f"modules.{module_name}")
                    self.modules[module_name] = module
                    log_info(f"Loaded module: {module_name}")
                except Exception as e:
                    log_error(f"Failed to load {module_name}: {e}")

    def run_module(self, module_name):
        """
        Run a specific module by name
        """
        if module_name in self.modules:
            try:
                log_info(f"Running module: {module_name} on target: {self.target}")
                self.modules[module_name].run(self.target)
            except Exception as e:
                log_error(f"Error running {module_name}: {e}")
        else:
            log_error(f"Module {module_name} not found")

    def run_all(self):
        """
        Run all discovered modules
        """
        log_info("Running all modules...")
        for module_name in self.modules:
            self.run_module(module_name)

