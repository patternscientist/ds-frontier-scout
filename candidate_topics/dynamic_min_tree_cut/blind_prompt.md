# Blind Prompt

A graph `G` changes by edge insertions and deletions. A spanning forest `T` is maintained. For each tree edge `e`, deleting `e` partitions its tree; define the cut value as the number or total weight of graph edges crossing that partition.

Maintain the minimum tree-cut value over all tree edges under updates. Seek polylogarithmic update time, or prove a lower bound for this restricted dynamic problem.
