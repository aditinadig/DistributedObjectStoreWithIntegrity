import subprocess
import time
from tc_utils import delete_file, overwrite_file, reset_all_nodes

def run_shell(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

def run_all_pipeline():
    out, err = run_shell("./run_all.sh")
    print(out)
    return out

def run_verify_and_reconstruct():
    run_shell("python3 verify_fragments.py")
    run_shell("python3 reconstruct_file.py")

def show_result():
    print("\n📄 Final reconstructed.txt content:\n")
    with open("reconstructed.txt", "r") as f:
        print(f.read())
    print("-" * 50)

def run_test_case(tc_id):
    print(f"\n========================")
    print(f"🧪 Running Test Case: {tc_id}")
    print(f"========================")

    # Step 1: Reset nodes
    reset_all_nodes()
    time.sleep(1)

    # Step 2: Upload valid fragments/fingerprints
    run_all_pipeline()

    # Step 3: Inject test case modifications
    if tc_id == "TC1":
        pass
    elif tc_id == "TC2":
        delete_file(1, "fragment_1.bin")
    elif tc_id == "TC3":
        delete_file(0, "fragment_0.bin")
        delete_file(1, "fragment_1.bin")
    elif tc_id == "TC4":
        delete_file(0, "fragment_0.bin")
        delete_file(1, "fragment_1.bin")
        delete_file(2, "fragment_2.bin")
    elif tc_id == "TC5":
        overwrite_file(2, "fragment_2.bin", "XXXXX\n")
    elif tc_id == "TC6":
        overwrite_file(1, "fragment_1.bin", "BAD1\n")
        overwrite_file(2, "fragment_2.bin", "BAD2\n")
    elif tc_id == "TC7":
        overwrite_file(0, "fragment_0.bin", "C0\n")
        overwrite_file(1, "fragment_1.bin", "C1\n")
        overwrite_file(2, "fragment_2.bin", "C2\n")
    elif tc_id == "TC8":
        delete_file(1, "fingerprint_1.txt")
    elif tc_id == "TC9":
        delete_file(1, "fragment_1.bin")
        delete_file(1, "fingerprint_1.txt")
    elif tc_id == "TC10":
        overwrite_file(1, "fingerprint_1.txt", "1234567890abcdef")
    elif tc_id == "TC11":
        delete_file(1, "fragment_1.bin")
        overwrite_file(2, "fragment_2.bin", "MIXED_ERROR\n")
    else:
        print("❌ Unknown Test Case ID.")
        return

    # Step 4: Re-run only verify + reconstruct
    run_verify_and_reconstruct()
    show_result()


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 run_tc.py TC<number>")
    else:
        run_test_case(sys.argv[1])