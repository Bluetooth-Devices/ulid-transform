#ifndef ULID_SPLITMIX64_HH
#define ULID_SPLITMIX64_HH

#include <cstdint>

namespace ulid {

/**
 * SplitMix64 is a fast, small-state PRNG suitable for non-cryptographic use.
 */
struct SplitMix64 {
    uint64_t state;

    explicit SplitMix64(uint64_t seed)
        : state(seed)
    {
    }

    uint64_t operator()()
    {
        uint64_t z = (state += 0x9e3779b97f4a7c15ULL);
        z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
        z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
        return z ^ (z >> 31);
    }
};

}

#endif // ULID_SPLITMIX64_HH
