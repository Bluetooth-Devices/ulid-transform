#ifndef ULID_UINT128_HH
#define ULID_UINT128_HH

#include <array>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <functional>
#include <random>
#include <vector>

#if _MSC_VER > 0
typedef uint32_t rand_t;
#else
typedef uint8_t rand_t;
#endif

namespace ulid {

/**
 * ULID is a 16 byte Universally Unique Lexicographically Sortable Identifier
 * */
typedef __uint128_t ULID;

/**
 * EncodeTimestamp will encode the int64_t timestamp to the passed ulid
 * */
inline void EncodeTimestamp(int64_t timestamp, ULID& ulid)
{
    ULID t = static_cast<uint8_t>(timestamp >> 40);

    t <<= 8;
    t |= static_cast<uint8_t>(timestamp >> 32);

    t <<= 8;
    t |= static_cast<uint8_t>(timestamp >> 24);

    t <<= 8;
    t |= static_cast<uint8_t>(timestamp >> 16);

    t <<= 8;
    t |= static_cast<uint8_t>(timestamp >> 8);

    t <<= 8;
    t |= static_cast<uint8_t>(timestamp);

    t <<= 80;

    ULID mask = 1;
    mask <<= 80;
    mask--;

    ulid = t | (ulid & mask);
}

/**
 * EncodeTime will encode the time point to the passed ulid
 * */
inline void EncodeTime(std::chrono::time_point<std::chrono::system_clock> time_point, ULID& ulid)
{
    auto time_ms = std::chrono::time_point_cast<std::chrono::milliseconds>(time_point);
    int64_t timestamp = time_ms.time_since_epoch().count();
    EncodeTimestamp(timestamp, ulid);
}

/**
 * EncodeTimeSystemClockNow will encode a ULID using the time obtained using
 * std::chrono::system_clock::now() by taking the timestamp in milliseconds.
 * */
inline void EncodeTimeSystemClockNow(ULID& ulid)
{
    EncodeTime(std::chrono::system_clock::now(), ulid);
}

/**
 * EncodeEntropyMt19937Fast will encode using std::mt19937
 * with only 3 generated values.
 * */
inline void EncodeEntropyMt19937Fast(ULID& ulid)
{
    static thread_local std::mt19937 gen([]() {
        // Use multiple entropy sources for seeding
        std::array<uint32_t, 3> seed_data = {
            static_cast<uint32_t>(std::chrono::high_resolution_clock::now().time_since_epoch().count()),
            static_cast<uint32_t>(std::random_device { }()),
            static_cast<uint32_t>(reinterpret_cast<uintptr_t>(&gen) & 0xFFFFFFFF)
        };
        std::seed_seq seed_seq(seed_data.begin(), seed_data.end());
        return std::mt19937(seed_seq);
    }());
    ulid = (ulid >> 80) << 80; // Clear lower 80 bits
    ulid |= (static_cast<ULID>((static_cast<uint64_t>(gen()) << 32) | gen()) << 16) | (gen() & 0xFFFF);
}

/**
 * Crockford's Base32
 * */
static const char Encoding[33] = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";

/**
 * MarshalTo will marshal a ULID to the passed character array.
 *
 * Implementation taken directly from oklog/ulid
 * (https://sourcegraph.com/github.com/oklog/ulid@0774f81f6e44af5ce5e91c8d7d76cf710e889ebb/-/blob/ulid.go#L162-190)
 *
 * timestamp:
 * dst[0]: first 3 bits of data[0]
 * dst[1]: last 5 bits of data[0]
 * dst[2]: first 5 bits of data[1]
 * dst[3]: last 3 bits of data[1] + first 2 bits of data[2]
 * dst[4]: bits 3-7 of data[2]
 * dst[5]: last bit of data[2] + first 4 bits of data[3]
 * dst[6]: last 4 bits of data[3] + first bit of data[4]
 * dst[7]: bits 2-6 of data[4]
 * dst[8]: last 2 bits of data[4] + first 3 bits of data[5]
 * dst[9]: last 5 bits of data[5]
 *
 * entropy:
 * follows similarly, except now all components are set to 5 bits.
 * */
inline void MarshalTo(const ULID& ulid, char dst[26])
{
    // 10 byte timestamp
    dst[0] = Encoding[(static_cast<uint8_t>(ulid >> 120) & 224) >> 5];
    dst[1] = Encoding[static_cast<uint8_t>(ulid >> 120) & 31];
    dst[2] = Encoding[(static_cast<uint8_t>(ulid >> 112) & 248) >> 3];
    dst[3] = Encoding[((static_cast<uint8_t>(ulid >> 112) & 7) << 2) | ((static_cast<uint8_t>(ulid >> 104) & 192) >> 6)];
    dst[4] = Encoding[(static_cast<uint8_t>(ulid >> 104) & 62) >> 1];
    dst[5] = Encoding[((static_cast<uint8_t>(ulid >> 104) & 1) << 4) | ((static_cast<uint8_t>(ulid >> 96) & 240) >> 4)];
    dst[6] = Encoding[((static_cast<uint8_t>(ulid >> 96) & 15) << 1) | ((static_cast<uint8_t>(ulid >> 88) & 128) >> 7)];
    dst[7] = Encoding[(static_cast<uint8_t>(ulid >> 88) & 124) >> 2];
    dst[8] = Encoding[((static_cast<uint8_t>(ulid >> 88) & 3) << 3) | ((static_cast<uint8_t>(ulid >> 80) & 224) >> 5)];
    dst[9] = Encoding[static_cast<uint8_t>(ulid >> 80) & 31];

    // 16 bytes of entropy
    dst[10] = Encoding[(static_cast<uint8_t>(ulid >> 72) & 248) >> 3];
    dst[11] = Encoding[((static_cast<uint8_t>(ulid >> 72) & 7) << 2) | ((static_cast<uint8_t>(ulid >> 64) & 192) >> 6)];
    dst[12] = Encoding[(static_cast<uint8_t>(ulid >> 64) & 62) >> 1];
    dst[13] = Encoding[((static_cast<uint8_t>(ulid >> 64) & 1) << 4) | ((static_cast<uint8_t>(ulid >> 56) & 240) >> 4)];
    dst[14] = Encoding[((static_cast<uint8_t>(ulid >> 56) & 15) << 1) | ((static_cast<uint8_t>(ulid >> 48) & 128) >> 7)];
    dst[15] = Encoding[(static_cast<uint8_t>(ulid >> 48) & 124) >> 2];
    dst[16] = Encoding[((static_cast<uint8_t>(ulid >> 48) & 3) << 3) | ((static_cast<uint8_t>(ulid >> 40) & 224) >> 5)];
    dst[17] = Encoding[static_cast<uint8_t>(ulid >> 40) & 31];
    dst[18] = Encoding[(static_cast<uint8_t>(ulid >> 32) & 248) >> 3];
    dst[19] = Encoding[((static_cast<uint8_t>(ulid >> 32) & 7) << 2) | ((static_cast<uint8_t>(ulid >> 24) & 192) >> 6)];
    dst[20] = Encoding[(static_cast<uint8_t>(ulid >> 24) & 62) >> 1];
    dst[21] = Encoding[((static_cast<uint8_t>(ulid >> 24) & 1) << 4) | ((static_cast<uint8_t>(ulid >> 16) & 240) >> 4)];
    dst[22] = Encoding[((static_cast<uint8_t>(ulid >> 16) & 15) << 1) | ((static_cast<uint8_t>(ulid >> 8) & 128) >> 7)];
    dst[23] = Encoding[(static_cast<uint8_t>(ulid >> 8) & 124) >> 2];
    dst[24] = Encoding[((static_cast<uint8_t>(ulid >> 8) & 3) << 3) | (((static_cast<uint8_t>(ulid)) & 224) >> 5)];
    dst[25] = Encoding[(static_cast<uint8_t>(ulid)) & 31];
}

/**
 * MarshalBinaryTo will Marshal a ULID to the passed byte array
 * */
inline void MarshalBinaryTo(const ULID& ulid, uint8_t dst[16])
{
    // timestamp
    dst[0] = static_cast<uint8_t>(ulid >> 120);
    dst[1] = static_cast<uint8_t>(ulid >> 112);
    dst[2] = static_cast<uint8_t>(ulid >> 104);
    dst[3] = static_cast<uint8_t>(ulid >> 96);
    dst[4] = static_cast<uint8_t>(ulid >> 88);
    dst[5] = static_cast<uint8_t>(ulid >> 80);

    // entropy
    dst[6] = static_cast<uint8_t>(ulid >> 72);
    dst[7] = static_cast<uint8_t>(ulid >> 64);
    dst[8] = static_cast<uint8_t>(ulid >> 56);
    dst[9] = static_cast<uint8_t>(ulid >> 48);
    dst[10] = static_cast<uint8_t>(ulid >> 40);
    dst[11] = static_cast<uint8_t>(ulid >> 32);
    dst[12] = static_cast<uint8_t>(ulid >> 24);
    dst[13] = static_cast<uint8_t>(ulid >> 16);
    dst[14] = static_cast<uint8_t>(ulid >> 8);
    dst[15] = static_cast<uint8_t>(ulid);
}

/**
 * dec storesdecimal encodings for characters.
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
 * UnmarshalFrom will unmarshal a ULID from the passed character array.
 * */
inline void UnmarshalFrom(const char str[26], ULID& ulid)
{
    // timestamp
    ulid = (dec[int(str[0])] << 5) | dec[int(str[1])];

    ulid <<= 8;
    ulid |= (dec[int(str[2])] << 3) | (dec[int(str[3])] >> 2);

    ulid <<= 8;
    ulid |= (dec[int(str[3])] << 6) | (dec[int(str[4])] << 1) | (dec[int(str[5])] >> 4);

    ulid <<= 8;
    ulid |= (dec[int(str[5])] << 4) | (dec[int(str[6])] >> 1);

    ulid <<= 8;
    ulid |= (dec[int(str[6])] << 7) | (dec[int(str[7])] << 2) | (dec[int(str[8])] >> 3);

    ulid <<= 8;
    ulid |= (dec[int(str[8])] << 5) | dec[int(str[9])];

    // entropy
    ulid <<= 8;
    ulid |= (dec[int(str[10])] << 3) | (dec[int(str[11])] >> 2);

    ulid <<= 8;
    ulid |= (dec[int(str[11])] << 6) | (dec[int(str[12])] << 1) | (dec[int(str[13])] >> 4);

    ulid <<= 8;
    ulid |= (dec[int(str[13])] << 4) | (dec[int(str[14])] >> 1);

    ulid <<= 8;
    ulid |= (dec[int(str[14])] << 7) | (dec[int(str[15])] << 2) | (dec[int(str[16])] >> 3);

    ulid <<= 8;
    ulid |= (dec[int(str[16])] << 5) | dec[int(str[17])];

    ulid <<= 8;
    ulid |= (dec[int(str[18])] << 3) | (dec[int(str[19])] >> 2);

    ulid <<= 8;
    ulid |= (dec[int(str[19])] << 6) | (dec[int(str[20])] << 1) | (dec[int(str[21])] >> 4);

    ulid <<= 8;
    ulid |= (dec[int(str[21])] << 4) | (dec[int(str[22])] >> 1);

    ulid <<= 8;
    ulid |= (dec[int(str[22])] << 7) | (dec[int(str[23])] << 2) | (dec[int(str[24])] >> 3);

    ulid <<= 8;
    ulid |= (dec[int(str[24])] << 5) | dec[int(str[25])];
}

/**
 * UnmarshalBinaryFrom will unmarshal a ULID from the passed byte array.
 * */
inline void UnmarshalBinaryFrom(const uint8_t b[16], ULID& ulid)
{
    // timestamp
    ulid = b[0];

    ulid <<= 8;
    ulid |= b[1];

    ulid <<= 8;
    ulid |= b[2];

    ulid <<= 8;
    ulid |= b[3];

    ulid <<= 8;
    ulid |= b[4];

    ulid <<= 8;
    ulid |= b[5];

    // entropy
    ulid <<= 8;
    ulid |= b[6];

    ulid <<= 8;
    ulid |= b[7];

    ulid <<= 8;
    ulid |= b[8];

    ulid <<= 8;
    ulid |= b[9];

    ulid <<= 8;
    ulid |= b[10];

    ulid <<= 8;
    ulid |= b[11];

    ulid <<= 8;
    ulid |= b[12];

    ulid <<= 8;
    ulid |= b[13];

    ulid <<= 8;
    ulid |= b[14];

    ulid <<= 8;
    ulid |= b[15];
}

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

#endif // ULID_UINT128_HH
