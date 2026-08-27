# tbb4u

## Why?

[`tbb` publishes really limited wheels to PyPI (just two)](https://github.com/uxlfoundation/oneTBB/issues/1972). Most notable is the lack of any ARM images. This repo builds the reset with GitHub Actions and uploads them to PyPI as [`tbb4u`](https://pypi.org/project/tbb4u/). We build extra images like musl based ones while we're at it.

The wheels are published with trusted publishing using the build scripts in this repo, and are provided as-is.

## Usage

If you're working on a project you can just install `tbb4u` instead of `tbb`:

```bash
uv add tbb4u
```

If you need to use a library which uses tbb you can override the dependencies.

```toml
[tool.uv]
override-dependencies = [
  { package = { name = "tbbusinglib" }, dependencies = ["tbb4u"] },
]
exclude-dependencies = [
  { package = { name = "tbbusinglib-parent" }, dependencies = ["tbb"] },
]
```

With any luck you'll be able to remove these when upstream remembers that tbb isn't meant to just be and Intel project anymore given ARM is a member of the UXL Foundation(!)

---

The rest of the README is from ze robot.

⬇️ 🤖 ⬇️

## What?

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


## License

The packaging shim is Apache-2.0. The bundled oneTBB sources are Apache-2.0
(with LLVM exceptions); their license texts ship inside each wheel under
`tbb4u/licenses/`.
