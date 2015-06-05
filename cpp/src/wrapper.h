#pragma once

#include "..\..\sdk\inc\natives.h"
#include "..\..\sdk\inc\types.h"
#include "..\..\sdk\inc\enums.h"

#include "..\..\sdk\inc\main.h"

#include "natives_wrap.h"

#include <Python.h>
#include <iostream>
#include <fstream>

#define PY3KWRAPPER_VERSION "0.9.7"

enum Py3kAction : int {
	NONE,
	STOP,
	RESTART
};

const char* game_version_name(eGameVersion version);
char* wchar_to_string(const wchar_t* wchar_message);
char* time_now();
void log_(const char* type, const char* message);
void log_debug(const char* message);
void log_error(const char* message);
void log_exception(const char* message);
std::string Py3kStr(PyObject* obj);
bool Py3kException();
bool Py3kException(PyObject* obj);
void Py3kKeyEvent(int code, bool down, bool alt, bool ctrl, bool shift);
void Py3kTick();
void Py3kInitialize();
void Py3kFinalize();
void Py3kReinitialize();
void OnKeyboardMessage(DWORD key, WORD repeats, BYTE scanCode, BOOL isExtended, BOOL isWithAlt, BOOL wasDownBefore, BOOL isUpNow);
void Py3kWrapperStart();
void Py3kWrapperStop();
