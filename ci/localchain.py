"""Local, cancellation-proof chain: tail-only, small classes, violators, then the full
class family on every base variant. Single core, so index 0 only for the big spaces."""
import os, sys, time
sys.path.insert(0, ".")
import mega, rtl_ci as R

t0 = time.time()
P0 = R.load()
mega.gate(P0)

print("=== stage 1: tail-only, both joins, indices 0-2 ===", flush=True)
import tail_sweep as T
for j in ("lf", "crlf"):
    T.run(0, 1 << 18, j, [0, 1, 2])
print("stage 1 done %.0fs" % (time.time() - t0), flush=True)

print("=== stage 2: classes of at most 6 letters, 7 bases, indices 0-2 ===", flush=True)
os.environ["MAXK"] = "6"
import smallclass
smallclass.run()
print("stage 2 done %.0fs" % (time.time() - t0), flush=True)

print("=== stage 3: 2^25 violators, as-is base, index 0 ===", flush=True)
mega.IDX = (0,)
norm = [p.encode() for p in P0]
flip = [R.flips(p).encode() for p in P0]
mega.sweep(norm, flip, [None] * 273, 0, 1 << 25, (b"\n\n", b"\r\n\r\n"), "viol-as-is-idx0", [])
print("stage 3 done %.0fs" % (time.time() - t0), flush=True)

print("=== stage 4: full 2^21 class family, six base variants, index 0 ===", flush=True)
for v in mega.VARIANTS:
    PV = mega.apply_variant(P0, v)
    norm = [p.encode() for p in PV]
    flip = [R.flips(p).encode() for p in PV]
    let, bits = mega.first_axes(PV)
    print("variant %s axes=%s" % (v, "".join(let)), flush=True)
    mega.sweep(norm, flip, bits, 0, 1 << 21, (b"\n\n", b"\r\n\r\n" if v != "CLWS" else b"\r\n"),
               "class-%s-idx0" % v, [])
print("CHAIN DONE %.0fs" % (time.time() - t0), flush=True)
