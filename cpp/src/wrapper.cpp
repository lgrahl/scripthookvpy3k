#include "wrapper.h"

void Py3kInitialize() {
	if (!Py_IsInitialized()) {
		// Add module
		PyImport_AppendInittab("_gta_native", &PyInit__gta_native);

		// Initialise interpreter
		Py_Initialize();
	}
}

void Py3kFinalize() {
	if (Py_IsInitialized()) {
		// Finalise interpreter
		Py_Finalize();
	}
}

void Py3kWrapper()
{
	int initializedCount = 0;

	while (true) {
		// Initalise
		if (IsKeyJustUp(VK_F11)) {
			PyObject* pName;
			PyObject* pModule;
			PyObject* pDict;
			PyObject* pFunc;
			PyObject* pArgs;

			// Initialise interpreter
			Py3kInitialize();

			// Reference module name
			pName = PyUnicode_FromString("gta");
			// Reference module object
			pModule = PyImport_Import(pName);
			// Get dictionary of module (borrowed)
			pDict = PyModule_GetDict(pModule);
			// Get hook function (borrowed)
			pFunc = PyDict_GetItemString(pDict, "_init");

			// Call init function
			if (PyCallable_Check(pFunc)) {
				pArgs = Py_BuildValue("(i)", initializedCount);
				PyObject_CallObject(pFunc, pArgs);
				Py_DECREF(pArgs);
				initializedCount += 1;
			} else {
				// TODO: Print error
				PyErr_Print();
			}

			// Clean up
			Py_DECREF(pName);
			Py_DECREF(pModule);
		}

		// Finalise
		if (IsKeyJustUp(VK_F12)) {
			// Finalise interpreter
			Py3kFinalize();
		}
		WAIT(0);
	}
}

