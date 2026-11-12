"""The 179-set transport sweep: paragraphs that carry a SATOSHI letter, moved under the
certified transport rule (first letter down, last letter up).

Selection axis
--------------
The chapter states its sign letters as {I,T,A,S,M}. Applying that test to the author's own
format example (grycoin block 2) yields five anomalies and breaks the FFWW quad. Applying the
six letters of SATOSHI {S,A,T,O,H,I} yields exactly four, 3(F) 4(F) 7(W) 8(W), with ¶5 I and
¶6 O both in-class. Under SATOSHI the chapter's sets are:

    out-of-class (anomalies)   94   the exclusion mask every earlier sweep used (as 118/120)
    in-class (carry a sign)   179   the positive rule, never used as the marked set

The chapter's instruction is "change only a couple of letters in their capitalization, for all
the paragraphs where you recognize the signs". Read positively, that marks the 179.

Lanes
-----
L1  179-set, paragraph edges, first-down + last-up, strict     (skip a paragraph that cannot move)
L2  179-set, paragraph edges, first-down + last-up, forced     (apply regardless)
L3   94-set, same two variants                                 (control against earlier closure)
L4  179-set, sentence edges, first-down + last-up, strict      (the demo's worked example is
                                                                sentence-level, CLUES §13.4)
L5  179-set, paragraph edges, inverted transport (first-up + last-down)

Serialisations: \n\n and \r\n\r\n, with and without trailing join, so the four certified forms.
Derivation: MD5 -> 12 BIP39 words -> m/44'/0'/0'/0/{0,1,2,44,76,77} -> P2PKH, coincurve lane,
validated against the certified stage-one pair before screening.

Reads:  ../wp_paras_br.json
Writes: ../sat_set_transport_results.json
"""
import hashlib, json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import sixteen_matrix as sm          # fast lane, validated in-script below

ESCROW = sm.ESCROW                    # 14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W
IDX = (0, 1, 2, 44, 76, 77)
ALPHABETS = {"SATOSHI": set("SATOSHI"), "AIMOST": set("AIMOST")}


def load():
    d = json.load(open(os.path.join(ROOT, "wp_paras_br.json"), encoding="utf-8"))
    ps = d if isinstance(d, list) else (d.get("paras") or list(d.values())[0])
    return [("\n".join(x) if isinstance(x, list) else x) for x in ps]


def first_i(s):
    for i, c in enumerate(s):
        if c.isalpha():
            return i
    return None


def last_i(s):
    for i in range(len(s) - 1, -1, -1):
        if s[i].isalpha():
            return i
    return None


def transport(s, strict=True, invert=False):
    """Move the capital from the unit's first letter to its last letter."""
    a, b = first_i(s), last_i(s)
    if a is None:
        return s, False
    if a == b:
        return s, False                      # one letter: nothing to transport
    q = list(s)
    if not invert:
        ok = (q[a].isupper() and q[b].islower()) if strict else True
        if not ok:
            return s, False
        q[a] = q[a].lower()
        q[b] = q[b].upper()
    else:
        ok = (q[a].islower() and q[b].isupper()) if strict else True
        if not ok:
            return s, False
        q[a] = q[a].upper()
        q[b] = q[b].lower()
    return "".join(q), True


SENT = re.compile(r"[^.!?]*[.!?]+|[^.!?]+$")


def mark_paras(paras, sel, strict=True, invert=False):
    out, moved = list(paras), 0
    for i in sel:
        out[i], ch = transport(out[i], strict=strict, invert=invert)
        moved += ch
    return out, moved


def mark_sentences(paras, sel, strict=True):
    out, moved = list(paras), 0
    for i in sel:
        parts = SENT.findall(out[i])
        if not parts:
            continue
        acc = []
        for p in parts:
            new, ch = transport(p, strict=strict)
            acc.append(new)
            moved += ch
        out[i] = "".join(acc)
    return out, moved


def serialisations(paras):
    for join, tag in ((b"\n\n", "LF"), (b"\r\n\r\n", "CRLF")):
        for trail in (False, True):
            yield join.join(p.encode() for p in paras) + (join if trail else b""), \
                tag + ("+t" if trail else "")


def main():
    sm.validate()                        # fast lane == pure-python harness, stage-one path
    paras = load()
    assert len(paras) == 273, len(paras)
    inits = [(first_i(p), p) for p in paras]
    for SIG_NAME, SIG in ALPHABETS.items():
      in_class = [i for i, (a, p) in enumerate(inits)
                  if a is not None and p[a].upper() in SIG]
      out_class = [i for i, (a, p) in enumerate(inits)
                   if a is not None and p[a].upper() not in SIG]
      print(f"\n=== alphabet {SIG_NAME} === in-class {len(in_class)}  out-class {len(out_class)}")
      assert len(in_class) + len(out_class) == 272, "one paragraph has no letters"

      # structural sub-sets of the in-class 178, for the two places the selection is arguable
      reprint = {230, 231, 232, 233, 234}                      # the hal_original.txt block
      subheads = {i for i, (a, p) in enumerate(inits)          # lowercase a) b) c) subheadings
                  if a is not None and p[a].islower()}
      no_reprint = [i for i in in_class if i not in reprint]
      no_subheads = [i for i in in_class if i not in subheads]
      print(f"subheading paragraphs ({len(subheads)}): {[i + 1 for i in sorted(subheads)]}")
      print(f"letterless paragraph: {[i + 1 for i, (a, _) in enumerate(inits) if a is None]}")
      lanes = [
          ("L1_in_para_strict", in_class, dict(strict=True), "para"),
          ("L2_in_para_forced", in_class, dict(strict=False), "para"),
          ("L3a_out_para_strict", out_class, dict(strict=True), "para"),
          ("L3b_out_para_forced", out_class, dict(strict=False), "para"),
          ("L4_in_sentence_strict", in_class, dict(strict=True), "sent"),
          ("L5_in_para_inverted", in_class, dict(strict=True, invert=True), "para"),
          ("L6_in_no_reprint_strict", no_reprint, dict(strict=True), "para"),
          ("L7_in_no_subheads_strict", no_subheads, dict(strict=True), "para"),
          ("L8_out_no_subheads_strict", [i for i in out_class if i not in subheads],
           dict(strict=True), "para"),
      ]

      t0, texts, results, hits = time.time(), 0, [], []
      for name, sel, kw, unit in lanes:
          if unit == "para":
              marked, moved = mark_paras(paras, sel, **kw)
          else:
              marked, moved = mark_sentences(paras, sel, **kw)
          # capital conservation check: transport must be net zero
          caps_in = sum(1 for p in paras for c in p if c.isupper())
          caps_out = sum(1 for p in marked for c in p if c.isupper())
          row = {"lane": name, "marked": len(sel), "units_moved": moved,
                 "caps_before": caps_in, "caps_after": caps_out,
                 "conserved": caps_in == caps_out, "texts": []}
          for blob, tag in serialisations(marked):
              texts += 1
              md5 = hashlib.md5(blob).hexdigest()
              addrs = sm.addrs(md5)
              rec = {"serialisation": tag, "md5": md5,
                     "bip39_head": sm.mnemonic(bytes.fromhex(md5)).split()[:4],
                     "addrs": {str(i): a for i, a in addrs.items()}}
              row["texts"].append(rec)
              for i, a in addrs.items():
                  if a == ESCROW:
                      hits.append({"lane": name, "serialisation": tag, "md5": md5, "index": i})
          results.append(row)
          print(f"  {name:24s} marked {len(sel):3d} units_moved {moved:3d} "
                f"caps {caps_in}->{caps_out} {'OK' if row['conserved'] else 'LEAK'} "
                f"{len(row['texts'])} texts")

      out = {"escrow": ESCROW, "indices": list(IDX), "sign_letters": SIG_NAME,
             "in_class": [i + 1 for i in in_class], "out_class": [i + 1 for i in out_class],
             "texts": texts, "derivations": texts * len(IDX),
             "elapsed_s": round(time.time() - t0, 2), "hits": hits, "lanes": results}
      json.dump(out, open(os.path.join(ROOT, f"sat_set_transport_results_{SIG_NAME}.json"), "w"), indent=1)
      print(f"\ntexts {texts} derivations {texts * len(IDX)} in {out['elapsed_s']}s "
            f"hits {len(hits)}")
      for h in hits:
          print("  HIT", h)


if __name__ == "__main__":
    main()
