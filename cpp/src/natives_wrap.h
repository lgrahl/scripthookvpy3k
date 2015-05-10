#pragma once

#include "..\..\sdk\inc\natives.h"
#include "..\..\sdk\inc\types.h"
#include "..\..\sdk\inc\enums.h"

#include "Python.h"

/* Warning: This is a very nasty hack and has been extracted
   from the SWIG generated file. It's likely that this will
   fail on other devices. */
extern "C" {
	__declspec(dllexport)
	PyObject* PyInit__gta_native(void);
}