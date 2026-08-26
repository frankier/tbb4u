# Thin packaging shim for the tbb4u PyPI distribution.
#
# This file does NOT define how oneTBB is built -- the full upstream CMake
# project is consumed unmodified via add_subdirectory() below. The only jobs
# done here are locating the oneTBB checkout and routing the built binaries
# into the 'tbb4u' package directory so they end up inside the wheel.
cmake_minimum_required(VERSION 3.16)
project(tbb4u LANGUAGES CXX)

# Location of an oneTBB checkout. Defaults to a sibling 'oneTBB' directory
# next to this file (how CI lays it out -- relative so it also resolves
# inside cibuildwheel's Linux build containers, where host paths do not
# exist). Override with the ONE_TBB_SOURCE_DIR environment variable.
if(DEFINED ENV{ONE_TBB_SOURCE_DIR})
    set(_tbb4u_one_tbb_src "$ENV{ONE_TBB_SOURCE_DIR}")
else()
    set(_tbb4u_one_tbb_src "${CMAKE_CURRENT_SOURCE_DIR}/oneTBB")
endif()
set(ONE_TBB_SOURCE_DIR "${_tbb4u_one_tbb_src}" CACHE PATH
    "Path to an oneTBB source checkout")
if(NOT EXISTS "${ONE_TBB_SOURCE_DIR}/CMakeLists.txt")
    message(FATAL_ERROR
        "ONE_TBB_SOURCE_DIR ('${ONE_TBB_SOURCE_DIR}') must contain an "
        "checkout of https://github.com/uxlfoundation/oneTBB")
endif()

# Trim the upstream build to the runtime libraries only. These options exist
# in every tag packaged so far (v2021.13.x onward). TBB_INSTALL is disabled so
# upstream's own install rules (which target system layouts) don't fire; this
# shim installs what the wheel needs instead.
set(TBB_TEST OFF CACHE BOOL "" FORCE)
set(TBB_EXAMPLES OFF CACHE BOOL "" FORCE)
set(TBB_BENCHMARK OFF CACHE BOOL "" FORCE)
set(TBB_STRICT OFF CACHE BOOL "" FORCE)
set(TBB_INSTALL OFF CACHE BOOL "" FORCE)

# NOTE: deliberately *not* EXCLUDE_FROM_ALL -- scikit-build-core builds the
# default ('all') target before installing, so the libraries must be part of
# it.
add_subdirectory(${ONE_TBB_SOURCE_DIR} ${CMAKE_BINARY_DIR}/oneTBB)

# Ship the shared libraries inside the Python package. Import/static libs are
# included too (ARCHIVE) because CMake falls back to default destinations for
# artifact kinds that are not named; keeping them beside the DLLs keeps the
# wheel contents predictable across platforms.
#
# tbbmalloc_proxy is deliberately NOT shipped: it is an LD_PRELOAD/
# interposition shim with a hard DT_NEEDED on libtbbmalloc.so.2, which
# auditwheel repair cannot resolve from wheel-internal paths -- and it has no
# use inside a Python distribution anyway.
#
# Targets are installed individually: upstream does not define every target
# on every platform.
foreach(tbb4u_target IN ITEMS tbb tbbmalloc)
    if(TARGET ${tbb4u_target})
        install(TARGETS ${tbb4u_target}
                LIBRARY DESTINATION tbb4u
                RUNTIME DESTINATION tbb4u
                ARCHIVE DESTINATION tbb4u)
    else()
        message(STATUS "tbb4u: upstream defines no '${tbb4u_target}' "
                       "target on this platform; skipping")
    endif()
endforeach()

# Carry the upstream license texts along.
if(EXISTS "${ONE_TBB_SOURCE_DIR}/LICENSE.txt")
    install(FILES ${ONE_TBB_SOURCE_DIR}/LICENSE.txt
                  ${ONE_TBB_SOURCE_DIR}/third-party-programs.txt
            DESTINATION tbb4u/licenses)
endif()
