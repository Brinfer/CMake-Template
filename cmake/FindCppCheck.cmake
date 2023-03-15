if(NOT CPPCHECK_FOUND)
    include(FindPackageHandleStandardArgs)

    find_program(
        CPPCHECK_EXECUTABLE
        NAMES cppcheck
        HINTS /usr/ /bin/
        DOC "CppCheck static analysis tool")
    mark_as_advanced(CPPCHECK_EXECUTABLE)

    find_package_handle_standard_args(CppCheck "Failed to find cppcheck executable" CPPCHECK_EXECUTABLE)

    set(CPPCHECK_FOUND
        ${CppCheck_FOUND}
        CACHE BOOL "Boolean containing the search result of the cppcheck executable")
endif(NOT CPPCHECK_FOUND)
