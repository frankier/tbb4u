# Thin packaging shim for the tbb4u PyPI distribution.
#
# This file does NOT define how oneTBB is built -- the full upstream CMake
# project is consumed unmodified via add_subdirectory() below. The only job
# done here is routing the built binaries into the 'tbb4u' package directory
# so they end up inside the wheel.
cmake_minimum_required(VERSION 3.16)
project(tbb4u LANGUAGES CXX)

# Location of an oneTBB checkout (CI clones uxlfoundation/oneTBB and points
# this at it). Accepts a CMake variable or the ONE_TBB_SOURCE_DIR env var.
set(ONE_TBB_SOURCE_DIR "" CACHE PATH "Path to an oneTBB source checkout")
if(NOT ONE_TBB_SOURCE_DIR AND DEFINED ENV{ONE_TBB_SOURCE_DIR})
    set(ONE_TBB_SOURCE_DIR "$ENV{ONE_TBB_SOURCE_DIR}"
        CACHE PATH "Path to an oneTBB source checkout" FORCE)
endif()
if(NOT ONE_TBB_SOURCE_DIR)
    message(FATAL_ERROR
        "ONE_TBB_SOURCE_DIR must point at a checkout of "
        "https://github.com/uxlfoundation/oneTBB")
endif()

# Trim the upstream build to the runtime libraries only. These options exist
# in every tag packaged so far (v2021.13.x onward).
set(TBB_TEST OFF CACHE BOOL "" FORCE)
set(TBB_EXAMPLES OFF CACHE BOOL "" FORCE)
set(TBB_BENCHMARK OFF CACHE BOOL "" FORCE)
set(TBB_STRICT OFF CACHE BOOL "" FORCE)

add_subdirectory(${ONE_TBB_SOURCE_DIR} ${CMAKE_BINARY_DIR}/oneTBB
                 EXCLUDE_FROM_ALL)

# Ship the shared libraries inside the Python package. Import/static libs are
# included too (ARCHIVE) because CMake falls back to default destinations for
# artifact kinds that are not named; keeping them beside the DLLs keeps the
# wheel contents predictable across platforms.
install(TARGETS tbb tbbmalloc tbbmalloc_proxy
        LIBRARY DESTINATION tbb4u
        RUNTIME DESTINATION tbb4u
        ARCHIVE DESTINATION tbb4u)

# Carry the upstream license texts along; declared as license-files in
# pyproject.toml.
install(FILES ${ONE_TBB_SOURCE_DIR}/LICENSE.txt
              ${ONE_TBB_SOURCE_DIR}/third-party-programs.txt
        DESTINATION tbb4u/licenses)
