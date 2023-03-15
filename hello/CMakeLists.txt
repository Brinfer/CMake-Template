cmake_minimum_required(VERSION 3.20)

add_executable(hello main.c)

if(COMMAND reference_target_for_analysis)
reference_target_for_docs(${IPC_LIB})
endif(COMMAND reference_target_for_analysis)

reference_target_for_docs(hello)

