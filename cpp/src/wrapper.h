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

#define PY3KWRAPPER_VERSION "0.9.3"

const char* game_version_name(eGameVersion version);
char* wchar_to_string(const wchar_t* wchar_message);
char* time_now();
void log_(const char* type, const char* message);
void log_debug(const char* message);
void log_error(const char* message);
void log_exception(const char* message);
std::string Py3kStr(PyObject* obj);
bool Py3kException(PyObject* obj);
bool Py3kException();
void Py3kInitialize();
void Py3kFinalize();
void Py3kReinitialize();
void Py3kWrapperStart();
void Py3kWrapperStop();
