import sys, hashlib, re, itertools
import demo_oracle

ESCROW = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"

with open("demo_base.txt", "r") as f:
    base_text = f.read()

paras = base_text.split("\n\n")

total_tested = 0
total_3c6 = 0
escrow_matches = []
hits_3c6 = []

def test_candidate(text, family, desc, flips_info=None):
    global total_tested, total_3c6
    total_tested += 1
    d = hashlib.md5(text.encode('utf-8')).digest()
    hex_md5 = d.hex()
    if hex_md5.startswith("3c6"):
        total_3c6 += 1
        words, addr = demo_oracle.derive(d)
        is_escrow = (addr == ESCROW)
        hit_record = {
            "family": family,
            "desc": desc,
            "md5": hex_md5,
            "words": words,
            "addr": addr,
            "is_escrow": is_escrow,
            "flips": flips_info
        }
        hits_3c6.append(hit_record)
        print(f"[3c6 HIT!] {family} | {desc} | md5: {hex_md5} | addr: {addr} | MATCH: {is_escrow}")
        if is_escrow:
            escrow_matches.append(hit_record)
            print(f"!!! SUCCESS !!! Escrow matched by: {desc}")
        return True
    return False

def flip_char(text, idx):
    c = text[idx]
    if c.islower():
        c_new = c.upper()
    elif c.isupper():
        c_new = c.lower()
    else:
        c_new = c
    return text[:idx] + c_new + text[idx+1:]

def flip_indices(text, indices):
    chars = list(text)
    for idx in indices:
        c = chars[idx]
        if c.islower():
            chars[idx] = c.upper()
        elif c.isupper():
            chars[idx] = c.lower()
    return "".join(chars)

print("Starting Hypothesis Battery...")

# -------------------------------------------------------------
# FAMILY 1: Paragraph-Level Selection Subsets (2^10 = 1024 per mode)
# -------------------------------------------------------------
print("--- Family 1: Paragraph Subsets & Boundary Rules ---")
for p_mask in range(1024):
    selected_paras = [i for i in range(10) if (p_mask & (1 << i))]
    
    # Mode 1a: Standard Stage 1 rule (first letter down, last letter up)
    mod_paras = list(paras)
    for p in selected_paras:
        txt = mod_paras[p]
        if not txt: continue
        # first letter
        f_idx = 0
        while f_idx < len(txt) and not txt[f_idx].isalpha(): f_idx += 1
        # last letter
        l_idx = len(txt) - 1
        while l_idx >= 0 and not txt[l_idx].isalpha(): l_idx -= 1
        
        c_list = list(txt)
        if f_idx < len(txt): c_list[f_idx] = c_list[f_idx].lower()
        if l_idx >= 0: c_list[l_idx] = c_list[l_idx].upper()
        mod_paras[p] = "".join(c_list)
    test_candidate("\n\n".join(mod_paras), "F1_para_subsets", f"Mode 1a (first down, last up) mask={p_mask} paras={selected_paras}")

    # Mode 1b: Exact first char down, exact last char up
    mod_paras = list(paras)
    for p in selected_paras:
        txt = mod_paras[p]
        if not txt: continue
        c_list = list(txt)
        c_list[0] = c_list[0].lower()
        c_list[-1] = c_list[-1].upper()
        mod_paras[p] = "".join(c_list)
    test_candidate("\n\n".join(mod_paras), "F1_para_subsets", f"Mode 1b (exact boundary) mask={p_mask} paras={selected_paras}")

    # Mode 1c: Case invert first alpha and last alpha
    mod_paras = list(paras)
    for p in selected_paras:
        txt = mod_paras[p]
        if not txt: continue
        f_idx = 0
        while f_idx < len(txt) and not txt[f_idx].isalpha(): f_idx += 1
        l_idx = len(txt) - 1
        while l_idx >= 0 and not txt[l_idx].isalpha(): l_idx -= 1
        c_list = list(txt)
        if f_idx < len(txt): c_list[f_idx] = c_list[f_idx].upper() if c_list[f_idx].islower() else c_list[f_idx].lower()
        if l_idx >= 0: c_list[l_idx] = c_list[l_idx].upper() if c_list[l_idx].islower() else c_list[l_idx].lower()
        mod_paras[p] = "".join(c_list)
    test_candidate("\n\n".join(mod_paras), "F1_para_subsets", f"Mode 1c (case invert boundary) mask={p_mask} paras={selected_paras}")

    # Mode 1d: First alpha down only
    mod_paras = list(paras)
    for p in selected_paras:
        txt = mod_paras[p]
        if not txt: continue
        f_idx = 0
        while f_idx < len(txt) and not txt[f_idx].isalpha(): f_idx += 1
        c_list = list(txt)
        if f_idx < len(txt): c_list[f_idx] = c_list[f_idx].lower()
        mod_paras[p] = "".join(c_list)
    test_candidate("\n\n".join(mod_paras), "F1_para_subsets", f"Mode 1d (first down only) mask={p_mask} paras={selected_paras}")

    # Mode 1e: Last alpha up only
    mod_paras = list(paras)
    for p in selected_paras:
        txt = mod_paras[p]
        if not txt: continue
        l_idx = len(txt) - 1
        while l_idx >= 0 and not txt[l_idx].isalpha(): l_idx -= 1
        c_list = list(txt)
        if l_idx >= 0: c_list[l_idx] = c_list[l_idx].upper()
        mod_paras[p] = "".join(c_list)
    test_candidate("\n\n".join(mod_paras), "F1_para_subsets", f"Mode 1e (last up only) mask={p_mask} paras={selected_paras}")

print(f"Done Family 1. Total tested so far: {total_tested}")

# -------------------------------------------------------------
# FAMILY 2: Specific Rule Paragraph Selection Sets
# -------------------------------------------------------------
print("--- Family 2: Specific Rule Paragraph Sets ---")
rule_sets = {
    "non_ITASM": [2, 3, 5, 6, 7],
    "non_SATOSHI": [2, 3, 6, 7],
    "ITASM": [0, 1, 4, 8, 9],
    "SATOSHI": [0, 1, 4, 5, 8, 9],
    "has_signs": [3, 4, 5, 7],
    "has_quotes": [1, 2, 3, 5, 6],
    "has_numbers": [0, 1, 8],
    "has_I": [0, 4, 5, 8],
    "has_Satoshi_Bitcointalk": [4],
    "has_solution": [2, 3, 7],
    "has_example": [0, 2, 8],
    "all_paras": list(range(10)),
}

for r_name, p_set in rule_sets.items():
    # Boundary flips
    for mode_name, first_mode, last_mode in [
        ("first_down_last_up", "lower", "upper"),
        ("first_up_last_down", "upper", "lower"),
        ("both_upper", "upper", "upper"),
        ("both_lower", "lower", "lower"),
        ("case_invert", "invert", "invert"),
    ]:
        mod_paras = list(paras)
        for p in p_set:
            txt = mod_paras[p]
            f_idx = 0
            while f_idx < len(txt) and not txt[f_idx].isalpha(): f_idx += 1
            l_idx = len(txt) - 1
            while l_idx >= 0 and not txt[l_idx].isalpha(): l_idx -= 1
            c_list = list(txt)
            if f_idx < len(txt):
                if first_mode == "lower": c_list[f_idx] = c_list[f_idx].lower()
                elif first_mode == "upper": c_list[f_idx] = c_list[f_idx].upper()
                elif first_mode == "invert": c_list[f_idx] = c_list[f_idx].upper() if c_list[f_idx].islower() else c_list[f_idx].lower()
            if l_idx >= 0:
                if last_mode == "lower": c_list[l_idx] = c_list[l_idx].lower()
                elif last_mode == "upper": c_list[l_idx] = c_list[l_idx].upper()
                elif last_mode == "invert": c_list[l_idx] = c_list[l_idx].upper() if c_list[l_idx].islower() else c_list[l_idx].lower()
            mod_paras[p] = "".join(c_list)
        test_candidate("\n\n".join(mod_paras), "F2_rule_sets", f"Rule {r_name} mode={mode_name}")

print(f"Done Family 2. Total tested so far: {total_tested}")

# -------------------------------------------------------------
# FAMILY 3: Quoted & Mentioned Pointer / Text Element Flips
# -------------------------------------------------------------
print("--- Family 3: Quoted & Mentioned Pointer Flips ---")
# Explicit mentions in text:
# 1. "n" in P2 -> "N"
# 2. "capitalizatioN" in P2 -> "capitalization" or P1 "capitalization." -> "capitalizatioN."
# 3. "I" at P4 -> "i"
# 4. "himself" at P4 -> "himselF"
# 5. "I" at P5 -> "i"
# 6. "I" at P6 -> "i"
# 7. "himself" at P6 -> "himselF"

# Test all combinations of these 7 specific pointer transformations
pointer_items = [
    ("P1_capitalization", ("capitalization.", "capitalizatioN.")),
    ("P2_n", ('"n"', '"N"')),
    ("P2_capitalizatioN", ('"capitalizatioN"', '"capitalization"')),
    ("P3_n", ('"n"', '"N"')),
    ("P4_I", ("I expected", "i expected")),
    ("P4_himself", ("himself.", "himselF.")),
    ("P5_I", ('"I"', '"i"')),
    ("P6_I", ('"I"', '"i"')),
    ("P6_himself", ('"himself"', '"himselF"')),
    ("P6_I_plain", ("changing \"I\" to \"i\"", "changing \"i\" to \"I\"")),
    ("P6_himself_plain", ("\"himself\" to \"himselF\"", "\"Himself\" to \"himselF\"")),
]

for k in range(1, len(pointer_items) + 1):
    for combo in itertools.combinations(pointer_items, k):
        txt = base_text
        desc_parts = []
        for name, (old_str, new_str) in combo:
            txt = txt.replace(old_str, new_str)
            desc_parts.append(name)
        test_candidate(txt, "F3_pointer_combos", "+".join(desc_parts))

print(f"Done Family 3. Total tested so far: {total_tested}")

# -------------------------------------------------------------
# FAMILY 4: Standalone 'I' and Pronoun Subsets
# -------------------------------------------------------------
print("--- Family 4: Standalone 'I' and Pronoun Subsets ---")
# Find all occurrences of standalone word "I"
i_indices = [m.start() for m in re.finditer(r'\bI\b', base_text)]
print(f"Found {len(i_indices)} standalone 'I's at offsets: {i_indices}")

for mask in range(1, 1 << len(i_indices)):
    chosen_indices = [i_indices[b] for b in range(len(i_indices)) if (mask & (1 << b))]
    # 4a: flip chosen 'I' to 'i'
    t1 = flip_indices(base_text, chosen_indices)
    test_candidate(t1, "F4_standalone_I", f"I->i mask={mask} offsets={chosen_indices}")
    
    # 4b: flip chosen 'I' to 'i' AND P4 himself -> himselF
    t2 = t1.replace("himself.", "himselF.")
    test_candidate(t2, "F4_standalone_I", f"I->i mask={mask} + P4 himself->himselF")
    
    # 4c: flip chosen 'I' to 'i' AND all 'himself' -> 'himselF'
    t3 = t1.replace("himself", "himselF")
    test_candidate(t3, "F4_standalone_I", f"I->i mask={mask} + all himself->himselF")

print(f"Done Family 4. Total tested so far: {total_tested}")

# -------------------------------------------------------------
# FAMILY 5: Word-Keyed Case Flips (Target terms)
# -------------------------------------------------------------
print("--- Family 5: Word-Keyed Case Flips ---")
target_words = [
    "signs", "solution", "Satoshi", "Bitcointalk", "himself", "capitalization",
    "method", "example", "block", "light", "mind", "script", "thinking",
    "format", "first", "stage", "previous", "paragraph", "reference", "Grycoin"
]

word_modes = [
    ("first_lower", lambda w: w[0].lower() + w[1:]),
    ("first_upper", lambda w: w[0].upper() + w[1:]),
    ("last_lower", lambda w: w[:-1] + w[-1].lower()),
    ("last_upper", lambda w: w[:-1] + w[-1].upper()),
    ("first_lower_last_upper", lambda w: w[0].lower() + w[1:-1] + w[-1].upper()),
    ("all_upper", lambda w: w.upper()),
    ("all_lower", lambda w: w.lower()),
    ("invert_all", lambda w: w.swapcase()),
]

for w in target_words:
    for m_name, transform in word_modes:
        if w in base_text:
            new_w = transform(w)
            txt = base_text.replace(w, new_w)
            test_candidate(txt, "F5_word_keyed", f"Word '{w}' mode={m_name} -> '{new_w}'")

# Combinations of key words (e.g. Satoshi + Bitcointalk + signs)
combo_words = ["signs", "solution", "Satoshi", "Bitcointalk", "himself"]
for k in range(2, len(combo_words) + 1):
    for word_sub in itertools.combinations(combo_words, k):
        for m_name in ["first_lower_last_upper", "last_upper", "all_upper"]:
            txt = base_text
            desc_list = []
            for w in word_sub:
                if m_name == "first_lower_last_upper":
                    new_w = w[0].lower() + w[1:-1] + w[-1].upper()
                elif m_name == "last_upper":
                    new_w = w[:-1] + w[-1].upper()
                elif m_name == "all_upper":
                    new_w = w.upper()
                txt = txt.replace(w, new_w)
                desc_list.append(f"{w}->{new_w}")
            test_candidate(txt, "F5_word_keyed_combos", f"Mode {m_name}: " + "+".join(desc_list))

print(f"Done Family 5. Total tested so far: {total_tested}")

# -------------------------------------------------------------
# FAMILY 6: Mid-Word & Vowel / Consonant Inversions (Block 29 style)
# -------------------------------------------------------------
print("--- Family 6: Mid-Word & Vowel Inversions ---")
# Block 29 flipped o,i -> O,I in "voice"
# Let's test flipping vowels in key words:
# "Bitcointalk" -> "BItcoIntalk", "BItcOIntalk"
# "Satoshi" -> "SatOshI", "SAtOshI"
# "himself" -> "hImsElf"
# "capitalization" -> "capItalIzatIon"
# "solution" -> "sOlutIOn"
# "signs" -> "sIgnS"

mid_word_replacements = [
    ("Bitcointalk", "BItcoIntalk"),
    ("Bitcointalk", "BItcOintalk"),
    ("Bitcointalk", "BItcOIntalk"),
    ("Bitcointalk", "bitcointalk"),
    ("Satoshi's", "SatOshI's"),
    ("Satoshi's", "sAtOshI's"),
    ("Satoshi's", "SATOSHI'S"),
    ("himself", "hImsElf"),
    ("himself", "himsElF"),
    ("capitalization", "capItalIzatIon"),
    ("capitalization", "capitalizatioN"),
    ("solution", "sOlutIOn"),
    ("solution", "solutioN"),
    ("signs", "sIgnS"),
    ("signs", "signS"),
]

for old_w, new_w in mid_word_replacements:
    txt = base_text.replace(old_w, new_w)
    test_candidate(txt, "F6_midword_vowels", f"Replace '{old_w}' with '{new_w}'")

# All combinations of 2 or 3 mid-word replacements
for combo in itertools.combinations(mid_word_replacements, 2):
    txt = base_text
    desc = []
    for old_w, new_w in combo:
        txt = txt.replace(old_w, new_w)
        desc.append(f"{old_w}->{new_w}")
    test_candidate(txt, "F6_midword_vowels_combos", "+".join(desc))

print(f"Done Family 6. Total tested so far: {total_tested}")

# -------------------------------------------------------------
# FAMILY 7: Number/Stride & Position Pointer Rules
# -------------------------------------------------------------
print("--- Family 7: Number/Stride Pointer Rules ---")
# Numbers mentioned: 77, 29, 13, 10, 350, 3c6
numbers = [77, 29, 13, 10, 350, 21, 2, 1, 4, 6]

for num in numbers:
    # 7a: Flip character at index num (0-based and 1-based)
    for pos in [num, num - 1, num + 1]:
        if 0 <= pos < len(base_text) and base_text[pos].isalpha():
            t = flip_char(base_text, pos)
            test_candidate(t, "F7_numeric_pointers", f"Flip char at pos={pos} (from num={num})")
            
            # Stated pair + pos
            t_pair = flip_indices(base_text, [535, 718, pos]) if base_text[535]=='I' else base_text
            test_candidate(t_pair, "F7_numeric_pointers", f"Stated pair + pos={pos}")

    # 7b: Flip character at multiples of num
    for mult in range(1, len(base_text) // num + 1):
        pos_list = [m * num for m in range(1, mult + 1) if m * num < len(base_text) and base_text[m * num].isalpha()]
        if pos_list:
            t = flip_indices(base_text, pos_list)
            test_candidate(t, "F7_numeric_pointers", f"Flip chars at multiples of {num} up to k={mult}: {pos_list}")

    # 7c: Flip word at word index num
    words_list = re.split(r'(\s+)', base_text)
    # count non-space words
    word_tokens = [(i, w) for i, w in enumerate(words_list) if w.strip()]
    if num < len(word_tokens):
        idx, w = word_tokens[num]
        w_mod = w[0].lower() + w[1:-1] + w[-1].upper() if len(w) > 1 else w.swapcase()
        words_mod = list(words_list)
        words_mod[idx] = w_mod
        test_candidate("".join(words_mod), "F7_numeric_pointers", f"Flip word #{num} ('{w}' -> '{w_mod}')")

print(f"Done Family 7. Total tested so far: {total_tested}")

# -------------------------------------------------------------
# FAMILY 8: Punctuation & Quote Adjacent Letter Flips
# -------------------------------------------------------------
print("--- Family 8: Punctuation & Quote Adjacent Flips ---")
# Find positions adjacent to quotes "
quote_positions = [m.start() for m in re.finditer(r'"', base_text)]
print(f"Quote positions ({len(quote_positions)}): {quote_positions}")

# Letters before/after quotes
quote_adj_indices = []
for q in quote_positions:
    if q > 0 and base_text[q-1].isalpha(): quote_adj_indices.append(q-1)
    if q < len(base_text)-1 and base_text[q+1].isalpha(): quote_adj_indices.append(q+1)

quote_adj_indices = sorted(list(set(quote_adj_indices)))
print(f"Quote-adjacent letter indices ({len(quote_adj_indices)}): {quote_adj_indices}")

for k in range(1, min(6, len(quote_adj_indices) + 1)):
    for combo in itertools.combinations(quote_adj_indices, k):
        t = flip_indices(base_text, list(combo))
        test_candidate(t, "F8_quote_adjacent", f"Flip quote-adj indices k={k}: {combo}")

# Sentence end letters (letters immediately preceding '.')
period_positions = [m.start() for m in re.finditer(r'\.', base_text)]
sent_end_indices = [p-1 for p in period_positions if p > 0 and base_text[p-1].isalpha()]
print(f"Sentence end letter indices ({len(sent_end_indices)}): {sent_end_indices}")

for mask in range(1, 1 << len(sent_end_indices)):
    chosen = [sent_end_indices[b] for b in range(len(sent_end_indices)) if (mask & (1 << b))]
    t = flip_indices(base_text, chosen)
    test_candidate(t, "F8_sentence_end", f"Flip sent-end indices mask={mask}: {chosen}")

print(f"Done Family 8. Total tested so far: {total_tested}")

# -------------------------------------------------------------
# FAMILY 9: Sentence-Level Boundary Flips
# -------------------------------------------------------------
print("--- Family 9: Sentence-Level Boundary Flips ---")
# Break text into sentences while keeping exact indices
sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', base_text) if s.strip()]
print(f"Total sentences: {len(sentences)}")

for s_mask in range(1, min(1024, 1 << len(sentences))):
    # Test first 1024 sentence masks with first down, last up
    txt = base_text
    # apply flips to sentences in s_mask
    s_idx = 0
    for match in re.finditer(r'(?<=[.!?])\s+|\Z', base_text):
        pass # we can test via regex string replaces for sentence bounds
    
print(f"Done Family 9. Total tested so far: {total_tested}")

# -------------------------------------------------------------
# FAMILY 10: NAGY / STNM / Anagram Capital Scatter
# -------------------------------------------------------------
print("--- Family 10: Anagram Capital Scatter ---")
# Find all capital letters in base_text
cap_indices = [i for i, c in enumerate(base_text) if c.isupper()]
print(f"Capital letter indices ({len(cap_indices)}): {cap_indices}")
cap_chars = [base_text[i] for i in cap_indices]
print(f"Capitals: {cap_chars}")

# Family name NAGY: A, G, Y, N
# Try toggling combinations of capital letters to lowercase
for k in range(1, len(cap_indices) + 1):
    for combo in itertools.combinations(cap_indices, k):
        t = flip_indices(base_text, list(combo))
        test_candidate(t, "F10_cap_scatter", f"Capitals down k={k} indices={combo}")

print(f"Done Family 10. Total tested so far: {total_tested}")

# -------------------------------------------------------------
# FAMILY 11: Stated Pair + Single/Double Flips Sweep
# -------------------------------------------------------------
print("--- Family 11: Stated Pair + Single/Double Flips Sweep ---")
# Stated pair in text:
# P4 first 'I' (pos 535) -> 'i'
# P4 last 'himself.' -> 'f' (pos 718) -> 'F' ('himselF.')
p4_i_pos = 535
p4_f_pos = 718

stated_pair_text = flip_indices(base_text, [p4_i_pos, p4_f_pos])
test_candidate(stated_pair_text, "F11_stated_pair", "Stated pair {I@535->i, f@718->F} alone")

# Stated pair + 1 flip anywhere in text
for pos in range(len(base_text)):
    if base_text[pos].isalpha():
        t = flip_char(stated_pair_text, pos)
        test_candidate(t, "F11_stated_pair_plus_1", f"Stated pair + pos={pos} char='{base_text[pos]}'")

print(f"Done Family 11. Total tested so far: {total_tested}")

# -------------------------------------------------------------
# FAMILY 12: Compound / Hybrid Multi-Rule Models
# -------------------------------------------------------------
print("--- Family 12: Compound Multi-Rule Models ---")
# Compound Model 1: Non-ITASM paras (boundary flips) + Stated pair
non_itasm_paras = [2, 3, 5, 6, 7]
mod_paras = list(paras)
for p in non_itasm_paras:
    txt = mod_paras[p]
    f_idx = 0
    while f_idx < len(txt) and not txt[f_idx].isalpha(): f_idx += 1
    l_idx = len(txt) - 1
    while l_idx >= 0 and not txt[l_idx].isalpha(): l_idx -= 1
    c_list = list(txt)
    if f_idx < len(txt): c_list[f_idx] = c_list[f_idx].lower()
    if l_idx >= 0: c_list[l_idx] = c_list[l_idx].upper()
    mod_paras[p] = "".join(c_list)
t_hybrid1 = "\n\n".join(mod_paras)
test_candidate(t_hybrid1, "F12_compound", "Non-ITASM boundary flips")

# Hybrid 1 + P4 stated pair
t_hybrid1_pair = t_hybrid1.replace("I expected", "i expected").replace("himself.", "himselF.")
test_candidate(t_hybrid1_pair, "F12_compound", "Non-ITASM boundary flips + P4 stated pair")

# Compound Model 2: Paras containing "signs" (boundary flips)
signs_paras = [3, 4, 5, 7]
mod_paras = list(paras)
for p in signs_paras:
    txt = mod_paras[p]
    f_idx = 0
    while f_idx < len(txt) and not txt[f_idx].isalpha(): f_idx += 1
    l_idx = len(txt) - 1
    while l_idx >= 0 and not txt[l_idx].isalpha(): l_idx -= 1
    c_list = list(txt)
    if f_idx < len(txt): c_list[f_idx] = c_list[f_idx].lower()
    if l_idx >= 0: c_list[l_idx] = c_list[l_idx].upper()
    mod_paras[p] = "".join(c_list)
t_hybrid2 = "\n\n".join(mod_paras)
test_candidate(t_hybrid2, "F12_compound", "Signs paras boundary flips")

# Hybrid 2 + P4 stated pair
t_hybrid2_pair = t_hybrid2.replace("I expected", "i expected").replace("himself.", "himselF.")
test_candidate(t_hybrid2_pair, "F12_compound", "Signs paras boundary flips + P4 stated pair")

print(f"Done Family 12. Total tested so far: {total_tested}")

print("==================================================")
print(f"BATTERY COMPLETE.")
print(f"Total hypotheses tested: {total_tested}")
print(f"Total MD5 starting with 3c6: {total_3c6}")
print(f"Total Escrow Matches: {len(escrow_matches)}")
print("==================================================")
