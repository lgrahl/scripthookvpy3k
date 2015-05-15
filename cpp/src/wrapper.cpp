#include "wrapper.h"

PyThreadState* pThreadState;
PyObject* pExit = nullptr;
std::ofstream logger("scripthookvpy3k.wrapper.log", std::ios_base::app | std::ios_base::out);

char* time_now() {
	char* buffer = new char[80];
	time_t now = time(0);
	struct tm time_info;
	localtime_s(&time_info, &now);
	strftime(buffer, 80, "%Y-%m-%d %X ", &time_info);
	return buffer;
}

void log_(char* type, std::string message) {
	char* now = time_now();
	logger << now << type << ": " << message.c_str() << std::endl;
	logger.flush();
	delete now;
}

void log_(char* type, wchar_t* message) {
	char* now = time_now();
	logger << now << type << ": " << message << std::endl;
	logger.flush();
	delete now;
}

void log_debug(std::string message) {
	log_("Debug", message);
}

void log_debug(wchar_t* message) {
	log_("Debug", message);
}

void log_error(std::string message) {
	log_("Error", message);
}

void log_error(wchar_t* message) {
	log_("Error", message);
}

void Py3kInitialize() {
	log_debug("Py3kInitialize called");

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

		// Initialise and acquire GIL
		log_debug("Initialising and acquiring GIL");
		PyEval_InitThreads();

		// Get version (borrowed)
		log_debug(std::string(Py_GetVersion()));

		// Get path (borrowed)
		wchar_t* path = Py_GetPath();
		log_debug(path);

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

		// Call init function
		if (PyCallable_Check(pInit)) {
			log_debug("Calling gta._init()");
			PyObject_CallObject(pInit, NULL);
			log_debug("Returned from gta._init()");
		} else {
			log_error("Init function is not callable");
		}

		// Release GIL
		log_debug("Releasing GIL");
		pThreadState = PyEval_SaveThread();
	} else {
		log_debug("Already initialised");
	}
}

void Py3kFinalize() {
	log_debug("Py3kFinalize called");

	if (Py_IsInitialized()) {
		log_debug("Finalising");

		// Acquire GIL
		log_debug("Acquiring GIL");
		PyEval_RestoreThread(pThreadState);

		// Call exit function
		if (PyCallable_Check(pExit)) {
			log_debug("Calling gta._exit()");
			PyObject_CallObject(pExit, NULL);
			log_debug("Returned from gta._exit()");
		} else {
			log_error("Exit function is not callable");
		}

		// Reset vars
		pExit = nullptr;
		pThreadState = nullptr;

		// Finalise interpreter
		Py_Finalize();
		log_debug("Finalised");
	}
}

void Py3kReinitialize() {
	Py3kFinalize();
	Py3kInitialize();
}

void Py3kWrapper() {
	log_debug("Py3kWrapper called");

	// (Re)Initialize
	Py3kReinitialize();

	// Main loop
	while (true) {
		// Stop
		if (IsKeyJustUp(VK_DELETE)) {
			// Finalize
			log_debug("Enforcing stop");
			Py3kFinalize();
			continue;
		}

		// Restart
		if (IsKeyJustUp(VK_F12)) {
			// Reinitialize
			log_debug("Reloading");
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

