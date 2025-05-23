#ifndef ULID_STRUCT_HH
#define ULID_STRUCT_HH

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
struct ULID {
    uint8_t data[16];
};

/**
 * EncodeTimestamp will encode the int64_t timestamp to the passed ulid
 * */
inline void EncodeTimestamp(int64_t timestamp, ULID& ulid)
{
    ulid.data[0] = static_cast<uint8_t>(timestamp >> 40);
    ulid.data[1] = static_cast<uint8_t>(timestamp >> 32);
    ulid.data[2] = static_cast<uint8_t>(timestamp >> 24);
    ulid.data[3] = static_cast<uint8_t>(timestamp >> 16);
    ulid.data[4] = static_cast<uint8_t>(timestamp >> 8);
    ulid.data[5] = static_cast<uint8_t>(timestamp);
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
            static_cast<uint32_t>(std::random_device {}()),
            static_cast<uint32_t>(reinterpret_cast<uintptr_t>(&gen) & 0xFFFFFFFF)
        };
        std::seed_seq seed_seq(seed_data.begin(), seed_data.end());
        return std::mt19937(seed_seq);
    }());
    uint64_t high = (static_cast<uint64_t>(gen()) << 32) | gen();
    uint32_t low = gen();
    ulid.data[6] = (high >> 40) & 0xFF;
    ulid.data[7] = (high >> 32) & 0xFF;
    ulid.data[8] = (high >> 24) & 0xFF;
    ulid.data[9] = (high >> 16) & 0xFF;
    ulid.data[10] = (high >> 8) & 0xFF;
    ulid.data[11] = high & 0xFF;
    ulid.data[12] = (low >> 24) & 0xFF;
    ulid.data[13] = (low >> 16) & 0xFF;
    ulid.data[14] = (low >> 8) & 0xFF;
    ulid.data[15] = low & 0xFF;
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
 * timestamp:<br>
 * dst[0]: first 3 bits of data[0]<br>
 * dst[1]: last 5 bits of data[0]<br>
 * dst[2]: first 5 bits of data[1]<br>
 * dst[3]: last 3 bits of data[1] + first 2 bits of data[2]<br>
 * dst[4]: bits 3-7 of data[2]<br>
 * dst[5]: last bit of data[2] + first 4 bits of data[3]<br>
 * dst[6]: last 4 bits of data[3] + first bit of data[4]<br>
 * dst[7]: bits 2-6 of data[4]<br>
 * dst[8]: last 2 bits of data[4] + first 3 bits of data[5]<br>
 * dst[9]: last 5 bits of data[5]<br>
 *
 * entropy:
 * follows similarly, except now all components are set to 5 bits.
 * */
inline void MarshalTo(const ULID& ulid, char dst[26])
{
    // 10 byte timestamp
    dst[0] = Encoding[(ulid.data[0] & 224) >> 5];
    dst[1] = Encoding[ulid.data[0] & 31];
    dst[2] = Encoding[(ulid.data[1] & 248) >> 3];
    dst[3] = Encoding[((ulid.data[1] & 7) << 2) | ((ulid.data[2] & 192) >> 6)];
    dst[4] = Encoding[(ulid.data[2] & 62) >> 1];
    dst[5] = Encoding[((ulid.data[2] & 1) << 4) | ((ulid.data[3] & 240) >> 4)];
    dst[6] = Encoding[((ulid.data[3] & 15) << 1) | ((ulid.data[4] & 128) >> 7)];
    dst[7] = Encoding[(ulid.data[4] & 124) >> 2];
    dst[8] = Encoding[((ulid.data[4] & 3) << 3) | ((ulid.data[5] & 224) >> 5)];
    dst[9] = Encoding[ulid.data[5] & 31];

    // 16 bytes of entropy
    dst[10] = Encoding[(ulid.data[6] & 248) >> 3];
    dst[11] = Encoding[((ulid.data[6] & 7) << 2) | ((ulid.data[7] & 192) >> 6)];
    dst[12] = Encoding[(ulid.data[7] & 62) >> 1];
    dst[13] = Encoding[((ulid.data[7] & 1) << 4) | ((ulid.data[8] & 240) >> 4)];
    dst[14] = Encoding[((ulid.data[8] & 15) << 1) | ((ulid.data[9] & 128) >> 7)];
    dst[15] = Encoding[(ulid.data[9] & 124) >> 2];
    dst[16] = Encoding[((ulid.data[9] & 3) << 3) | ((ulid.data[10] & 224) >> 5)];
    dst[17] = Encoding[ulid.data[10] & 31];
    dst[18] = Encoding[(ulid.data[11] & 248) >> 3];
    dst[19] = Encoding[((ulid.data[11] & 7) << 2) | ((ulid.data[12] & 192) >> 6)];
    dst[20] = Encoding[(ulid.data[12] & 62) >> 1];
    dst[21] = Encoding[((ulid.data[12] & 1) << 4) | ((ulid.data[13] & 240) >> 4)];
    dst[22] = Encoding[((ulid.data[13] & 15) << 1) | ((ulid.data[14] & 128) >> 7)];
    dst[23] = Encoding[(ulid.data[14] & 124) >> 2];
    dst[24] = Encoding[((ulid.data[14] & 3) << 3) | ((ulid.data[15] & 224) >> 5)];
    dst[25] = Encoding[ulid.data[15] & 31];
}

/**
 * MarshalBinaryTo will Marshal a ULID to the passed byte array
 * */
inline void MarshalBinaryTo(const ULID& ulid, uint8_t dst[16])
{
    // timestamp
    dst[0] = ulid.data[0];
    dst[1] = ulid.data[1];
    dst[2] = ulid.data[2];
    dst[3] = ulid.data[3];
    dst[4] = ulid.data[4];
    dst[5] = ulid.data[5];

    // entropy
    dst[6] = ulid.data[6];
    dst[7] = ulid.data[7];
    dst[8] = ulid.data[8];
    dst[9] = ulid.data[9];
    dst[10] = ulid.data[10];
    dst[11] = ulid.data[11];
    dst[12] = ulid.data[12];
    dst[13] = ulid.data[13];
    dst[14] = ulid.data[14];
    dst[15] = ulid.data[15];
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
    ulid.data[0] = (dec[int(str[0])] << 5) | dec[int(str[1])];
    ulid.data[1] = (dec[int(str[2])] << 3) | (dec[int(str[3])] >> 2);
    ulid.data[2] = (dec[int(str[3])] << 6) | (dec[int(str[4])] << 1) | (dec[int(str[5])] >> 4);
    ulid.data[3] = (dec[int(str[5])] << 4) | (dec[int(str[6])] >> 1);
    ulid.data[4] = (dec[int(str[6])] << 7) | (dec[int(str[7])] << 2) | (dec[int(str[8])] >> 3);
    ulid.data[5] = (dec[int(str[8])] << 5) | dec[int(str[9])];

    // entropy
    ulid.data[6] = (dec[int(str[10])] << 3) | (dec[int(str[11])] >> 2);
    ulid.data[7] = (dec[int(str[11])] << 6) | (dec[int(str[12])] << 1) | (dec[int(str[13])] >> 4);
    ulid.data[8] = (dec[int(str[13])] << 4) | (dec[int(str[14])] >> 1);
    ulid.data[9] = (dec[int(str[14])] << 7) | (dec[int(str[15])] << 2) | (dec[int(str[16])] >> 3);
    ulid.data[10] = (dec[int(str[16])] << 5) | dec[int(str[17])];
    ulid.data[11] = (dec[int(str[18])] << 3) | (dec[int(str[19])] >> 2);
    ulid.data[12] = (dec[int(str[19])] << 6) | (dec[int(str[20])] << 1) | (dec[int(str[21])] >> 4);
    ulid.data[13] = (dec[int(str[21])] << 4) | (dec[int(str[22])] >> 1);
    ulid.data[14] = (dec[int(str[22])] << 7) | (dec[int(str[23])] << 2) | (dec[int(str[24])] >> 3);
    ulid.data[15] = (dec[int(str[24])] << 5) | dec[int(str[25])];
}

/**
 * UnmarshalBinaryFrom will unmarshal a ULID from the passed byte array.
 * */
inline void UnmarshalBinaryFrom(const uint8_t b[16], ULID& ulid)
{
    // timestamp
    ulid.data[0] = b[0];
    ulid.data[1] = b[1];
    ulid.data[2] = b[2];
    ulid.data[3] = b[3];
    ulid.data[4] = b[4];
    ulid.data[5] = b[5];

    // entropy
    ulid.data[6] = b[6];
    ulid.data[7] = b[7];
    ulid.data[8] = b[8];
    ulid.data[9] = b[9];
    ulid.data[10] = b[10];
    ulid.data[11] = b[11];
    ulid.data[12] = b[12];
    ulid.data[13] = b[13];
    ulid.data[14] = b[14];
    ulid.data[15] = b[15];
}

}; // namespace ulid

#endif // ULID_STRUCT_HH
