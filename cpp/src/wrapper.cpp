#include "wrapper.h"

Py3kAction action = NONE;
PyThreadState* pThreadState;
PyObject* pExit = nullptr;
PyObject* pTick = nullptr;
PyObject* pKeyEvent = nullptr;
std::ofstream logger("scripthookvpy3k.wrapper.log", std::ios_base::trunc | std::ios_base::out);

const char* game_version_name(eGameVersion version) {
	switch (version) {
		case VER_1_0_335_2_STEAM:
			return "1.0.335.2_STEAM";
		case VER_1_0_335_2_NOSTEAM:
			return "1.0.335.2_NOSTEAM";
		case VER_1_0_350_1_STEAM:
			return "1.0.350.1_STEAM";
		case VER_1_0_350_2_NOSTEAM:
			return "1.0.350.2_NOSTEAM";
		default:
			return "Unknown";
	}
}

char* wchar_to_string(const wchar_t* wchar_message) {
	size_t size = (wcslen(wchar_message) + 1) * 2;
	char* message = new char[size];
	size_t converted = 0;
	wcstombs_s(&converted, message, size, wchar_message, _TRUNCATE);
	return message;
}

char* time_now() {
	char* buffer = new char[80];
	time_t now = time(0);
	struct tm time_info;
	localtime_s(&time_info, &now);
	strftime(buffer, 80, "%Y-%m-%d %X ", &time_info);
	return buffer;
}

void log_(const char* type, const char* message) {
	char* now = time_now();
	logger << now << "@" << GetCurrentThreadId() << " " << type << ": " << message << std::endl;
	logger.flush();
	delete now;
}

void log_debug(const char* message) {
	log_("Debug", message);
}

void log_error(const char* message) {
	log_("Error", message);
}

void log_exception(const char* message) {
	log_("Exception", message);
}

std::string Py3kStr(PyObject* obj) {
	if (obj != nullptr) {
		PyObject* pStr = nullptr;
		PyObject* pValue = nullptr;

		// Get representation
		pStr = PyObject_Str(obj);
		if (pStr == nullptr) {
			log_error("Could not retrieve string representation from object");
			return std::string();
		}

		// Convert error value to UTF-8
		pValue = PyUnicode_AsUTF8String(pStr);
		if (pValue == nullptr) {
			log_error("Could not convert Unicode to UTF-8 string");
			Py_DECREF(pStr);
			return std::string();
		}

		// Get bytearray as string
		char* message = PyBytes_AsString(pValue);
		if (message == nullptr) {
			log_error("Could not convert bytes to string");
			Py_DECREF(pStr); Py_DECREF(pValue);
			return std::string();
		}

		Py_DECREF(pStr); Py_DECREF(pValue);
		return std::string(message);
	}
	else {
		return std::string();
	}
}

bool Py3kException() {
	PyObject* pType;
	PyObject* pValue;
	PyObject* pTraceback;
	PyObject* pModule;
	PyObject* pList;
	PyObject* pEmpty;
	PyObject* pMessage;

	// Fetch error (if any)
	PyErr_Fetch(&pType, &pValue, &pTraceback);
	PyErr_NormalizeException(&pType, &pValue, &pTraceback);
	if (pType == nullptr && pValue == nullptr && pTraceback == nullptr) {
		// No error
		return false;
	}

	// Import traceback module
	pModule = PyImport_ImportModule("traceback");
	if (pModule == nullptr) {
		log_error("Could not import 'traceback' module");
		return true;
	}

	// Get formatted exception as an iterable
	pList = PyObject_CallMethod(
		pModule, "format_exception", "OOO", pType,
		pValue == nullptr ? Py_None : pValue,
		pTraceback == nullptr ? Py_None : pTraceback
		);
	if (pList == nullptr) {
		log_error("Invoking traceback.format_exception failed");
		Py_DECREF(pModule);
		return true;
	}

	// Join iterable with an empty string
	pEmpty = PyUnicode_FromString("");
	if (pEmpty == nullptr) {
		log_error("Creating empty string failed");
		Py_DECREF(pModule); Py_DECREF(pList);
		return true;
	}
	pMessage = PyObject_CallMethod(pEmpty, "join", "O", pList);
	if (pMessage == nullptr) {
		log_error("Joining traceback list failed");
		Py_DECREF(pModule); Py_DECREF(pList); Py_DECREF(pEmpty);
		return true;
	}

	// Log the exception
	std::string message = Py3kStr(pMessage);
	if (!message.empty()) {
		log_exception(message.c_str());
	}

	// Clean up
	Py_DECREF(pModule); Py_DECREF(pList); Py_DECREF(pEmpty); Py_DECREF(pMessage);
	Py_XDECREF(pType); Py_XDECREF(pValue); Py_XDECREF(pTraceback);
	return true;
}

bool Py3kException(PyObject* obj) {
	if (obj == nullptr) {
		return Py3kException();
	} else {
		return false;
	}
}

void Py3kKeyEvent(int code, bool down, bool alt, bool ctrl, bool shift) {
	if (Py_IsInitialized() && pKeyEvent != nullptr) {
		PyObject* pArgs;
		PyObject* pKwargs;
		PyObject* pResult;

		// Create arguments
		pArgs = Py_BuildValue("iO",
			code, // key code
			down ? Py_True : Py_False // down
		);

		// Create keyword arguments
		pKwargs = Py_BuildValue("{s:O,s:O,s:O}",
			"alt", alt ? Py_True : Py_False,
			"ctrl", ctrl ? Py_True : Py_False,
			"shift", shift ? Py_True : Py_False
		);

		// Pass key event
		if (PyCallable_Check(pKeyEvent)) {
			pResult = PyObject_CallObject(pKeyEvent, NULL);
			if (!Py3kException(pResult)) {
				Py_DECREF(pResult);
			}
		} else {
			log_error("Key event function is not callable");
		}

		// Clean up
		Py_DECREF(pArgs);
		Py_DECREF(pKwargs);
	}
}

void Py3kTick() {
	if (Py_IsInitialized() && pTick != nullptr) {
		PyObject* pResult;

		// Acquire GIL
		PyEval_RestoreThread(pThreadState);

		// Call tick function
		if (PyCallable_Check(pTick)) {
			pResult = PyObject_CallObject(pTick, NULL);
			if (!Py3kException(pResult)) {
				Py_DECREF(pResult);
			}
		} else {
			log_error("Tick function is not callable");
		}

		// Release GIL
		pThreadState = PyEval_SaveThread();
	}
}

void Py3kInitialize() {
	log_debug("Py3kInitialize called");

	if (!Py_IsInitialized()) {
		PyObject* pModule;
		PyObject* pInit;
		PyObject* pDict;
		PyObject* pResult;
		PyObject* pOsModule;
		PyObject* pPathModule;
		PyObject* pCWD;
		PyObject* pAbsPathCWD;
		PyObject* pSysPath;
		PyObject* pStrPythonPath;
		PyObject* pJoinedPath;

		// Add module
		log_debug("Creating module _gta_native");
		if (PyImport_AppendInittab("_gta_native", &PyInit__gta_native) == -1) {
			log_error("Could not extend built-in modules table");
			return;
		}

		// Get version (borrowed)
		log_debug((std::string("Python ") + std::string(Py_GetVersion())).c_str());

		// Get path (borrowed)
		const wchar_t* path = Py_GetPath();
		if (path == nullptr) {
			log_error("Could not retrieve path");
			return;
		}
		char* cPath = wchar_to_string(path);
		log_debug((std::string("Path: ") + std::string(cPath)).c_str());
		delete cPath;

		// Initialise interpreter
		log_debug("Initialising");
		Py_InitializeEx(0);
		log_debug("Initialised");

		// Initialise and acquire GIL
		log_debug("Initialising and acquiring GIL");
		PyEval_InitThreads();

		// Get required modules (os, os.path)
		pOsModule = PyImport_ImportModule("os");
		if (Py3kException(pOsModule)) { Py_Finalize(); return; }
		pPathModule = PyImport_ImportModule("os.path");
		if (Py3kException(pPathModule)) { Py_DECREF(pOsModule); Py_Finalize(); return; }

		// Get current working directory [os.path.abspath(os.getcwd())]
		pCWD = PyObject_CallMethod(pOsModule, "getcwd", nullptr);
		if (Py3kException(pCWD)) { Py_DECREF(pOsModule); Py_DECREF(pPathModule); Py_Finalize(); return; }
		pAbsPathCWD = PyObject_CallMethod(pPathModule, "abspath", "O", pCWD);
		if (Py3kException(pAbsPathCWD)) { Py_DECREF(pOsModule); Py_DECREF(pPathModule); Py_DECREF(pCWD); Py_Finalize(); return; }
		Py_DECREF(pCWD); Py_DECREF(pOsModule);
		// Get sys path (borrowed) [sys.path]
		pSysPath = PySys_GetObject("path");
		if (Py3kException(pAbsPathCWD)) { Py_DECREF(pPathModule); Py_DECREF(pAbsPathCWD); Py_Finalize(); return; }
		// Check if working directory is in sys.path
		int contains = PySequence_Contains(pSysPath, pAbsPathCWD);
		if (contains == -1 || Py3kException()) { Py_DECREF(pPathModule); Py_DECREF(pAbsPathCWD); Py_Finalize(); return; }
		if (contains == 1) {
			// Remove from sys path
			pResult = PyObject_CallMethod(pSysPath, "remove", "O", pAbsPathCWD);
			if (Py3kException(pResult)) { Py_DECREF(pPathModule); Py_DECREF(pAbsPathCWD); Py_Finalize(); return; }
			Py_DECREF(pResult);
		}

		// Append modified path
		pStrPythonPath = PyUnicode_FromString("python");
		if (Py3kException(pStrPythonPath)) { Py_DECREF(pPathModule); Py_DECREF(pAbsPathCWD); Py_Finalize(); return; }
		pJoinedPath = PyObject_CallMethod(pPathModule, "join", "OO", pAbsPathCWD, pStrPythonPath);
		if (Py3kException(pJoinedPath)) { Py_DECREF(pPathModule); Py_DECREF(pAbsPathCWD); Py_DECREF(pStrPythonPath); Py_Finalize(); return; }
		Py_DECREF(pPathModule); Py_DECREF(pAbsPathCWD); Py_DECREF(pStrPythonPath);
		pResult = PyObject_CallMethod(pSysPath, "append", "O", pJoinedPath);
		if (Py3kException(pResult)) { Py_DECREF(pJoinedPath); Py_Finalize(); return; }
		Py_DECREF(pJoinedPath);
		Py_DECREF(pResult);

		// Reference module object
		log_debug("Importing module: gta");
		pModule = PyImport_ImportModule("gta");
		if (Py3kException(pModule)) { Py_Finalize(); return; }
		// Get dictionary of module (borrowed)
		pDict = PyModule_GetDict(pModule);
		Py_DECREF(pModule);
		if (Py3kException(pDict)) { Py_Finalize(); return; }
		// Get necessary functions (borrowed)
		log_debug("Referencing functions");
		pInit = PyDict_GetItemString(pDict, "_init");
		if (pInit == nullptr) { log_error("'gta._init' does not exist"); Py_Finalize(); return; }
		pExit = PyDict_GetItemString(pDict, "_exit");
		if (pExit == nullptr) { log_error("'gta._exit' does not exist"); Py_Finalize(); return; }
		pTick = PyDict_GetItemString(pDict, "_tick");
		if (pTick == nullptr) { log_error("'gta._tick' does not exist"); Py_Finalize(); return; }
		pKeyEvent = PyDict_GetItemString(pDict, "_key_event");
		if (pKeyEvent == nullptr) { log_error("'gta._key_event' does not exist"); Py_Finalize(); return; }

		// Call init function
		if (PyCallable_Check(pInit)) {
			log_debug("Calling gta._init()");
			pResult = PyObject_CallObject(pInit, NULL);
			if (Py3kException(pResult)) { Py_Finalize(); return; }
			Py_DECREF(pResult);
			log_debug("Returned from gta._init()");
		} else {
			log_error("Init function is not callable");
			Py_Finalize();
			return;
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
		PyObject* pResult;

		log_debug("Finalising");

		// Acquire GIL
		log_debug("Acquiring GIL");
		PyEval_RestoreThread(pThreadState);

		// Call exit function
		if (PyCallable_Check(pExit)) {
			log_debug("Calling gta._exit()");
			pResult = PyObject_CallObject(pExit, NULL);
			if (!Py3kException(pResult)) {
				log_debug("Returned from gta._exit()");
				Py_DECREF(pResult);
			}
		} else {
			log_error("Exit function is not callable");
		}

		// Finalise interpreter
		log_debug("Finalising");
		Py_Finalize();
		log_debug("Finalised");

		// Reset vars
		pExit = nullptr;
		pTick = nullptr;
		pKeyEvent = nullptr;
		pThreadState = nullptr;
	}
}

void Py3kReinitialize() {
	Py3kFinalize();
	Py3kInitialize();
}

void OnKeyboardMessage(DWORD key, WORD repeats, BYTE scanCode, BOOL isExtended, BOOL isWithAlt, BOOL wasDownBefore, BOOL isUpNow) {
	int code = static_cast<int>(key);
	bool down = isUpNow == FALSE;
	bool alt = isWithAlt == TRUE;
	bool ctrl = (GetAsyncKeyState(VK_CONTROL) & 0x8000) != 0;
	bool shift = (GetAsyncKeyState(VK_SHIFT) & 0x8000) != 0;

	// Catch built-in key events
	if (ctrl && !down) {
		if (key == VK_DELETE) {
			// Stop on Ctrl + Del
			action = STOP;
			return;
		} else if (key == VK_F12) {
			// Reload on Ctrl + F12
			action = RESTART;
			return;
		}
	}
	
	// Propagate key event
	Py3kKeyEvent(code, down, alt, ctrl, shift);
}

void Py3kWrapperStart() {
	log_debug("Py3kWrapper called");
	log_debug((std::string("Version: ") + std::string(PY3KWRAPPER_VERSION)).c_str());
	log_debug((std::string("Game Version: ") + std::string(game_version_name(getGameVersion()))).c_str());

	// (Re)Initialise
	Py3kReinitialize();

	// Main loop
	while (true) {
		switch (action) {
			case STOP:
				// Stop
				log_debug("Enforcing stop");
				Py3kFinalize();
				action = NONE;
				break;
			case RESTART:
				// Restart
				log_debug("Reloading");
				Py3kReinitialize();
				action = NONE;
				break;
			default:
				// Tick
				Py3kTick();
		}

		// Yield
		scriptWait(0);
	}
}

void Py3kWrapperStop() {
	// Finalise
	Py3kFinalize();
}


