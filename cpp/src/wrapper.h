#pragma once

#include "..\..\sdk\inc\natives.h"
#include "..\..\sdk\inc\types.h"
#include "..\..\sdk\inc\enums.h"

#include "..\..\sdk\inc\main.h"

#include "keyboard.h"
#include "natives_wrap.h"

#include <Python.h>
#include <iostream>
#include <fstream>

char* time_now();
void log_(char* type, std::string message);
void log_(char* type, wchar_t* message);
void log_debug(std::string message);
void log_debug(wchar_t* message);
void log_error(std::string message);
void log_error(wchar_t* message);
void Py3kInitialize();
void Py3kFinalize();
void Py3kReinitialize();
void Py3kWrapper();
