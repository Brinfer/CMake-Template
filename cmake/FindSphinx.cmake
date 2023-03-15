include(FindPackageHandleStandardArgs)

find_program(
  SPHINX_EXECUTABLE
  NAMES sphinx-build
  HINTS $ENV{SPHINX_FOLDER} /usr/
  PATH_SUFFIXES bin
  DOC "Sphinx documentation generator")
mark_as_advanced(SPHINX_EXECUTABLE)

find_package_handle_standard_args(
  Sphinx "Failed to find sphinx-build executable" SPHINX_EXECUTABLE)
