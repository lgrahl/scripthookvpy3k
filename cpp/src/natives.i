%module gta_native
%{
#include "natives_wrap.h"
%}

%include <windows.i>
%include "../../sdk/inc/natives.h"
%include "../../sdk/inc/enums.h"
%include "../../sdk/inc/types.h"