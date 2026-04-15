cmake_minimum_required(VERSION 3.20)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_C_STANDARD 11)

project(
    flowmeters
    VERSION 0.0.1
    DESCRIPTION "Manageme a flowmeter using the HART protocol")
set(PROJECT_AUTHOR "Brinfer")
set(PROJECT_COPYRIGHT "2022, ${PROJECT_AUTHOR}")

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

add_subdirectory(analysis)
add_subdirectory(docs)


