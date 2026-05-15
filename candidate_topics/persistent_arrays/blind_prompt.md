# Blind Prompt

Design a fully persistent array. Operations are `lookup(version, index)` and `update(version, index, value)`, where each update creates a new version and old versions remain accessible and updatable.

Use `O(n+m)` total space after `m` updates to an initial array of length `n`. Try to achieve worst-case `O(log log m)` time for both lookup and update, or prove a barrier for version-tree/order-maintenance based designs.
