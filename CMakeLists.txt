cmake_minimum_required(VERSION 3.23.2)

# initialize the SDK based on PICO_SDK_PATH
# note: this must happen before project()
include(pico_sdk_import.cmake)

project(byte-beat)

# initialize the Raspberry Pi Pico SDK
pico_sdk_init()


add_subdirectory(serial)
