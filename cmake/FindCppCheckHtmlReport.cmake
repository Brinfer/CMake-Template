if(NOT CPPCHECK_HTMLREPORT_FOUND)
    include(FindPackageHandleStandardArgs)

    find_program(
        CPPCHECK_HTML_REPORT_EXECUTABLE
        NAMES cppcheck-htmlreport
        HINTS /usr/ /bin/
        DOC "Convert the XML output from Cppcheck into a HTML report")
    mark_as_advanced(CPPCHECK_HTML_REPORT_EXECUTABLE)

    find_package_handle_standard_args(CppCheckHtmlReport "Failed to find cppcheck-htnlreport executable"
                                      CPPCHECK_HTML_REPORT_EXECUTABLE)

    set(CPPCHECK_HTMLREPORT_FOUND
        ${CppCheckHtmlReport_FOUND}
        CACHE BOOL "Boolean containing the search result of the cppcheck-htmlreport executable")
endif(NOT CPPCHECK_HTMLREPORT_FOUND)
