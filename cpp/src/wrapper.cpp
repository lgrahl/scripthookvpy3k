#include "wrapper.h"

void Py3kInitialize() {
	if (!Py_IsInitialized()) {
		PyObject* pName;
		PyObject* pModule;
		PyObject* pDict;
		PyObject* pFunc;

		// Add module
		PyImport_AppendInittab("_gta_native", &PyInit__gta_native);

		// Initialise interpreter
		Py_Initialize();

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
			PyObject_CallObject(pFunc, NULL);
		} else {
			// TODO: Print error
			PyErr_Print();
		}

		// Clean up
		Py_DECREF(pName);
		Py_DECREF(pModule);
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
	// Initialise
	Py3kInitialize();

	while (true) {
		// Restart
		if (IsKeyJustUp(VK_F12)) {
			// Finalise and reinitialise
			Py3kFinalize();
			Py3kInitialize();
		}
		WAIT(0);
	}
}

