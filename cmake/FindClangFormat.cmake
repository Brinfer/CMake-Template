if(NOT CLANGFORMAT_FOUND)

    include(FindPackageHandleStandardArgs)

    find_program(
        CLANG_FORMAT_EXECUTABLE
        NAMES clang-format
        HINTS /usr/ /bin/
        DOC "A tool to format C/C++/Java/JavaScript/JSON/Objective-C/Protobuf/C# code.")
    mark_as_advanced(CLANG_FORMAT_EXECUTABLE)

    find_package_handle_standard_args(ClangFormat "Failed to find clang-format executable" CLANG_FORMAT_EXECUTABLE)
    set(CLANGFORMAT_FOUND
        ${ClangFormat_FOUND}
        CACHE BOOL "Boolean containing the search result of the 'clang-format' executable")
endif(NOT CLANGFORMAT_FOUND)
