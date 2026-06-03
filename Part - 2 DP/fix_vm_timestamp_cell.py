# =============================================================================
# VIRTUAL LAB FIX: Run this script OR copy the cell below into the FIRST
# code cell of your notebook when executing in the virtual lab.
# This ensures the VM ID and timestamp are captured and printed.
# =============================================================================

"""
Copy this as the FIRST CODE CELL in your notebook (before any imports).
This satisfies the assignment requirement:
  'The timestamp of the execution, Virtual Machine ID shall be
   fetched & printed in the top of the Python notebook.'
"""

FIRST_CELL_CODE = '''
import os
import time
import socket
import platform

# ============================================================
# VIRTUAL LAB EXECUTION METADATA
# (Required by assignment — must appear at top of notebook)
# ============================================================
print("=" * 65)
print(" BITS PILANI — DRL Assignment 1, Part 2: Drone Rescue DP")
print("=" * 65)
print(f"  Group ID         : 151")
print(f"  Student          : Abhinav Mandloi")
print(f"  Execution Date   : {time.strftime('%d %B %Y')}")
print(f"  Execution Time   : {time.strftime('%H:%M:%S IST')}")
print(f"  Virtual Machine  : {socket.gethostname()}")
print(f"  OS               : {platform.system()} {platform.release()}")
print(f"  Python Version   : {platform.python_version()}")
print("=" * 65)
print("  ✅ Timestamp and VM ID captured successfully")
print("=" * 65)
'''

if __name__ == "__main__":
    print("Paste the following as the FIRST code cell in your notebook:")
    print("-" * 60)
    print(FIRST_CELL_CODE)
