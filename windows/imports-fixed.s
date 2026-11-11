.section .winimp,"aw"
import_base:
.long lookup0-import_base+0x3000
.long 0,0
.long dll0-import_base+0x3000,iat0-import_base+0x3000
.long lookup1-import_base+0x3000
.long 0,0
.long dll1-import_base+0x3000,iat1-import_base+0x3000
.long lookup2-import_base+0x3000
.long 0,0
.long dll2-import_base+0x3000,iat2-import_base+0x3000
.long lookup3-import_base+0x3000
.long 0,0
.long dll3-import_base+0x3000,iat3-import_base+0x3000
.zero 20
.balign 8
lookup0:
.long hintCreateFileW-import_base+0x3000
.long 0
.long hintWriteFile-import_base+0x3000
.long 0
.long hintCloseHandle-import_base+0x3000
.long 0
.long hintGetTempFileNameW-import_base+0x3000
.long 0
.long hintDeleteFileW-import_base+0x3000
.long 0
.long hintMoveFileExW-import_base+0x3000
.long 0
.long hintCreateDirectoryW-import_base+0x3000
.long 0
.long hintGetEnvironmentVariableW-import_base+0x3000
.long 0
.long hintGetFileAttributesW-import_base+0x3000
.long 0
.long hintExitProcess-import_base+0x3000
.long 0
.long hintlstrcpyW-import_base+0x3000
.long 0
.long hintlstrcatW-import_base+0x3000
.long 0
.quad 0
iat0:
.global ptrCreateFileW
ptrCreateFileW:
.long hintCreateFileW-import_base+0x3000
.long 0
.global ptrWriteFile
ptrWriteFile:
.long hintWriteFile-import_base+0x3000
.long 0
.global ptrCloseHandle
ptrCloseHandle:
.long hintCloseHandle-import_base+0x3000
.long 0
.global ptrGetTempFileNameW
ptrGetTempFileNameW:
.long hintGetTempFileNameW-import_base+0x3000
.long 0
.global ptrDeleteFileW
ptrDeleteFileW:
.long hintDeleteFileW-import_base+0x3000
.long 0
.global ptrMoveFileExW
ptrMoveFileExW:
.long hintMoveFileExW-import_base+0x3000
.long 0
.global ptrCreateDirectoryW
ptrCreateDirectoryW:
.long hintCreateDirectoryW-import_base+0x3000
.long 0
.global ptrGetEnvironmentVariableW
ptrGetEnvironmentVariableW:
.long hintGetEnvironmentVariableW-import_base+0x3000
.long 0
.global ptrGetFileAttributesW
ptrGetFileAttributesW:
.long hintGetFileAttributesW-import_base+0x3000
.long 0
.global ptrExitProcess
ptrExitProcess:
.long hintExitProcess-import_base+0x3000
.long 0
.global ptrlstrcpyW
ptrlstrcpyW:
.long hintlstrcpyW-import_base+0x3000
.long 0
.global ptrlstrcatW
ptrlstrcatW:
.long hintlstrcatW-import_base+0x3000
.long 0
.quad 0
dll0:
.asciz "KERNEL32.dll"
.balign 2
hintCreateFileW:
.short 0
.asciz "CreateFileW"
.balign 2
hintWriteFile:
.short 0
.asciz "WriteFile"
.balign 2
hintCloseHandle:
.short 0
.asciz "CloseHandle"
.balign 2
hintGetTempFileNameW:
.short 0
.asciz "GetTempFileNameW"
.balign 2
hintDeleteFileW:
.short 0
.asciz "DeleteFileW"
.balign 2
hintMoveFileExW:
.short 0
.asciz "MoveFileExW"
.balign 2
hintCreateDirectoryW:
.short 0
.asciz "CreateDirectoryW"
.balign 2
hintGetEnvironmentVariableW:
.short 0
.asciz "GetEnvironmentVariableW"
.balign 2
hintGetFileAttributesW:
.short 0
.asciz "GetFileAttributesW"
.balign 2
hintExitProcess:
.short 0
.asciz "ExitProcess"
.balign 2
hintlstrcpyW:
.short 0
.asciz "lstrcpyW"
.balign 2
hintlstrcatW:
.short 0
.asciz "lstrcatW"
.balign 8
lookup1:
.long hintShellExecuteW-import_base+0x3000
.long 0
.quad 0
iat1:
.global ptrShellExecuteW
ptrShellExecuteW:
.long hintShellExecuteW-import_base+0x3000
.long 0
.quad 0
dll1:
.asciz "SHELL32.dll"
.balign 2
hintShellExecuteW:
.short 0
.asciz "ShellExecuteW"
.balign 8
lookup2:
.long hintUrlCreateFromPathW-import_base+0x3000
.long 0
.quad 0
iat2:
.global ptrUrlCreateFromPathW
ptrUrlCreateFromPathW:
.long hintUrlCreateFromPathW-import_base+0x3000
.long 0
.quad 0
dll2:
.asciz "SHLWAPI.dll"
.balign 2
hintUrlCreateFromPathW:
.short 0
.asciz "UrlCreateFromPathW"
.balign 8
lookup3:
.long hintMessageBoxW-import_base+0x3000
.long 0
.quad 0
iat3:
.global ptrMessageBoxW
ptrMessageBoxW:
.long hintMessageBoxW-import_base+0x3000
.long 0
.quad 0
dll3:
.asciz "USER32.dll"
.balign 2
hintMessageBoxW:
.short 0
.asciz "MessageBoxW"
.section .rdata,"a"
.global page,page_end
page:
.incbin "Dodoche.html"
page_end:
