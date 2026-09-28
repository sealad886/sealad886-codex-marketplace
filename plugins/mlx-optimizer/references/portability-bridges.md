# Portability Bridges

Use this reference when MLX Python work needs to integrate with another
language or application runtime.

## Native MLX Surfaces

- Python is the v1 optimization focus for this plugin.
- Swift is the practical Apple-app integration path.
- C and C++ are native extension and lower-level integration paths.

## Other Languages

For Rust, Go, JavaScript, Java, Kotlin, and other ecosystems, prefer explicit
boundaries:

- Call a Python service or subprocess for MLX execution.
- Use a C ABI wrapper when a native boundary is required.
- Export to Core ML or another deployment format when MLX runtime access is not
  required.
- Keep data marshaling and synchronization costs in the benchmark.
