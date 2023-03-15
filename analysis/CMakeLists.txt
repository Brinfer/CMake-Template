#[=======================================================================[.rst:
ReferenceTargetForAnalysis
--------------------------

Set up an analysis target.

The function call :ref:```create_cppcheck_target()``<CreateCppcheckTarget>`
and :ref:```create_clangformat_target()``<CreateClangFormatTarget>`.

.. command:: reference_target_for_analysis

   .. code-block:: cmake

      reference_target_for_analysis(<target>)

   where

   ``target``
   The target to which an analysis target should be created. The target must be part of the use of ``add_library`` or
   ``add_executable``

.. note::

   The following variables may be set before calling this function to modify the way the check is run:

   - ``ENABLE_ANALYSIS``: Option to disable or not the analysis targets
#]=======================================================================]
function(REFERENCE_TARGET_FOR_ANALYSIS target)
    message(CHECK_START "Set up analysis for target ${target}")

    if(TARGET ${target})
        list(APPEND CMAKE_MESSAGE_INDENT "  ")

        if(ENABLE_ANALYSIS)
            create_cppcheck_target(${target})
            create_clangformat_target(${target})
        else(ENABLE_ANALYSIS)
            message(CHECK_FAIL "aborted, analysis option is disabled")
        endif(ENABLE_ANALYSIS)

        list(POP_BACK CMAKE_MESSAGE_INDENT)
    else(TARGET ${target})
        message(CHECK_FAIL "target does not exist")

    endif(TARGET ${target})
endfunction(REFERENCE_TARGET_FOR_ANALYSIS)

#[=======================================================================[.rst:
CreateClangFormatTarget
-----------------------

Set up an analysis target using ClangFormat.

.. command:: create_clangformat_target

   .. code-block:: cmake

      create_clangformat_target(<target>)

   where

   ``target``
   The target to which an analysis target should be created. The target must be part of the use of ``add_library`` or
   ``add_executable``
#]=======================================================================]
function(CREATE_CLANGFORMAT_TARGET target)
    set(clangformat_target clangformat-${target})
    set(CLANGFORMAT_FILE ${CMAKE_SOURCE_DIR}/.clang-format)

    message(CHECK_START "Set up target '${clangformat_target}' for ${target}")
    message(STATUS "  Use the clang-format file: ${CLANGFORMAT_FILE}")
    find_package(ClangFormat)

    if(NOT TARGET ${target})
        message(CHECK_FAIL "aborted, '${target}' is not an existing target")
        return()
    elseif(NOT CLANGFORMAT_FOUND)
        message(CHECK_FAIL "aborted, 'clang-format' was not found")
        return()
    elseif(NOT EXISTS ${CLANGFORMAT_FILE})
        message(CHECK_FAIL "aborted, clang-format file is not found")
    endif()

    # NOTE Unlike the include directories, the paths to the source files are relative, so it is necessary to recompose
    # the absolute path by adding to the beginning of the relational path the absolute path where the target is declared
    get_target_property(TARGET_SOURCE_DIR ${target} SOURCE_DIR)
    get_target_property(TARGET_INCLUDE_DIR ${target} INCLUDE_DIRECTORIES)

    # NOTE It is not possible to find the headers used by a target directly, so the solution is to do a recursive reload
    # of the *.h* files in the includes folders and add them in a list
    set(header_files "")
    foreach(include_dir ${TARGET_INCLUDE_DIR})
        set(header_file_include_folder)
        file(GLOB_RECURSE header_file_include_folder ${include_dir}/*.h*)
        list(APPEND header_files ${header_file_include_folder})
    endforeach(include_dir)

    add_custom_target(
        ${clangformat_target} ALL
        COMMAND
            ${CLANG_FORMAT_EXECUTABLE} --dry-run --Werror --style=file:${CLANGFORMAT_FILE}
            "${TARGET_SOURCE_DIR}/$<JOIN:$<TARGET_PROPERTY:${target},SOURCES>,$<SEMICOLON>${TARGET_SOURCE_DIR}/>"
            ${header_files}
        COMMAND_EXPAND_LISTS VERBATIM
        COMMENT "Check the correct formatting of the source and header files for the ${target}")

    add_clangformat_target_to_all(${clangformat_target})
    message(CHECK_PASS "successfully configured")

endfunction(CREATE_CLANGFORMAT_TARGET)

#[=======================================================================[.rst:
AddClangFormatTargetToAll
-------------------------

Create the target ``clangformat-all`` if not exist, and adds a dependency between ``clangformat-all``
and ``clang_target``.


.. command:: add_clangformat_target_to_all

   .. code-block:: cmake

      add_clangformat_target_to_all(<clang_target>)

   where

   ``clang_target``
   The target that must be executed before the execution of ``clangformat``.
#]=======================================================================]
function(ADD_CLANGFORMAT_TARGET_TO_ALL clang_target)
    set(CLANGFORMAT_ALL clangformat-all)

    message(STATUS "  Connect ${clang_target} to ${CLANGFORMAT_ALL}")

    if(NOT TARGET ${CLANGFORMAT_ALL})
        add_custom_target(${CLANGFORMAT_ALL} COMMENT "Execute all the 'clangformat' target")
    endif(NOT TARGET ${CLANGFORMAT_ALL})

    add_dependencies(${CLANGFORMAT_ALL} ${clang_target})

endfunction(ADD_CLANGFORMAT_TARGET_TO_ALL)

option(ENABLE_ANALYSIS "Option to configure or not the analysis target" ON)

add_subdirectory(cppcheck)
