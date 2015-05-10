#pragma once

#include "..\..\sdk\inc\natives.h"
#include "..\..\sdk\inc\types.h"
#include "..\..\sdk\inc\enums.h"

#include "..\..\sdk\inc\main.h"

#include "keyboard.h"
#include "natives_wrap.h"

#include <Python.h>

void Py3kInitialize();
void Py3kFinalize();
void Py3kWrapper();