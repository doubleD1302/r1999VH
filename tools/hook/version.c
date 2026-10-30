#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// ============================================================================
// 1. SYSTEM VERSION.DLL PROXY (Không dùng .def forwarder để tránh lỗi Error 193)
// ============================================================================
static HMODULE hOriginalVersion = NULL;

static void EnsureOriginalLoaded() {
    if (hOriginalVersion) return;
    wchar_t sysDir[MAX_PATH];
    GetSystemDirectoryW(sysDir, MAX_PATH);
    wcscat(sysDir, L"\\version.dll");
    hOriginalVersion = LoadLibraryW(sysDir);
}

static FARPROC GetOrigProc(const char* name) {
    EnsureOriginalLoaded();
    return hOriginalVersion ? GetProcAddress(hOriginalVersion, name) : NULL;
}

__declspec(dllexport) BOOL WINAPI GetFileVersionInfoA(LPCSTR lptstrFilename, DWORD dwHandle, DWORD dwLen, LPVOID lpData) {
    typedef BOOL (WINAPI *pfn)(LPCSTR, DWORD, DWORD, LPVOID);
    pfn p = (pfn)GetOrigProc("GetFileVersionInfoA");
    return p ? p(lptstrFilename, dwHandle, dwLen, lpData) : FALSE;
}

__declspec(dllexport) BOOL WINAPI GetFileVersionInfoW(LPCWSTR lptstrFilename, DWORD dwHandle, DWORD dwLen, LPVOID lpData) {
    typedef BOOL (WINAPI *pfn)(LPCWSTR, DWORD, DWORD, LPVOID);
    pfn p = (pfn)GetOrigProc("GetFileVersionInfoW");
    return p ? p(lptstrFilename, dwHandle, dwLen, lpData) : FALSE;
}

__declspec(dllexport) DWORD WINAPI GetFileVersionInfoSizeA(LPCSTR lptstrFilename, LPDWORD lpdwHandle) {
    typedef DWORD (WINAPI *pfn)(LPCSTR, LPDWORD);
    pfn p = (pfn)GetOrigProc("GetFileVersionInfoSizeA");
    return p ? p(lptstrFilename, lpdwHandle) : 0;
}

__declspec(dllexport) DWORD WINAPI GetFileVersionInfoSizeW(LPCWSTR lptstrFilename, LPDWORD lpdwHandle) {
    typedef DWORD (WINAPI *pfn)(LPCWSTR, LPDWORD);
    pfn p = (pfn)GetOrigProc("GetFileVersionInfoSizeW");
    return p ? p(lptstrFilename, lpdwHandle) : 0;
}

__declspec(dllexport) BOOL WINAPI VerQueryValueA(LPCVOID pBlock, LPCSTR lpSubBlock, LPVOID *lplpBuffer, PUINT puLen) {
    typedef BOOL (WINAPI *pfn)(LPCVOID, LPCSTR, LPVOID*, PUINT);
    pfn p = (pfn)GetOrigProc("VerQueryValueA");
    return p ? p(lplpBuffer ? pBlock : NULL, lpSubBlock, lplpBuffer, puLen) : FALSE;
}

__declspec(dllexport) BOOL WINAPI VerQueryValueW(LPCVOID pBlock, LPCWSTR lpSubBlock, LPVOID *lplpBuffer, PUINT puLen) {
    typedef BOOL (WINAPI *pfn)(LPCVOID, LPCWSTR, LPVOID*, PUINT);
    pfn p = (pfn)GetOrigProc("VerQueryValueW");
    return p ? p(lplpBuffer ? pBlock : NULL, lpSubBlock, lplpBuffer, puLen) : FALSE;
}

__declspec(dllexport) DWORD WINAPI GetFileVersionInfoSizeExA(DWORD dwFlags, LPCSTR lpwstrFilename, LPDWORD lpdwHandle) {
    typedef DWORD (WINAPI *pfn)(DWORD, LPCSTR, LPDWORD);
    pfn p = (pfn)GetOrigProc("GetFileVersionInfoSizeExA");
    return p ? p(dwFlags, lpwstrFilename, lpdwHandle) : 0;
}

__declspec(dllexport) DWORD WINAPI GetFileVersionInfoSizeExW(DWORD dwFlags, LPCWSTR lpwstrFilename, LPDWORD lpdwHandle) {
    typedef DWORD (WINAPI *pfn)(DWORD, LPCWSTR, LPDWORD);
    pfn p = (pfn)GetOrigProc("GetFileVersionInfoSizeExW");
    return p ? p(dwFlags, lpwstrFilename, lpdwHandle) : 0;
}

__declspec(dllexport) BOOL WINAPI GetFileVersionInfoExA(DWORD dwFlags, LPCSTR lpwstrFilename, DWORD dwHandle, DWORD dwLen, LPVOID lpData) {
    typedef BOOL (WINAPI *pfn)(DWORD, LPCSTR, DWORD, DWORD, LPVOID);
    pfn p = (pfn)GetOrigProc("GetFileVersionInfoExA");
    return p ? p(dwFlags, lpwstrFilename, dwHandle, dwLen, lpData) : FALSE;
}

__declspec(dllexport) BOOL WINAPI GetFileVersionInfoExW(DWORD dwFlags, LPCWSTR lpwstrFilename, DWORD dwHandle, DWORD dwLen, LPVOID lpData) {
    typedef BOOL (WINAPI *pfn)(DWORD, LPCWSTR, DWORD, DWORD, LPVOID);
    pfn p = (pfn)GetOrigProc("GetFileVersionInfoExW");
    return p ? p(dwFlags, lpwstrFilename, dwHandle, dwLen, lpData) : FALSE;
}

__declspec(dllexport) DWORD WINAPI VerLanguageNameA(DWORD wLang, LPSTR szLang, DWORD nSize) {
    typedef DWORD (WINAPI *pfn)(DWORD, LPSTR, DWORD);
    pfn p = (pfn)GetOrigProc("VerLanguageNameA");
    return p ? p(wLang, szLang, nSize) : 0;
}

__declspec(dllexport) DWORD WINAPI VerLanguageNameW(DWORD wLang, LPWSTR szLang, DWORD nSize) {
    typedef DWORD (WINAPI *pfn)(DWORD, LPWSTR, DWORD);
    pfn p = (pfn)GetOrigProc("VerLanguageNameW");
    return p ? p(wLang, szLang, nSize) : 0;
}

__declspec(dllexport) DWORD WINAPI VerFindFileA(DWORD uFlags, LPSTR szFileName, LPSTR szWinDir, LPSTR szAppDir, LPSTR szCurDir, PUINT lpuCurDirLen, LPSTR szDestDir, PUINT lpuDestDirLen) {
    typedef DWORD (WINAPI *pfn)(DWORD, LPSTR, LPSTR, LPSTR, LPSTR, PUINT, LPSTR, PUINT);
    pfn p = (pfn)GetOrigProc("VerFindFileA");
    return p ? p(uFlags, szFileName, szWinDir, szAppDir, szCurDir, lpuCurDirLen, szDestDir, lpuDestDirLen) : 0;
}

__declspec(dllexport) DWORD WINAPI VerFindFileW(DWORD uFlags, LPWSTR szFileName, LPWSTR szWinDir, LPWSTR szAppDir, LPWSTR szCurDir, PUINT lpuCurDirLen, LPWSTR szDestDir, PUINT lpuDestDirLen) {
    typedef DWORD (WINAPI *pfn)(DWORD, LPWSTR, LPWSTR, LPWSTR, LPWSTR, PUINT, LPWSTR, PUINT);
    pfn p = (pfn)GetOrigProc("VerFindFileW");
    return p ? p(uFlags, szFileName, szWinDir, szAppDir, szCurDir, lpuCurDirLen, szDestDir, lpuDestDirLen) : 0;
}

__declspec(dllexport) DWORD WINAPI VerInstallFileA(DWORD uFlags, LPSTR szSrcFileName, LPSTR szDestFileName, LPSTR szSrcDir, LPSTR szDestDir, LPSTR szCurDir, LPSTR szTmpFile, PUINT lpuTmpFileLen) {
    typedef DWORD (WINAPI *pfn)(DWORD, LPSTR, LPSTR, LPSTR, LPSTR, LPSTR, LPSTR, PUINT);
    pfn p = (pfn)GetOrigProc("VerInstallFileA");
    return p ? p(uFlags, szSrcFileName, szDestFileName, szSrcDir, szDestDir, szCurDir, szTmpFile, lpuTmpFileLen) : 0;
}

__declspec(dllexport) DWORD WINAPI VerInstallFileW(DWORD uFlags, LPWSTR szSrcFileName, LPWSTR szDestFileName, LPWSTR szSrcDir, LPWSTR szDestDir, LPWSTR szCurDir, LPWSTR szTmpFile, PUINT lpuTmpFileLen) {
    typedef DWORD (WINAPI *pfn)(DWORD, LPWSTR, LPWSTR, LPWSTR, LPWSTR, LPWSTR, LPWSTR, PUINT);
    pfn p = (pfn)GetOrigProc("VerInstallFileW");
    return p ? p(uFlags, szSrcFileName, szDestFileName, szSrcDir, szDestDir, szCurDir, szTmpFile, lpuTmpFileLen) : 0;
}

__declspec(dllexport) int WINAPI GetFileVersionInfoByHandle(int h, int a, int b, int c) {
    typedef int (WINAPI *pfn)(int, int, int, int);
    pfn p = (pfn)GetOrigProc("GetFileVersionInfoByHandle");
    return p ? p(h, a, b, c) : 0;
}

// ============================================================================
// 2. RUNTIME LUA HOOK FOR VIETNAMESE LOCALIZATION
// ============================================================================
typedef int (*pfn_luaL_loadbuffer)(void* L, const char* buff, size_t sz, const char* name);
typedef int (*pfn_luaL_loadstring)(void* L, const char* s);
typedef int (*pfn_lua_pcall)(void* L, int nargs, int nresults, int errfunc);
typedef void (*pfn_lua_pushlstring)(void* L, const char* s, size_t len);
typedef void (*pfn_lua_setfield)(void* L, int idx, const char* k);
typedef void (*pfn_lua_settop)(void* L, int idx);

static pfn_luaL_loadbuffer orig_luaL_loadbuffer = NULL;
static pfn_luaL_loadstring fp_luaL_loadstring = NULL;
static pfn_lua_pcall fp_lua_pcall = NULL;
static pfn_lua_pushlstring fp_lua_pushlstring = NULL;
static pfn_lua_setfield fp_lua_setfield = NULL;
static pfn_lua_settop fp_lua_settop = NULL;

static BYTE g_trampoline[32];
static char* g_vi_json_str = NULL;
static size_t g_vi_json_len = 0;
static volatile LONG g_hook_installed = 0;
static FILE* g_log_fp = NULL;

static void LogMsg(const char* fmt, ...) {
    if (!g_log_fp) {
        g_log_fp = fopen("viethoa.log", "a");
    }
    if (g_log_fp) {
        SYSTEMTIME st;
        GetLocalTime(&st);
        fprintf(g_log_fp, "[%02d:%02d:%02d] ", st.wHour, st.wMinute, st.wSecond);
        va_list args;
        va_start(args, fmt);
        vfprintf(g_log_fp, fmt, args);
        va_end(args);
        fprintf(g_log_fp, "\n");
        fflush(g_log_fp);
    }
}

static void LoadViJson() {
    FILE* fp = fopen("vi_strings.json", "rb");
    if (!fp) {
        LogMsg("[WARN] Khong the mo vi_strings.json!");
        return;
    }
    fseek(fp, 0, SEEK_END);
    long sz = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    if (sz <= 0) {
        fclose(fp);
        return;
    }
    g_vi_json_str = (char*)malloc(sz + 1);
    if (g_vi_json_str) {
        fread(g_vi_json_str, 1, sz, fp);
        g_vi_json_str[sz] = '\0';
        g_vi_json_len = (size_t)sz;
        LogMsg("[OK] Da nap vi_strings.json (%ld bytes)", sz);
    }
    fclose(fp);
}

static void TryInstallLuaHook(void* L) {
    if (InterlockedCompareExchange(&g_hook_installed, 1, 0) != 0) {
        return;
    }

    if (!fp_lua_pushlstring || !fp_lua_setfield || !fp_luaL_loadstring || !fp_lua_pcall) {
        g_hook_installed = 0;
        return;
    }

    if (g_vi_json_str && g_vi_json_len > 0) {
        fp_lua_pushlstring(L, g_vi_json_str, g_vi_json_len);
        fp_lua_setfield(L, -10002, "__R1999_VI_JSON__");
    }

    const char* hook_script =
        "local ok, cjson = pcall(require, 'cjson')\n"
        "if ok and cjson and cjson.decode then\n"
        "    local orig_decode = cjson.decode\n"
        "    local vi_map = nil\n"
        "    if _G.__R1999_VI_JSON__ then\n"
        "        local ok_p, parsed = pcall(orig_decode, _G.__R1999_VI_JSON__)\n"
        "        if ok_p and type(parsed) == 'table' then\n"
        "            vi_map = parsed\n"
        "        end\n"
        "        _G.__R1999_VI_JSON__ = nil\n"
        "    end\n"
        "    if vi_map then\n"
        "        cjson.decode = function(str)\n"
        "            local t = orig_decode(str)\n"
        "            if type(t) == 'table' and t[1] == 'language_en' and type(t[2]) == 'table' then\n"
        "                local items = t[2]\n"
        "                for i = 1, #items do\n"
        "                    local it = items[i]\n"
        "                    local val = vi_map[it[1]]\n"
        "                    if val then\n"
        "                        it[2] = val\n"
        "                    end\n"
        "                end\n"
        "            end\n"
        "            return t\n"
        "        end\n"
        "    end\n"
        "    _G.__R1999_HOOK_SUCCESS = true\n"
        "end\n";

    if (fp_luaL_loadstring(L, hook_script) == 0) {
        if (fp_lua_pcall(L, 0, 0, 0) == 0) {
            LogMsg("[SUCCESS] Da nap thanh cong hook cjson.decode vao Lua state!");
        } else {
            LogMsg("[WARN] pcall lua_hook that bai!");
            g_hook_installed = 0;
        }
    } else {
        LogMsg("[WARN] loadstring lua_hook that bai!");
        g_hook_installed = 0;
    }
}

static int Hooked_luaL_loadbuffer(void* L, const char* buff, size_t sz, const char* name) {
    int res = orig_luaL_loadbuffer(L, buff, sz, name);
    if (res == 0 && !g_hook_installed) {
        TryInstallLuaHook(L);
    }
    return res;
}

static DWORD WINAPI InitHookThread(LPVOID lpParam) {
    EnsureOriginalLoaded();
    LogMsg("=== Reverse: 1999 Viet Hoa Runtime Hook Khoi Dong ===");
    LoadViJson();

    HMODULE hTolua = NULL;
    int tries = 0;
    while (!hTolua && tries < 300) {
        hTolua = GetModuleHandleA("tolua.dll");
        if (!hTolua) {
            Sleep(100);
            tries++;
        }
    }

    if (!hTolua) {
        LogMsg("[ERROR] Khong tim thay tolua.dll sau 30 giay!");
        return 0;
    }

    LogMsg("[OK] Tim thay tolua.dll tai dia chi: %p", hTolua);

    pfn_luaL_loadbuffer target_func = (pfn_luaL_loadbuffer)GetProcAddress(hTolua, "luaL_loadbuffer");
    fp_luaL_loadstring = (pfn_luaL_loadstring)GetProcAddress(hTolua, "luaL_loadstring");
    fp_lua_pcall = (pfn_lua_pcall)GetProcAddress(hTolua, "lua_pcall");
    fp_lua_pushlstring = (pfn_lua_pushlstring)GetProcAddress(hTolua, "lua_pushlstring");
    fp_lua_setfield = (pfn_lua_setfield)GetProcAddress(hTolua, "lua_setfield");
    fp_lua_settop = (pfn_lua_settop)GetProcAddress(hTolua, "lua_settop");

    if (!target_func || !fp_luaL_loadstring || !fp_lua_pcall) {
        LogMsg("[ERROR] Khong the resolve cac ham Lua trong tolua.dll!");
        return 0;
    }

    BYTE* target = (BYTE*)target_func;
    DWORD oldProt;
    VirtualProtect(g_trampoline, sizeof(g_trampoline), PAGE_EXECUTE_READWRITE, &oldProt);

    memcpy(g_trampoline, target, 14);
    g_trampoline[14] = 0xFF;
    g_trampoline[15] = 0x25;
    *(DWORD*)(&g_trampoline[16]) = 0;
    *(ULONG_PTR*)(&g_trampoline[20]) = (ULONG_PTR)(target + 14);

    orig_luaL_loadbuffer = (pfn_luaL_loadbuffer)g_trampoline;

    VirtualProtect(target, 14, PAGE_EXECUTE_READWRITE, &oldProt);
    target[0] = 0xFF;
    target[1] = 0x25;
    *(DWORD*)(&target[2]) = 0;
    *(ULONG_PTR*)(&target[6]) = (ULONG_PTR)Hooked_luaL_loadbuffer;
    VirtualProtect(target, 14, oldProt, &oldProt);

    FlushInstructionCache(GetCurrentProcess(), target, 14);
    LogMsg("[OK] Da cai dat thanh cong Inline Hook vao luaL_loadbuffer!");

    return 0;
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved) {
    if (fdwReason == DLL_PROCESS_ATTACH) {
        DisableThreadLibraryCalls(hinstDLL);
        CreateThread(NULL, 0, InitHookThread, NULL, 0, NULL);
    }
    return TRUE;
}
