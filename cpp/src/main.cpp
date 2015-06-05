#include "wrapper.h"

BOOL APIENTRY DllMain(HMODULE hInstance, DWORD reason, LPVOID lpReserved)
{
	switch (reason) {
		case DLL_PROCESS_ATTACH:
			log_debug("Attaching");
			scriptRegister(hInstance, &Py3kWrapperStart);
			keyboardHandlerRegister(&OnKeyboardMessage);
			break;

		case DLL_PROCESS_DETACH:
			log_debug("Detaching");
			Py3kWrapperStop();
			scriptUnregister(hInstance);
			keyboardHandlerUnregister(&OnKeyboardMessage);
			break;
	}		

	return TRUE;
}