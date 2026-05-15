# Problem

Maintain a single dynamic text `T` under substring insertions and deletions, while supporting pattern-search queries in compact space.

Open status: open in the cited older source; modern status uncertain. Target: `O(|T|)` bits, update a substring of length `s` in `O(s polylog |T|)` time, and search a pattern of length `p` in `O((p+occ) polylog |T|)` time.
