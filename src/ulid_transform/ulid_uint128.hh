#ifndef ULID_UINT128_HH
#define ULID_UINT128_HH

#include <array>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <functional>
#include <random>
#include <vector>

#include "splitmix64.hh"
#include "ulid_base32.hh"

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
 * EncodeEntropyFast will encode using SplitMix64
 * with only 2 generated values (providing 128 bits, of which 80 are used).
 * */
inline void EncodeEntropyFast(ULID& ulid)
{
    static thread_local SplitMix64 gen([]() {
        // Use multiple entropy sources for seeding
        uint64_t seed = static_cast<uint64_t>(std::chrono::high_resolution_clock::now().time_since_epoch().count());
        seed ^= static_cast<uint64_t>(std::random_device { }()) << 32;
        seed ^= static_cast<uint64_t>(std::random_device { }());
        return seed;
    }());
    constexpr ULID lower80 = (static_cast<ULID>(1) << 80) - 1;
    ulid = (ulid >> 80) << 80; // Clear lower 80 bits
    uint64_t first_draw = gen();
    uint64_t second_draw = gen();
    ulid |= ((static_cast<ULID>(first_draw) << 16) | (second_draw & 0xFFFF)) & lower80;
}

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
    // Decompose into two 64-bit halves kept in registers to avoid
    // repeated memory loads the compiler generates with __uint128_t.
    const uint64_t hi = static_cast<uint64_t>(ulid >> 64);
    const uint64_t lo = static_cast<uint64_t>(ulid);

    // 10 char timestamp (3 + 9*5 = 48 bits)
    dst[0] = Encoding[(hi >> 61) & 0x07];
    dst[1] = Encoding[(hi >> 56) & 0x1F];
    dst[2] = Encoding[(hi >> 51) & 0x1F];
    dst[3] = Encoding[(hi >> 46) & 0x1F];
    dst[4] = Encoding[(hi >> 41) & 0x1F];
    dst[5] = Encoding[(hi >> 36) & 0x1F];
    dst[6] = Encoding[(hi >> 31) & 0x1F];
    dst[7] = Encoding[(hi >> 26) & 0x1F];
    dst[8] = Encoding[(hi >> 21) & 0x1F];
    dst[9] = Encoding[(hi >> 16) & 0x1F];

    // 16 char entropy (80 bits)
    dst[10] = Encoding[(hi >> 11) & 0x1F];
    dst[11] = Encoding[(hi >> 6) & 0x1F];
    dst[12] = Encoding[(hi >> 1) & 0x1F];
    dst[13] = Encoding[((hi & 1) << 4) | ((lo >> 60) & 0x0F)];
    dst[14] = Encoding[(lo >> 55) & 0x1F];
    dst[15] = Encoding[(lo >> 50) & 0x1F];
    dst[16] = Encoding[(lo >> 45) & 0x1F];
    dst[17] = Encoding[(lo >> 40) & 0x1F];
    dst[18] = Encoding[(lo >> 35) & 0x1F];
    dst[19] = Encoding[(lo >> 30) & 0x1F];
    dst[20] = Encoding[(lo >> 25) & 0x1F];
    dst[21] = Encoding[(lo >> 20) & 0x1F];
    dst[22] = Encoding[(lo >> 15) & 0x1F];
    dst[23] = Encoding[(lo >> 10) & 0x1F];
    dst[24] = Encoding[(lo >> 5) & 0x1F];
    dst[25] = Encoding[lo & 0x1F];
}

/**
 * MarshalBinaryTo will Marshal a ULID to the passed byte array
 * */
inline void MarshalBinaryTo(const ULID& ulid, uint8_t dst[16])
{
    // Use bswap to convert each 64-bit half from host order to big-endian,
    // instead of 16 individual byte shifts.
    uint64_t high = __builtin_bswap64(static_cast<uint64_t>(ulid >> 64));
    uint64_t low = __builtin_bswap64(static_cast<uint64_t>(ulid));
    __builtin_memcpy(dst, &high, 8);
    __builtin_memcpy(dst + 8, &low, 8);
}

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

}; // namespace ulid

#endif // ULID_UINT128_HH
