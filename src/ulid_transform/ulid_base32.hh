#ifndef ULID_BASE32_HH
#define ULID_BASE32_HH

#include <stdint.h>

namespace ulid {

/**
 * Crockford's Base32
 * */
static const char Encoding[33] = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";

/**
 * dec stores decimal encodings for characters.
 * 0xFF indicates invalid character.
 * 48-57 are digits.
 * 65-90 are capital alphabets.
 * */
static const uint8_t dec[256] = {
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,

    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    /* 0     1     2     3     4     5     6     7  */
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    /* 8     9                                      */
    0x08, 0x09, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,

    /*    10(A) 11(B) 12(C) 13(D) 14(E) 15(F) 16(G) */
    0xFF, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10,
    /*17(H)     18(J) 19(K)       20(M) 21(N)       */
    0x11, 0xFF, 0x12, 0x13, 0xFF, 0x14, 0x15, 0xFF,
    /*22(P)23(Q)24(R) 25(S) 26(T)       27(V) 28(W) */
    0x16, 0x17, 0x18, 0x19, 0x1A, 0xFF, 0x1B, 0x1C,
    /*29(X)30(Y)31(Z)                               */
    0x1D, 0x1E, 0x1F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,

    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,

    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,

    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,

    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,

    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF
};

/**
 * Decode a base32 ULID string directly to 16 bytes, no intermediate ULID.
 * */
inline void DecodeBase32To(const char str[26], uint8_t dst[16])
{
    // timestamp
    dst[0] = (dec[(unsigned char)str[0]] << 5) | dec[(unsigned char)str[1]];
    dst[1] = (dec[(unsigned char)str[2]] << 3) | (dec[(unsigned char)str[3]] >> 2);
    dst[2] = (dec[(unsigned char)str[3]] << 6) | (dec[(unsigned char)str[4]] << 1) | (dec[(unsigned char)str[5]] >> 4);
    dst[3] = (dec[(unsigned char)str[5]] << 4) | (dec[(unsigned char)str[6]] >> 1);
    dst[4] = (dec[(unsigned char)str[6]] << 7) | (dec[(unsigned char)str[7]] << 2) | (dec[(unsigned char)str[8]] >> 3);
    dst[5] = (dec[(unsigned char)str[8]] << 5) | dec[(unsigned char)str[9]];
    // entropy
    dst[6] = (dec[(unsigned char)str[10]] << 3) | (dec[(unsigned char)str[11]] >> 2);
    dst[7] = (dec[(unsigned char)str[11]] << 6) | (dec[(unsigned char)str[12]] << 1) | (dec[(unsigned char)str[13]] >> 4);
    dst[8] = (dec[(unsigned char)str[13]] << 4) | (dec[(unsigned char)str[14]] >> 1);
    dst[9] = (dec[(unsigned char)str[14]] << 7) | (dec[(unsigned char)str[15]] << 2) | (dec[(unsigned char)str[16]] >> 3);
    dst[10] = (dec[(unsigned char)str[16]] << 5) | dec[(unsigned char)str[17]];
    dst[11] = (dec[(unsigned char)str[18]] << 3) | (dec[(unsigned char)str[19]] >> 2);
    dst[12] = (dec[(unsigned char)str[19]] << 6) | (dec[(unsigned char)str[20]] << 1) | (dec[(unsigned char)str[21]] >> 4);
    dst[13] = (dec[(unsigned char)str[21]] << 4) | (dec[(unsigned char)str[22]] >> 1);
    dst[14] = (dec[(unsigned char)str[22]] << 7) | (dec[(unsigned char)str[23]] << 2) | (dec[(unsigned char)str[24]] >> 3);
    dst[15] = (dec[(unsigned char)str[24]] << 5) | dec[(unsigned char)str[25]];
}

/**
 * Encode 16 bytes directly to a base32 ULID string, no intermediate ULID.
 * */
inline void EncodeBase32From(const uint8_t b[16], char dst[26])
{
    // timestamp
    dst[0] = Encoding[(b[0] & 224) >> 5];
    dst[1] = Encoding[b[0] & 31];
    dst[2] = Encoding[(b[1] & 248) >> 3];
    dst[3] = Encoding[((b[1] & 7) << 2) | ((b[2] & 192) >> 6)];
    dst[4] = Encoding[(b[2] & 62) >> 1];
    dst[5] = Encoding[((b[2] & 1) << 4) | ((b[3] & 240) >> 4)];
    dst[6] = Encoding[((b[3] & 15) << 1) | ((b[4] & 128) >> 7)];
    dst[7] = Encoding[(b[4] & 124) >> 2];
    dst[8] = Encoding[((b[4] & 3) << 3) | ((b[5] & 224) >> 5)];
    dst[9] = Encoding[b[5] & 31];
    // entropy
    dst[10] = Encoding[(b[6] & 248) >> 3];
    dst[11] = Encoding[((b[6] & 7) << 2) | ((b[7] & 192) >> 6)];
    dst[12] = Encoding[(b[7] & 62) >> 1];
    dst[13] = Encoding[((b[7] & 1) << 4) | ((b[8] & 240) >> 4)];
    dst[14] = Encoding[((b[8] & 15) << 1) | ((b[9] & 128) >> 7)];
    dst[15] = Encoding[(b[9] & 124) >> 2];
    dst[16] = Encoding[((b[9] & 3) << 3) | ((b[10] & 224) >> 5)];
    dst[17] = Encoding[b[10] & 31];
    dst[18] = Encoding[(b[11] & 248) >> 3];
    dst[19] = Encoding[((b[11] & 7) << 2) | ((b[12] & 192) >> 6)];
    dst[20] = Encoding[(b[12] & 62) >> 1];
    dst[21] = Encoding[((b[12] & 1) << 4) | ((b[13] & 240) >> 4)];
    dst[22] = Encoding[((b[13] & 15) << 1) | ((b[14] & 128) >> 7)];
    dst[23] = Encoding[(b[14] & 124) >> 2];
    dst[24] = Encoding[((b[14] & 3) << 3) | ((b[15] & 224) >> 5)];
    dst[25] = Encoding[b[15] & 31];
}

}; // namespace ulid

#endif // ULID_BASE32_HH
