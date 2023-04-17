cmake_minimum_required(VERSION 3.20)

add_executable(hello main.c)

if(COMMAND reference_target_for_analysis)
    reference_target_for_analysis(hello)
endif(COMMAND reference_target_for_analysis)

if(COMMAND reference_target_for_docs)
    reference_target_for_docs(hello)
endif(COMMAND reference_target_for_docs)
