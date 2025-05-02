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

def run_test_case(tc_id):
    print(f"\n========================")
    print(f"🧪 Running Test Case: {tc_id}")
    print(f"========================")

    # Step 1: Reset all remote state
    reset_all_nodes()
    time.sleep(1)

    # Step 2: Upload valid fragments/fingerprints
    run_all_pipeline()

    # Step 3: Inject test case-specific modifications
    if tc_id == "TC1":
        pass  # All intact
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
        overwrite_file(2, "fragment_2.bin", "CORRUPTED-5")
    elif tc_id == "TC6":
        overwrite_file(1, "fragment_1.bin", "BAD-FRAG-6A")
        overwrite_file(2, "fragment_2.bin", "BAD-FRAG-6B")
    elif tc_id == "TC7":
        overwrite_file(0, "fragment_0.bin", "BAD-FRAG-7A")
        overwrite_file(1, "fragment_1.bin", "BAD-FRAG-7B")
        overwrite_file(2, "fragment_2.bin", "BAD-FRAG-7C")
    elif tc_id == "TC8":
        delete_file(1, "fingerprint_1.txt")
    elif tc_id == "TC9":
        delete_file(1, "fragment_1.bin")
        delete_file(1, "fingerprint_1.txt")
    elif tc_id == "TC10":
        overwrite_file(1, "fingerprint_1.txt", "1234567890abcdef")
    elif tc_id == "TC11":
        delete_file(1, "fragment_1.bin")
        overwrite_file(2, "fragment_2.bin", "MIXED-ERROR-TC11")
    elif tc_id == "TC12":
        overwrite_file(3, "fragment_3.bin", "BAD-BUT-UNUSED-TC12")
    elif tc_id == "TC13":
        delete_file(3, "fragment_3.bin")
    elif tc_id == "TC14":
        delete_file(3, "fragment_3.bin")
        delete_file(3, "fingerprint_3.txt")
    elif tc_id == "TC15":
        overwrite_file(3, "fingerprint_3.txt", "wrongfingerprintTC15")
    elif tc_id == "TC16":
        overwrite_file(3, "fragment_3.bin", "BAD")
        overwrite_file(3, "fingerprint_3.txt", "wrongFP-TC16")
    elif tc_id == "TC17":
        delete_file(4, "fragment_4.bin")
        delete_file(4, "fingerprint_4.txt")
    else:
        print("❌ Unknown Test Case ID.")
        return

    # Step 4: Run verify + reconstruct
    run_verify_and_reconstruct()

    # Step 5: Show final result
    show_result()


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 run_tc.py TC<number>")
    else:
        run_test_case(sys.argv[1])