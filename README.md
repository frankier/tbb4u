# tbb4u

Wheels for [oneTBB](https://github.com/uxlfoundation/oneTBB) (oneAPI Thread
Building Blocks), published to PyPI as [`tbb4u`](https://pypi.org/project/tbb4u/).

Each wheel bundles the oneTBB shared libraries (`tbb`, `tbbmalloc`) built
**unmodified** from an upstream release tag. The wheel version matches the
packaged oneTBB release (e.g. `2023.1.0`). The `tbbmalloc_proxy` interposition
shim is not included.

Wheels are tagged `py3-none-<platform>` and are independent of the Python
version and ABI: a single wheel per OS/architecture/libc covers every
supported Python (3.8+). Platforms covered: manylinux_2_28 and musllinux_1_2
(x86_64, aarch64), Windows x64 and ARM64, macOS 10.15+ x86_64 and macOS 11+
ARM64.

## How it works

- `CMakeLists.txt` here is only a thin shim: it `add_subdirectory()`s a checkout
  of `uxlfoundation/oneTBB` (pointed at by the `ONE_TBB_SOURCE_DIR` variable or
  environment variable) and installs the built libraries into the `tbb4u`
  package directory. All build logic lives upstream.
- `.github/workflows/build.yml` is manually triggered and builds a matrix of
  OS (`windows`/`linux`/`macos`) x architecture (`intel`/`arm`) x libc
  (glibc/musl) x oneTBB tag using plain `python -m build`, then uploads
  everything to PyPI via trusted publishing. Linux builds run inside pypa's
  official [manylinux/musllinux containers](https://quay.io/organization/pypa)
  to pin the libc compatibility floor, and auditwheel validates and retags
  those wheels. cibuildwheel is deliberately not used because it refuses to
  build wheels that are not tied to a specific CPython ABI
  ([pypa/cibuildwheel#255](https://github.com/pypa/cibuildwheel/issues/255)).
- To package a new oneTBB release, add its tag to the matrix in the workflow
  (both `build_wheels` and `build_sdist`).

## Usage

```python
import tbb4u

tbb4u.__version__   # e.g. "2023.1.0"
lib = tbb4u.load()  # ctypes handle to the bundled libtbb
```

## License

The packaging shim is Apache-2.0. The bundled oneTBB sources are Apache-2.0
(with LLVM exceptions); their license texts ship inside each wheel under
`tbb4u/licenses/`.
