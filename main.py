import argparse
from core.engine import PentestEngine
from core.logger import log_info

def main():
    # 1. Display banner
    print("="*50)
    print("      BlackICE – Intrusion Countermeasures Electronics")
    print("                 Version 0.1 – Alpha")
    print("="*50)

    # 2. Parse arguments
    parser = argparse.ArgumentParser(
        description="BlackICE: Modular Python-based Pentesting Framework"
    )
    parser.add_argument(
        "--target", "-t", help="Target IP or domain to scan", required=False
    )
    args = parser.parse_args()

    # 3. Prompt for target if not provided
    if args.target:
        target = args.target
    else:
        target = input("Enter target IP or domain: ").strip()

    # 4. Initialize engine
    engine = PentestEngine(target)

    # 5. Discover modules
    engine.discover_modules()

    # 6. List available modules
    print("\nModules Found:")
    for i, mod_name in enumerate(engine.modules, start=1):
        print(f"{i}. {mod_name}")

    # 7. Interactive module selection
    choice = input("\nEnter module number to run (or 'all' for all modules): ").strip()

    if choice.lower() == "all":
        engine.run_all()
    else:
        try:
            # Numeric selection
            if choice.isdigit():
                mod_index = int(choice) - 1
                module_name = list(engine.modules.keys())[mod_index]
            else:
                # Allow typing the module name
                module_name = choice
            engine.run_module(module_name)
        except Exception:
            print("Invalid module choice. Exiting.")

    log_info("Scan finished.")

if __name__ == "__main__":
    log_info("BlackICE started")
    main()

