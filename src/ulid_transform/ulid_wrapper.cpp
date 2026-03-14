#include "ulid_wrapper.h"

#ifdef __SIZEOF_INT128__ // http://stackoverflow.com/a/23981011
#include "ulid_uint128.hh"
#else
#include "ulid_struct.hh"
#endif

#include <string.h>

#ifdef __SIZEOF_INT128__
/**
 * Marshal a uint128 ULID to 26 base32 characters.
 * Decomposes into two 64-bit halves kept in registers to avoid
 * the repeated memory loads the compiler generates with MarshalTo.
 */
static inline void marshal_text(const ulid::ULID& ulid, char dst[26])
{
    const uint64_t hi = static_cast<uint64_t>(ulid >> 64);
    const uint64_t lo = static_cast<uint64_t>(ulid);
    const char* e = ulid::Encoding;

    // 10 char timestamp (3 + 9*5 = 48 bits)
    dst[0] = e[(hi >> 61) & 0x07];
    dst[1] = e[(hi >> 56) & 0x1F];
    dst[2] = e[(hi >> 51) & 0x1F];
    dst[3] = e[(hi >> 46) & 0x1F];
    dst[4] = e[(hi >> 41) & 0x1F];
    dst[5] = e[(hi >> 36) & 0x1F];
    dst[6] = e[(hi >> 31) & 0x1F];
    dst[7] = e[(hi >> 26) & 0x1F];
    dst[8] = e[(hi >> 21) & 0x1F];
    dst[9] = e[(hi >> 16) & 0x1F];

    // 16 char entropy (80 bits)
    dst[10] = e[(hi >> 11) & 0x1F];
    dst[11] = e[(hi >> 6) & 0x1F];
    dst[12] = e[(hi >> 1) & 0x1F];
    dst[13] = e[((hi & 1) << 4) | ((lo >> 60) & 0x0F)];
    dst[14] = e[(lo >> 55) & 0x1F];
    dst[15] = e[(lo >> 50) & 0x1F];
    dst[16] = e[(lo >> 45) & 0x1F];
    dst[17] = e[(lo >> 40) & 0x1F];
    dst[18] = e[(lo >> 35) & 0x1F];
    dst[19] = e[(lo >> 30) & 0x1F];
    dst[20] = e[(lo >> 25) & 0x1F];
    dst[21] = e[(lo >> 20) & 0x1F];
    dst[22] = e[(lo >> 15) & 0x1F];
    dst[23] = e[(lo >> 10) & 0x1F];
    dst[24] = e[(lo >> 5) & 0x1F];
    dst[25] = e[lo & 0x1F];
}

/**
 * Marshal a uint128 ULID to 16 bytes using bswap instead of
 * byte-by-byte extraction (16 shifts + 16 vector lane inserts).
 */
static inline void marshal_bytes(const ulid::ULID& ulid, uint8_t dst[16])
{
    uint64_t high = __builtin_bswap64(static_cast<uint64_t>(ulid >> 64));
    uint64_t low = __builtin_bswap64(static_cast<uint64_t>(ulid));
    memcpy(dst, &high, 8);
    memcpy(dst + 8, &low, 8);
}

#else // struct path

static inline void marshal_text(const ulid::ULID& ulid, char dst[26])
{
    ulid::MarshalTo(ulid, dst);
}

static inline void marshal_bytes(const ulid::ULID& ulid, uint8_t dst[16])
{
    ulid::MarshalBinaryTo(ulid, dst);
}
#endif

/**
 * Generate a new text ULID and write it to the provided buffer.
 * The buffer is NOT null-terminated.
 */
void _cpp_ulid(char dst[26])
{
    ulid::ULID ulid;
    ulid::EncodeTimeSystemClockNow(ulid);
    ulid::EncodeEntropyMt19937Fast(ulid);
    marshal_text(ulid, dst);
}

/**
 * Generate a new binary ULID and write it to the provided buffer.
 */
void _cpp_ulid_bytes(uint8_t dst[16])
{
    ulid::ULID ulid;
    ulid::EncodeTimeSystemClockNow(ulid);
    ulid::EncodeEntropyMt19937Fast(ulid);
    marshal_bytes(ulid, dst);
}

/**
 * Generate a new text ULID at the provided epoch time and write it to the provided buffer.
 * The buffer is NOT null-terminated.
 */
void _cpp_ulid_at_time(double epoch_time, char dst[26])
{
    ulid::ULID ulid;
    ulid::EncodeTimestamp(static_cast<int64_t>(epoch_time * 1000), ulid);
    ulid::EncodeEntropyMt19937Fast(ulid);
    marshal_text(ulid, dst);
}

/**
 * Generate a new binary ULID at the provided epoch time and write it to the provided buffer.
 */
void _cpp_ulid_at_time_bytes(double epoch_time, uint8_t dst[16])
{
    ulid::ULID ulid;
    ulid::EncodeTimestamp(static_cast<int64_t>(epoch_time * 1000), ulid);
    ulid::EncodeEntropyMt19937Fast(ulid);
    marshal_bytes(ulid, dst);
}

/**
 * Convert a text ULID to a binary ULID directly.
 * Decodes base32 straight to bytes without an intermediate uint128/struct.
 * The buffer passed in must contain at least 26 bytes.
 * Invalid data will result in undefined behavior.
 */
void _cpp_ulid_to_bytes(const char* str, uint8_t dst[16])
{
    ulid::DecodeBase32To(str, dst);
}

/**
 * Convert a binary ULID to a text ULID directly.
 * Encodes base32 straight from bytes without an intermediate uint128/struct.
 * The buffer passed in must contain at least 16 bytes.
 * The output buffer will NOT be null-terminated.
 */
void _cpp_bytes_to_ulid(const uint8_t b[16], char dst[26])
{
    ulid::EncodeBase32From(b, dst);
}

/**
 * Convert a buffer of exactly 16 bytes to 32 hex characters.
 * The output buffer will NOT be null-terminated.
 */
void _cpp_hexlify_16(const uint8_t b[16], char dst[32])
{
    static const char hexdigits[17] = "0123456789abcdef";
    int in_index, out_index;
    for (in_index = out_index = 0; in_index < 16; in_index++) {
        uint8_t c = b[in_index];
        dst[out_index++] = hexdigits[c >> 4];
        dst[out_index++] = hexdigits[c & 0x0f];
    }
}

/**
 * Interpret the first 6 bytes of a binary ULID as a timestamp.
 */
uint64_t _cpp_bytes_to_timestamp(const uint8_t b[16])
{
    uint64_t timestamp = 0;
    timestamp |= static_cast<uint64_t>(b[0]) << 40;
    timestamp |= static_cast<uint64_t>(b[1]) << 32;
    timestamp |= static_cast<uint64_t>(b[2]) << 24;
    timestamp |= static_cast<uint64_t>(b[3]) << 16;
    timestamp |= static_cast<uint64_t>(b[4]) << 8;
    timestamp |= static_cast<uint64_t>(b[5]);
    return timestamp;
}
