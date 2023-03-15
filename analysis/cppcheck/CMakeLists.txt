#[=======================================================================[.rst:
CreateCppcheckTarget
--------------------

Set up an analysis target using CppCheck.

The target created has the format ``cppcheck-<target_name>``.

If ``CPPCHECK_HTMLREPORT_FOUND`` is ``YES``, then an HTML report is created in the ``CPPCHECK_REPORT_DIRECTORY`` folder,
in addition to the XML report.

The function call :ref:```add_cppcheck_target_to_all()``<AddCppCheckTargetToAll>`.

.. command:: create_cppcheck_target

   .. code-block:: cmake

      create_cppcheck_target(<target>)

   where

   ``target``
   The target to which an analysis target should be created. The target must be part of the use of ``add_library`` or
   ``add_executable``

From the target, the includes and source files are found and passed as a parameter to ``cppcheck``.

.. note::

   The following variables may be set before calling this function to modify the way the check is run:

   - ``CPPCHECK_BUILD_DIRECTORY``: The CppCheck build folder. A sub-folder with the name ``<target>`` is created, all
                                   files resulting from the execution of ``cppcheck`` will be put there.
   - ``CPPCHECK_WORKING_DIRECTORY``: The working directory where ``cppcheck`` will be executed
   - ``CPPCHECK_COMMAND_LINE_ARGUMENTS``: The default arguments passed to ``cppcheck``
   - ``CPPCHECK_REPORT_DIRECTORY``: The CppCheck HTML report folder. A sub-folder with the name ``<target>`` is created,
                                    all files resulting from the execution of ``cppcheck-htmlreport`` will be put there.
#]=======================================================================]
function(CREATE_CPPCHECK_TARGET target)
    set(cppcheck_target cppcheck-${target})

    message(CHECK_START "Set up target '${cppcheck_target}' for ${target}")

    find_package(CppCheck)

    if(NOT TARGET ${target})
        message(CHECK_FAIL "aborted, '${target}' is not an existing target")
        return()
    elseif(NOT CPPCHECK_FOUND)
        message(CHECK_FAIL "aborted, 'cppcheck' was not found")
        return()
    endif()

    list(APPEND CMAKE_MESSAGE_INDENT "  ")

    # NOTE Unlike the include directories, the paths to the source files are relative, so it is necessary to recompose
    # the absolute path by adding to the beginning of the relational path the absolute path where the target is declared
    get_target_property(TARGET_SOURCE_DIR ${target} SOURCE_DIR)
    set(CPPCHECK_BUILD ${CPPCHECK_BUILD_DIRECTORY}/${target}) # Path to the CppCheck output directory
    set(CPPCHECK_XML_REPORT ${CPPCHECK_BUILD}/${target}_cppcheck_report.xml) # Path to the CppCheck XML output file
    file(MAKE_DIRECTORY ${CPPCHECK_BUILD}) # Tell CMake to create the build directory

    # Set up cppcheck target

    # NOTE There is a use of the expression generator of CMake because the include directories are not available at the
    # configuration time, the use of the expression generator makes it possible to find these files during the phase of
    # build (execution of the command)
    #
    # Using a semicolon ($<SEMICOLON>) to separate arguments and adding the COMMAND_EXPAND_LISTS option means that paths
    # with spaces will be handled correctly.
    add_custom_target(
        ${cppcheck_target} ALL
        COMMAND
            ${CPPCHECK_EXECUTABLE} ${CPPCHECK_COMMAND_LINE_ARGUMENTS} --cppcheck-build-dir=${CPPCHECK_BUILD}
            --output-file=${CPPCHECK_XML_REPORT}
            "--includes-file=$<JOIN:$<TARGET_PROPERTY:${target},INCLUDE_DIRECTORIES>,$<SEMICOLON>--includes-file=>"
            "${TARGET_SOURCE_DIR}/$<JOIN:$<TARGET_PROPERTY:${target},SOURCES>,$<SEMICOLON>${TARGET_SOURCE_DIR}/>"
        COMMAND_EXPAND_LISTS VERBATIM
        WORKING_DIRECTORY ${CPPCHECK_WORKING_DIRECTORY}
        COMMENT "Generating static analysis report of the code of ${target} in XML format")
    # TODO clean *.c.dump and *.c.ctu-info files -I $<JOIN:$<TARGET_PROPERTY:${CCSDS_LIB},INCLUDE_DIRECTORIES>, -I >

    # Add the HTML report generation as dependecy of the cppcheck target
    message(CHECK_START "Add HTML report generation")

    find_package(CppCheckHtmlReport)

    if(CPPCHECK_HTMLREPORT_FOUND)
        set(CPPCHECK_HTML_BUILD_DIR ${CPPCHECK_REPORT_DIRECTORY}/${target})
        file(MAKE_DIRECTORY ${CPPCHECK_HTML_BUILD_DIR}) # Tell CMake to create the build directory

        add_custom_command(
            TARGET ${cppcheck_target}
            POST_BUILD
            COMMAND ${CPPCHECK_HTML_REPORT_EXECUTABLE} --source-dir=${TARGET_SOURCE_DIR} --file=${CPPCHECK_XML_REPORT}
                    --report-dir=${CPPCHECK_HTML_BUILD_DIR} --title=${target}
            WORKING_DIRECTORY ${CPPCHECK_WORKING_DIRECTORY}
            COMMENT "Converting XML report into HTML report for ${target}")
        # Inform the build folder to CMake to allow it to clean it
        set_property(
            TARGET ${cppcheck_target}
            APPEND
            PROPERTY ADDITIONAL_CLEAN_FILES ${REPORT_DIR})

        message(CHECK_PASS "target '${cppcheck_target}' generate HTML report")
    else(CPPCHECK_HTMLREPORT_FOUND)
        message(CHECK_FAIL "aborted, 'cppcheck-htmlreport' was not found")
    endif(CPPCHECK_HTMLREPORT_FOUND)

    add_cppcheck_target_to_all(${cppcheck_target})

    list(POP_BACK CMAKE_MESSAGE_INDENT)

    message(CHECK_PASS "successfully configured")
endfunction(CREATE_CPPCHECK_TARGET)

# ]=======================================================================]
function(ADD_CPPCHECK_TARGET_TO_ALL cppcheck_target)
    set(CPPCHECK_ALL cppcheck-all)

    message(STATUS "  Connect ${cppcheck_target} to ${CPPCHECK_ALL}")

    if(NOT TARGET ${CPPCHECK_ALL})
        add_custom_target(${CPPCHECK_ALL} COMMENT "Execute all the 'clangformat' target")
    endif(NOT TARGET ${CPPCHECK_ALL})

    add_dependencies(${CPPCHECK_ALL} ${cppcheck_target})

endfunction(ADD_CPPCHECK_TARGET_TO_ALL)

if(ENABLE_ANALYSIS)
    # Create new cache variable used by the different cppchec target
    set(CPPCHECK_COMMAND_LINE_ARGUMENTS
        "--enable=all" "--addon=${CMAKE_CURRENT_SOURCE_DIR}/misra.json" "--dump" "--xml-version=2" "--inline-suppr"
        "--quiet"
        CACHE STRING "List of the argument passed at the command line cppcheck")
    set(CPPCHECK_WORKING_DIRECTORY
        ${CMAKE_CURRENT_SOURCE_DIR}
        CACHE PATH "Working directory of the execution of the cppcheck analysis")
    set(CPPCHECK_BUILD_DIRECTORY
        ${CMAKE_CURRENT_BINARY_DIR}
        CACHE PATH "Base path of the build folder for CppCheck commands")
    set(CPPCHECK_REPORT_DIRECTORY
        ${CMAKE_CURRENT_SOURCE_DIR}/build/html
        CACHE PATH "Base path of the build folder for CppCheck HTML report")
endif(ENABLE_ANALYSIS)
