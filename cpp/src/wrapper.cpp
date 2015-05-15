#include "wrapper.h"

PyObject* pExit = nullptr;
HANDLE lock = nullptr;
HANDLE py3k;
std::ofstream logger("scripthookvpy3k.wrapper.log", std::ios_base::app | std::ios_base::out);

void log_(char* type, char* message) {
	time_t now = time(0);
	struct tm tstruct;
	char buffer[80];
	tstruct = *localtime(&now);
	strftime(buffer, sizeof(buffer), "%Y-%m-%d %X ", &tstruct);
	logger << buffer << type << ": " << message << std::endl;
	logger.flush();
}

void log_debug(char* message) {
	log_("Debug", message);
}

void log_error(char* message) {
	log_("Error", message);
}

DWORD WINAPI Py3kThreadInitialize(LPVOID _) {
	// Check if there is a lock
	if (lock == nullptr) {
		log_error("Py3kThreadInitialize lock is null");
		return 1;
	}

	// Acquire lock
	log_debug("Py3kFinalize acquire");
	WaitForSingleObject(lock, INFINITE);

	if (!Py_IsInitialized()) {
		PyObject* pName;
		PyObject* pModule;
		PyObject* pDict;
		PyObject* pInit;

		// Add module
		log_debug("Creating module _gta_native");
		PyImport_AppendInittab("_gta_native", &PyInit__gta_native);

		// Initialise interpreter
		log_debug("Initialising");
		Py_Initialize();
		log_debug("Initialised");

		// Reference module name
		pName = PyUnicode_FromString("gta");
		// Reference module object
		log_debug("Importing module: gta");
		pModule = PyImport_Import(pName);
		// Get dictionary of module (borrowed)
		pDict = PyModule_GetDict(pModule);
		// Get init and exit functions (borrowed)
		log_debug("Referencing functions");
		pInit = PyDict_GetItemString(pDict, "_init");
		pExit = PyDict_GetItemString(pDict, "_exit");
		// Clean up
		log_debug("Cleaning up references");
		Py_DECREF(pName);
		Py_DECREF(pModule);

		// Release lock
		log_debug("Py3kFinalize release");
		ReleaseMutex(lock);

		// Call init function
		if (PyCallable_Check(pInit)) {
			log_debug("Calling gta._init()");
			PyObject_CallObject(pInit, NULL);
			log_debug("Returned from gta._init()");
		} else {
			log_error("Init function is not callable");
		}
	} else {
		log_debug("Already initialised");
		// Release lock
		log_debug("Py3kFinalize release");
		ReleaseMutex(lock);
	}

	return 0;
}

void Py3kInitialize() {
	// Create thread for Python and initialise
	log_debug("Creating thread");
	py3k = CreateThread(nullptr, 0, Py3kThreadInitialize, nullptr, 0, nullptr);
}

void Py3kFinalize() {
	// Check if there is a lock
	if (lock == nullptr) {
		log_error("Py3kFinalize lock is null");
		return;
	}

	// Acquire lock
	log_debug("Py3kFinalize acquire");
	WaitForSingleObject(lock, INFINITE);

	if (Py_IsInitialized()) {
		log_debug("Finalising");
		// Call exit function
		if (pExit != nullptr) {
			if (PyCallable_Check(pExit)) {
				log_debug("Calling gta._exit()");
				PyObject_CallObject(pExit, NULL);
				log_debug("Returned from gta._exit()");
			} else {
				log_error("Exit function is not callable");
			}
		}

		// Reset vars
		pExit = nullptr;

		// Finalise interpreter
		Py_Finalize();
		log_debug("Finalised");
	} else {
		log_debug("Already finalised");
	}

	// Release lock
	log_debug("Py3kFinalize release");
	ReleaseMutex(lock);
}

void Py3kReinitialize() {
	Py3kFinalize();
	Py3kInitialize();
}

void Py3kWrapper() {
	// Create lock
	if (lock == nullptr) {
		log_debug("Creating mutex");
		lock = CreateMutex(nullptr, false, nullptr);
	}

	// (Re)Initialize
	Py3kReinitialize();

	// Main loop
	while (true) {
		// Restart
		if (IsKeyJustUp(VK_F12)) {
			// Reinitialize
			log_debug("Reinitialising Python");
			Py3kReinitialize();
			continue;
		}

		// TODO: Handle tick
		// log_debug("TODO: Handle tick");
		// Py3kTick();

		// Yield
		scriptWait(0);
	}
}
