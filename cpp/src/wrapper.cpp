#include "wrapper.h"
#include "keyboard.h"

#include <string>

static PyMethodDef EmbMethods[] = {
	{ "stuff", EmbStuff, METH_VARARGS,
	"Increase wanted level." },
	{ NULL, NULL, 0, NULL }
};

static PyModuleDef EmbModule = {
	PyModuleDef_HEAD_INIT, "gta_native", NULL, -1, EmbMethods,
	NULL, NULL, NULL, NULL
};

static PyObject* EmbStuff(PyObject* self, PyObject* args) {
	BOOL bPlayerExists = ENTITY::DOES_ENTITY_EXIST(PLAYER::PLAYER_PED_ID());
	Player player = PLAYER::PLAYER_ID();
	Ped playerPed = PLAYER::PLAYER_PED_ID();
	int wantedLevel = PLAYER::GET_PLAYER_WANTED_LEVEL(player) + 1;
	PLAYER::SET_PLAYER_WANTED_LEVEL(player, wantedLevel, 0);
	PLAYER::SET_PLAYER_WANTED_LEVEL_NOW(player, 0);
	return PyUnicode_FromFormat("Your wanted level is now %d", wantedLevel);
}

static PyObject* Py3kEmbInit() {
	return PyModule_Create(&EmbModule);
}

void Py3kInitialize() {
	if (!Py_IsInitialized()) {
		// Add module
		PyImport_AppendInittab("gta_native", &Py3kEmbInit);

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

		if (IsKeyJustUp(VK_F4)) {
			BOOL bPlayerExists = ENTITY::DOES_ENTITY_EXIST(PLAYER::PLAYER_PED_ID());
			Player player = PLAYER::PLAYER_ID();
			Ped playerPed = PLAYER::PLAYER_PED_ID();
			PLAYER::SET_PLAYER_WANTED_LEVEL(player, PLAYER::GET_PLAYER_WANTED_LEVEL(player) + 1, 0);
			PLAYER::SET_PLAYER_WANTED_LEVEL_NOW(player, 0);
		}
		WAIT(0);
	}
}

