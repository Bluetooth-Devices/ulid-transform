#ifndef ULID_STRUCT_HH
#define ULID_STRUCT_HH

#include <array>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <functional>
#include <random>
#include <thread>
#include <vector>

#include "ulid_base32.hh"

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
            static_cast<uint32_t>(std::random_device { }()),
            static_cast<uint32_t>(std::hash<std::thread::id> { }(std::this_thread::get_id()))
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
    EncodeBase32From(ulid.data, dst);
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
 * UnmarshalFrom will unmarshal a ULID from the passed character array.
 * */
inline void UnmarshalFrom(const char str[26], ULID& ulid)
{
    DecodeBase32To(str, ulid.data);
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
