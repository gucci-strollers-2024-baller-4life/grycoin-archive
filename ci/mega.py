"""One dispatch, every remaining family.

The 2^25 violator run 43574281869 was killed at 08:59:19 with 18 of 20 shards at the
finish line, so a queue of separate runs is fragile. This module runs, per shard and in
one job: the 2^25 violator space on the as-is base, the 2^21 class family on each of the
six base variants, and the 2^18 tail-only family. Every candidate is compared against
both escrows, and the gate prints the three certified base digests before anything runs.
"""
import hashlib, json, os, sys
import rtl_ci as R

VARIANTS = ["CLSN", "CLSS", "CLDB", "CLPX", "CLCR", "CLWS"]
IDX = (0, 1, 2)


def apply_variant(P, v):
    if v in ("CLSN", "CLSS"):
        P = [p.replace("\u00a0", " ") for p in P]
        if v == "CLSS":
            P = ["\n".join(l.rstrip(" ") for l in p.split("\n")) for p in P]
    elif v in ("CLDB", "CLPX", "CLCR"):
        rep = {"CLDB": " ", "CLPX": "", "CLCR": "\r\n"}[v]
        P = [p.replace("\n", rep) for p in P]
    return P


def gate(P):
    norm = [p.encode() for p in P]
    for sep, want in R.CERT.items():
        got = hashlib.md5(sep.join(norm)).hexdigest()
        assert got == want, ("base drift", sep, got, want)
    print("gate OK [MEGA]: bases 46a308c2 (LF) / bd07e6ee (CRLF) / e7f3720c (single CR) "
          "reproduced; targets %s" % "+".join(R.TARGETS.values()), flush=True)


def first_axes(P):
    let = sorted({next((c.upper() for c in p if c.isalpha()), None) for p in P} - {None})
    idx = {c: k for k, c in enumerate(let)}
    bits = []
    for p in P:
        c = next((c.upper() for c in p if c.isalpha()), None)
        bits.append(None if c is None else idx[c])
    return let, bits


def tail_axes(P):
    let = sorted({t for t in (next((c.upper() for c in reversed(p) if c.isalpha()), None)
                             for p in P) if t})
    idx = {c: k for k, c in enumerate(let)}
    bits = []
    for p in P:
        t = next((c.upper() for c in reversed(p) if c.isalpha()), None)
        bits.append(None if t is None else idx[t])
    return let, bits


def flips_tail(p):
    a = [i for i, c in enumerate(p) if c.isalpha()]
    if not a:
        return p
    b = list(p)
    b[a[-1]] = b[a[-1]].upper()
    return "".join(b)


def _chunk(job):
    (norm, flip, bits, seps, start, end) = job
    n = 0
    out = []
    for sep in seps:
        for mask in range(start, end):
            body = sep.join([norm[i] if (bits[i] is None or (mask >> bits[i]) & 1) else flip[i]
                             for i in range(len(norm))])
            d = hashlib.md5(body).hexdigest()
            n += 1
            for ix in IDX:
                a = R.addr(d, ix)
                if a in R.TARGETS:
                    out.append(dict(sep=repr(sep), mask=mask, idx=ix, md5=d, escrow=R.TARGETS[a]))
                    open("HIT_MEGA_%d_%d.txt" % (mask, ix), "wb").write(body)
    return n, out


def sweep(norm, flip, bits, start, end, seps, label, hits, procs=1):
    if procs > 1:
        lo = min(end, 1 << len(bits))
        step = max(1, (lo - start) // procs)
        jobs, a = [], start
        while a < lo:
            jobs.append((norm, flip, bits, seps, a, min(lo, a + step)))
            a += step
        import multiprocessing as mp
        with mp.Pool(len(jobs)) as pool:
            res = pool.map(_chunk, jobs)
        n = sum(r[0] for r in res)
        for r in res:
            hits.extend(r[1])
            for h in r[1]:
                print("***HIT", h, flush=True)
        print("DONE %-22s start=%d end=%d n=%d procs=%d" % (label, start, end, n, len(jobs)), flush=True)
        try:
            st = json.load(open("mega_progress.json"))
        except Exception:
            st = {"total": 0, "families": {}}
        st["total"] = st.get("total", 0) + n
        st["families"][label] = st["families"].get(label, 0) + n
        json.dump(st, open("mega_progress.json", "w"), indent=1)
        return n
    n = 0
    for sep in seps:
        for mask in range(start, min(end, 1 << len(bits))):
            body = sep.join([norm[i] if (bits[i] is None or (mask >> bits[i]) & 1) else flip[i]
                             for i in range(len(norm))])
            d = hashlib.md5(body).hexdigest()
            n += 1
            for ix in IDX:
                a = R.addr(d, ix)
                if a in R.TARGETS:
                    hits.append(dict(family=label, sep=repr(sep), mask=mask, idx=ix,
                                     md5=d, escrow=R.TARGETS[a]))
                    print("***HIT", hits[-1], flush=True)
                    open("HIT_MEGA_%s_%s_%d_%d.txt" % (label, "crlf" if len(sep) > 1 and sep != b"\n\n" else "lf", mask, ix), "wb").write(body)
    print("DONE %-22s start=%d end=%d n=%d" % (label, start, end, n), flush=True)
    try:
        st = json.load(open("mega_progress.json"))
    except Exception:
        st = {"total": 0, "families": {}}
    st["total"] = st.get("total", 0) + n
    st["families"][label] = st["families"].get(label, 0) + n
    json.dump(st, open("mega_progress.json", "w"), indent=1)
    return n


def main():
    mode = os.environ.get("MEGA_MODE", "shard")
    P0 = R.load()
    gate(P0)
    nclass = 1 << 21
    nviol = 1 << 25
    if mode == "local":
        class_ranges = [(0, nclass)]
        viol_ranges = [(0, nviol)]
    else:
        shard = int(os.environ.get("SHARD", "0"))
        span = nclass // 20
        cs = shard * span
        ce = nclass if shard == 19 else cs + span
        class_ranges = [(cs, ce)]
        vs = cs * 16
        ve = nviol if shard == 19 else ce * 16
        viol_ranges = [(vs, ve)]
    hits = []
    total = 0
    # A GitHub runner has more than one core; the shard step cannot pass extra env, so
    # shard mode defaults to four workers and local mode stays single-process.
    PROCS = int(os.environ.get("MEGA_PROCS", "4" if os.environ.get("MEGA_MODE") != "local" else "1"))
    SEPS = (b"\n\n", b"\r\n\r\n")
    # 1. violator space, as-is base, index 0
    norm = [p.encode() for p in P0]
    flip = [R.flips(p).encode() for p in P0]
    if not os.environ.get("MEGA_SKIP_VIOL"):
        for vs, ve in viol_ranges:
            total += sweep(norm, flip, [None] * 273, vs, ve, SEPS, "viol-as-is", hits, PROCS)
    # 2. class family on each base variant
    for v in VARIANTS:
        PV = apply_variant(P0, v)
        norm = [p.encode() for p in PV]
        flip = [R.flips(p).encode() for p in PV]
        let, bits = first_axes(PV)
        for sep2 in (b"\n\n", b"\r\n\r\n"):
            print("variant %s %r %s axes=%s" % (v, sep2, hashlib.md5(sep2.join(norm)).hexdigest()[:8], "".join(let)), flush=True)
        for cs, ce in class_ranges:
            total += sweep(norm, flip, bits, cs, ce, SEPS, "class-" + v, hits, PROCS)
    # 3. tail-only family
    norm = [p.encode() for p in P0]
    flip = [flips_tail(p).encode() for p in P0]
    let, bits = tail_axes(P0)
    print("tail axes n=%d %s" % (len(let), "".join(let)), flush=True)
    for cs, ce in class_ranges:
        total += sweep(norm, flip, bits, cs, ce, SEPS, "tail-only", hits, PROCS)
    print("MEGA DONE total=%d hits=%d" % (total, len(hits)), flush=True)
    json.dump(dict(total=total, hits=hits, mode=mode), open("mega_results.json", "w"), indent=1)


if __name__ == "__main__":
    main()
