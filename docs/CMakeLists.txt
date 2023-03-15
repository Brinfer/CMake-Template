#[=======================================================================[.rst:
ReferenceTargetForDocs
----------------------

Set up an documentation target.

The function call :ref:```create_doxygen_target()``<CreateDoxygenTarget>`,
:ref:```add_doxygen_target_to_docs()``<AddDoxygenToDocs>` and :ref:```link_sphinx_generation()``<LinkSphinxGeneration>`.

.. command:: create_doxygen_target

   .. code-block:: cmake

      reference_target_for_docs(<target>)

   where

   ``target``
   The target to which an documentation should be a generated. The target must be part of the use of ``add_library`` or
   ``add_executable``

.. note::

   The following variables may be set before calling this function to modify the way the check is run:

   - ``ENABLE_DOCS``: Option to disable or not the analysis targets
#]=======================================================================]
function(REFERENCE_TARGET_FOR_DOCS target)
    message(CHECK_START "Set up docs for target ${target}")
    set(docs_all docs)

    if(TARGET ${target})
        list(APPEND CMAKE_MESSAGE_INDENT "  ")

        if(ENABLE_DOCS)
            create_doxygen_target(${target})
            link_sphinx_generation()
        else(ENABLE_DOCS)
            message(CHECK_FAIL "aborted, analysis option is disabled")
        endif(ENABLE_DOCS)

        list(POP_BACK CMAKE_MESSAGE_INDENT)
    else(TARGET ${target})
        message(CHECK_FAIL "target does not exist")

    endif(TARGET ${target})
endfunction(REFERENCE_TARGET_FOR_DOCS)

#[=======================================================================[.rst:
CreateDoxygenTarget
-------------------

Set up an doxygen target.

The function call :ref:```add_doxygen_target_to_docs()``<AddDoxygenToDocs>`.

.. command:: create_doxygen_target

   .. code-block:: cmake

      create_doxygen_target(<target>)

   where

   ``target``
   The target to which an doxygen target should be created. The target must be part of the use of ``add_library`` or
   ``add_executable``
#]=======================================================================]
function(CREATE_DOXYGEN_TARGET target)
    set(doxygen_target doxygen-${target})

    set(DOXYGEN_EXCLUDE_PATTERNS */build/* */docs/* */cmake/* */venv/*)
    set(DOXYGEN_GENERATE_HTML NO)
    set(DOXYGEN_GENERATE_XML YES)
    set(DOXYGEN_OUTPUT_DIRECTORY ${DOXYGEN_BASE_BUILD_DIRECTORY}/${target})
    set(DOXYGEN_OPTIMIZE_OUTPUT_FOR_C YES)
    set(DOXYGEN_EXTRACT_ALL YES)
    set(DOXYGEN_EXTRACT_PRIVATE YES)
    set(DOXYGEN_EXTRACT_PRIV_VIRTUAL YES)
    set(DOXYGEN_EXTRACT_STATIC YES)
    set(DOXYGEN_RECURSIVE YES)

    message(CHECK_START "Set up target '${doxygen_target}' for target '${target}'")
    find_package(Doxygen)

    if(NOT TARGET ${target})
        message(CHECK_FAIL "aborted, '${target}' is not an existing target")
        return()
    elseif(NOT DOXYGEN_FOUND)
        message(CHECK_FAIL "aborted, 'doxygen' was not found")
        return()
    endif()

    get_target_property(TARGET_SOURCE_DIR ${target} SOURCE_DIR)

    doxygen_add_docs(
        ${doxygen_target} ${TARGET_SOURCE_DIR} ALL
        COMMENT "Generating documentation with Doxygen for '${target}'"
        WORKING_DIRECTORY ${TARGET_SOURCE_DIR})
    set_property(
        TARGET ${doxygen_target}
        APPEND
        PROPERTY ADDITIONAL_CLEAN_FILES ${DOXYGEN_OUTPUT_DIRECTORY})

    add_doxygen_target_to_docs(${doxygen_target})
    message(CHECK_PASS "successfully configured")

endfunction(CREATE_DOXYGEN_TARGET)

#[=======================================================================[.rst:
LinkSphinxGeneration
--------------------

Set up the documentation target.

If the target docs already exists, then the sphinx operation is placed in post build, otherwise the target is created.

.. command:: link_sphinx_generation

   .. code-block:: cmake

      link_sphinx_generation()
#]=======================================================================]
function(LINK_SPHINX_GENERATION)
    find_package(Sphinx)

    if((Sphinx_FOUND) AND (NOT SPHINX_GENERATION_SET_UP))
        if(TARGET ${docs_all})
            message(STATUS "Add Sphinx generation target as post build of ${docs_all}")
            add_custom_command(
                TARGET ${docs_all}
                POST_BUILD
                COMMAND
                    ${SPHINX_EXECUTABLE} -b html -Drelease=${PROJECT_VERSION} -Dcopyright=${PROJECT_COPYRIGHT}
                    -Dauthor=${PROJECT_AUTHOR} -Dproject=${PROJECT_NAME} ${SPHINX_SOURCE_DIRECTORY}
                    ${SPHINX_BUILD_DIRECTORY}
                WORKING_DIRECTORY ${SPHINX_SOURCE_DIRECTORY}
                COMMENT "Generating documentation with Sphinx")

            set(SPHINX_GENERATION_SET_UP
                YES
                CACHE BOOL "Saves the fact that a target to generate sphinx documentation already exists")

        else(TARGET ${docs_all})
            message(STATUS "Add Sphinx generation target as target ${docs_all}")
            add_custom_target(
                ${docs_target}
                COMMAND
                    ${SPHINX_EXECUTABLE} -b html -Drelease=${PROJECT_VERSION} -Dcopyright=${PROJECT_COPYRIGHT}
                    -Dauthor=${PROJECT_AUTHOR} -Dproject=${PROJECT_NAME} ${SPHINX_SOURCE_DIRECTORY}
                    ${SPHINX_BUILD_DIRECTORY}
                WORKING_DIRECTORY ${SPHINX_SOURCE_DIRECTORY}
                COMMENT "Generating documentation with Sphinx")
        endif(TARGET ${docs_all})

        set_property(
            TARGET ${docs_target}
            APPEND
            PROPERTY ADDITIONAL_CLEAN_FILES ${SPHINX_BUILD_DIRECTORY})

    endif((Sphinx_FOUND) AND (NOT SPHINX_GENERATION_SET_UP))
endfunction(LINK_SPHINX_GENERATION)

#[=======================================================================[.rst:
AddDoxygenToDocs
----------------

Create the target ``docs`` if not exist, and adds a dependency between ``docs`` and ``doxygen_target``


.. command:: add_doxygen_target_to_docs

   .. code-block:: cmake

      add_doxygen_target_to_docs(<doxygen_target>)

   where

   ``doxygen_target``
   The target that must be executed before the execution of ``docs``.
#]=======================================================================]
function(ADD_DOXYGEN_TARGET_TO_DOCS doxygen_target)
    message(STATUS "  Connect '${doxygen_target}' to '${docs_all}'")

    if(NOT TARGET ${docs_all})
        add_custom_target(${docs_all} COMMENT "Execute all the 'doxygen' target")
    endif(NOT TARGET ${docs_all})

    add_dependencies(${docs_all} ${doxygen_target})

endfunction(ADD_DOXYGEN_TARGET_TO_DOCS)

option(ENABLE_DOCS "Option to configure or not the documentation targets" ON)

if(ENABLE_DOCS)
    set(SPHINX_SOURCE_DIRECTORY
        ${CMAKE_CURRENT_SOURCE_DIR}
        CACHE PATH "Path to the Sphinx input directory")
    set(SPHINX_BUILD_DIRECTORY
        ${CMAKE_CURRENT_SOURCE_DIR}/build/html
        CACHE PATH "Path to the Sphinx output directory")
    set(DOXYGEN_BASE_BUILD_DIRECTORY
        ${CMAKE_CURRENT_SOURCE_DIR}/build/doxygen
        CACHE PATH "Path to the Doxygen output directory")
    set(SPHINX_GENERATION_SET_UP
        NO
        CACHE BOOL "Saves the fact that a target to generate sphinx documentation already exists")
endif(ENABLE_DOCS)
