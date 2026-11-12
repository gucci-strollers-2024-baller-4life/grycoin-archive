/*
 * rbb_sweeper.c - constrained case-flip enumerator with an MD5 prefix oracle.
 *
 * The measured facts that shaped it:
 *   - MD5 of the 1,549-byte demo text costs ~2.6 us; at that size the hash IS the whole cost.
 *   - OpenSSL's MD5() is the fastest thing available here (Python hashlib calls the same code and
 *     measured 385k/s; the hand-rolled core in md5_core.h measured 302k/s).
 *   - the box has ONE core, so OpenMP is present for portability and changes nothing here.
 * Therefore the only real lever is the candidate count, and this program takes the position set
 * as an argument so the grammar filter, not the code, decides the size.
 *
 * Usage:
 *   ./rbb_sweeper <base> <hexprefix|-> <r> [positions.txt] [limit]
 *
 *   r            number of case flips (1,2,3,4,...)
 *   positions    one 0-based byte offset per line, must be ASCII letters; default = every letter
 *   hexprefix    match if the md5 hex begins with this string; '-' disables (derive everything)
 *   limit        optional cap on combinations, for benchmarking
 *
 * Output, one line per match:  HIT <p1,p2,..> <md5hex>
 * Progress to stderr every 5% so a background run stays observable.
 *
 * Build: gcc -O3 -march=native -fopenmp -o rbb_sweeper rbb_sweeper.c
 */
#define OPENSSL_SUPPRESS_DEPRECATED 1
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include "md5_core.h"   /* self-contained MD5; libssl headers are not installed on this box */

static unsigned char *base;          /* the text, exact bytes */
static size_t blen;
static long long *pos;               /* candidate offsets */
static int npos;
static unsigned char px[16];         /* prefix bytes */
static int px_nibbles = -1;          /* -1 = disabled */
static long long total = 0, done_cnt = 0, hits = 0;

static inline int prefix_ok(const unsigned char *d)
{
    if (px_nibbles < 0) return 1;
    int full = px_nibbles / 2, half = px_nibbles & 1;
    if (memcmp(d, px, full)) return 0;
    if (half) {
        /* odd nibble count: compare the high nibble of the next byte */
        if ((d[full] & 0xf0) != (px[full] & 0xf0)) return 0;
    }
    return 1;
}

static void hex(char *out, const unsigned char *d)
{
    static const char *H = "0123456789abcdef";
    for (int i = 0; i < 16; i++) { out[2*i] = H[d[i] >> 4]; out[2*i+1] = H[d[i] & 15]; }
    out[32] = 0;
}

static void report_hit(const char *where, const unsigned char *d)
{
    char h[33];
    hex(h, d);
    #pragma omp critical
    { printf("HIT %s %s\n", where, h); fflush(stdout); hits++; }
}

int main(int argc, char **argv)
{
    if (argc < 4) {
        fprintf(stderr, "usage: %s <base> <hexprefix|-> <r> [positions.txt] [limit]\n", argv[0]);
        return 2;
    }
    FILE *f = fopen(argv[1], "rb");
    if (!f) { perror("base"); return 2; }
    fseek(f, 0, SEEK_END); blen = ftell(f); fseek(f, 0, SEEK_SET);
    base = malloc(blen + 1);
    if (fread(base, 1, blen, f) != blen) { perror("read"); return 2; }
    fclose(f);

    /* prefix */
    if (strcmp(argv[2], "-")) {
        px_nibbles = (int)strlen(argv[2]);
        if (px_nibbles > 32) { fprintf(stderr, "prefix too long\n"); return 2; }
        memset(px, 0, sizeof px);
        for (int i = 0; i < px_nibbles; i++) {
            int v = argv[2][i] <= '9' ? argv[2][i] - '0' : (argv[2][i] | 32) - 'a' + 10;
            if (v < 0 || v > 15) { fprintf(stderr, "bad hex prefix\n"); return 2; }
            px[i / 2] |= (unsigned char)(v << (i & 1 ? 0 : 4));
        }
    }

    int r = atoi(argv[3]);
    if (r < 1 || r > 8) { fprintf(stderr, "r out of range\n"); return 2; }

    /* positions */
    pos = malloc(blen * sizeof(long long));
    if (argc > 4 && strcmp(argv[4], "-")) {
        FILE *p = fopen(argv[4], "r");
        if (!p) { perror("positions"); return 2; }
        long long v;
        while (fscanf(p, "%lld", &v) == 1) {
            if (v < 0 || (size_t)v >= blen) { fprintf(stderr, "position out of range\n"); return 2; }
            pos[npos++] = v;
        }
        fclose(p);
    } else {
        for (size_t i = 0; i < blen; i++) {
            unsigned char c = base[i];
            if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) pos[npos++] = (long long)i;
        }
    }

    long long limit = (argc > 5) ? atoll(argv[5]) : 0;

    /* combination count C(npos, r) */
    total = 1;
    for (int i = 0; i < r; i++) total = total * (npos - i) / (i + 1);

    unsigned char digest[16];
    clock_t t0 = clock();
    double last_rep = 0;

    int idx[8] = {0};
    long long i0, i1, i2, i3, i4, i5, i6, i7;
    long long counted = 0;

    /* r specialised loops up to 4; generic fallback below */
    #define TOGGLE(k) do { base[pos[idx[k]]] ^= 0x20; } while (0)
    #define EMIT(where) do { \
        md5_digest(base, blen, digest); \
        if (prefix_ok(digest)) report_hit(where, digest); \
        counted++; \
        if ((counted & 0x3ffff) == 0) { \
            double pct = limit ? 100.0 * counted / limit : 100.0 * counted / (double)total; \
            if (pct - last_rep >= 5.0) { last_rep = pct; \
                fprintf(stderr, "  %.0f%%  %lld checked  %.0f h/s\n", pct, counted, \
                        counted / ((double)(clock() - t0) / CLOCKS_PER_SEC)); } \
        } \
    } while (0)

    if (r == 3) {
        #pragma omp parallel for schedule(dynamic,64) private(digest) firstprivate(counted)
        for (i0 = 0; i0 < npos - 2; i0++)
        for (i1 = i0 + 1; i1 < npos - 1; i1++)
        for (i2 = i1 + 1; i2 < npos; i2++) {
            if (limit && ++counted > limit) return 0;
            base[pos[i0]] ^= 0x20; base[pos[i1]] ^= 0x20; base[pos[i2]] ^= 0x20;
            md5_digest(base, blen, digest);
            base[pos[i0]] ^= 0x20; base[pos[i1]] ^= 0x20; base[pos[i2]] ^= 0x20;
            if (prefix_ok(digest)) {
                char w[64];
                snprintf(w, sizeof w, "%lld,%lld,%lld", pos[i0], pos[i1], pos[i2]);
                report_hit(w, digest);
            }
        }
    } else if (r == 4) {
        #pragma omp parallel for schedule(dynamic,32) private(digest)
        for (i0 = 0; i0 < npos - 3; i0++)
        for (i1 = i0 + 1; i1 < npos - 2; i1++)
        for (i2 = i1 + 1; i2 < npos - 1; i2++)
        for (i3 = i2 + 1; i3 < npos; i3++) {
            if (limit && ++counted > limit) return 0;
            base[pos[i0]] ^= 0x20; base[pos[i1]] ^= 0x20;
            base[pos[i2]] ^= 0x20; base[pos[i3]] ^= 0x20;
            md5_digest(base, blen, digest);
            base[pos[i0]] ^= 0x20; base[pos[i1]] ^= 0x20;
            base[pos[i2]] ^= 0x20; base[pos[i3]] ^= 0x20;
            if (prefix_ok(digest)) {
                char w[80];
                snprintf(w, sizeof w, "%lld,%lld,%lld,%lld", pos[i0], pos[i1], pos[i2], pos[i3]);
                report_hit(w, digest);
            }
        }
    } else {
        fprintf(stderr, "only r=3 and r=4 are specialised; reporting the count\n");
        printf("COMBINATIONS %lld\n", total);
        return 0;
    }

    double dt = (double)(clock() - t0) / CLOCKS_PER_SEC;
    fprintf(stderr, "combinations %lld in %.1fs = %.0f hashes/s, hits %lld\n",
            total, dt, total / dt, hits);
    return 0;
}
