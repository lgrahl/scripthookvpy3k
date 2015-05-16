#include "wrapper.h"
#include "keyboard.h"

BOOL APIENTRY DllMain(HMODULE hInstance, DWORD reason, LPVOID lpReserved)
{
	switch (reason) {
		case DLL_PROCESS_ATTACH:
			log_debug("Attaching");
			scriptRegister(hInstance, &Py3kWrapper);
			keyboardHandlerRegister(&OnKeyboardMessage);
			break;

		case DLL_PROCESS_DETACH:
			log_debug("Detaching");
			Py3kFinalize();
			scriptUnregister(&Py3kWrapper);
			keyboardHandlerUnregister(&OnKeyboardMessage);
			break;
	}		

	return TRUE;
}