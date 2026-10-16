"""Lock the preregistration: writes SHA-256 + UTC timestamp. Re-run `--verify` any time."""
import hashlib, sys, datetime, pathlib
P = pathlib.Path("docs/PREREGISTRATION.md"); L = pathlib.Path("docs/PREREG.lock")
h = hashlib.sha256(P.read_bytes()).hexdigest()
if "--verify" in sys.argv:
    ok = L.read_text().split()[0] == h
    print("PREREG INTACT" if ok else "PREREG MODIFIED -> log in docs/deviations.md"); sys.exit(0 if ok else 1)
L.write_text(f"{h}  locked_utc={datetime.datetime.now(datetime.timezone.utc).isoformat()}\n")
print("locked", h)
