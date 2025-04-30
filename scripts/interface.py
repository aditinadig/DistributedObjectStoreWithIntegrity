from rich import print
from rich.prompt import Prompt
from rich.console import Console
import subprocess

console = Console()

def run_test_case():
    tc = Prompt.ask("Enter test case ID", default="TC1")
    subprocess.run(["python3", "test_cases/run_tc.py", tc])


def main_menu():
    while True:
        print("\n[bold yellow]🔧 Distributed Object Store - Main Menu[/bold yellow]")
        print("[1] Run a test case")
        print("[2] Exit")

        choice = Prompt.ask("Choose an option", choices=["1", "2"])
        if choice == "1":
            run_test_case()
        else:
            break

if __name__ == "__main__":
    main_menu()