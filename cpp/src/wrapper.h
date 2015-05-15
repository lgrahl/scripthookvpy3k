#pragma once

#include "..\..\sdk\inc\natives.h"
#include "..\..\sdk\inc\types.h"
#include "..\..\sdk\inc\enums.h"

#include "..\..\sdk\inc\main.h"

#include "keyboard.h"
#include "natives_wrap.h"

#include <iostream>
#include <fstream>
#include <Python.h>

void log_(char* type, char* message);
void log_debug(char* message);
void log_error(char* message);
DWORD WINAPI Py3kThreadInitialize(LPVOID _);
void Py3kInitialize();
void Py3kFinalize();
void Py3kReinitialize();
void Py3kWrapper();
