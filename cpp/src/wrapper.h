#pragma once

#include "..\..\sdk\inc\natives.h"
#include "..\..\sdk\inc\types.h"
#include "..\..\sdk\inc\enums.h"

#include "..\..\sdk\inc\main.h"

#include <Python.h>

static PyObject* EmbStuff(PyObject* self, PyObject* args);
static PyObject* Py3kEmbInit();
void Py3kInitialize();
void Py3kFinalize();
void Py3kWrapper();