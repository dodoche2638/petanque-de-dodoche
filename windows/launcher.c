typedef unsigned short W;
typedef __INTPTR_TYPE__ N;
typedef unsigned int D;
#define LIT(s) ((const W*)u##s)
#define API(type,name,...) extern type (__attribute__((ms_abi)) *ptr##name)(__VA_ARGS__)
API(N,CreateFileW,const W*,D,D,void*,D,D,N);
API(int,WriteFile,N,const void*,D,D*,void*);
API(int,CloseHandle,N);
API(D,GetTempFileNameW,const W*,const W*,D,W*);
API(int,DeleteFileW,const W*);
API(int,MoveFileExW,const W*,const W*,D);
API(int,CreateDirectoryW,const W*,void*);
API(D,GetEnvironmentVariableW,const W*,W*,D);
API(D,GetFileAttributesW,const W*);
API(void,ExitProcess,D);
API(W*,lstrcpyW,W*,const W*);
API(W*,lstrcatW,W*,const W*);
API(N,ShellExecuteW,N,const W*,const W*,const W*,const W*,int);
API(int,UrlCreateFromPathW,const W*,W*,D*,D);
API(int,MessageBoxW,N,const W*,const W*,D);
extern const char page[],page_end[];
static W dir[1024],path[1024],tmp[1024],edge[1024],url[4096],arg[4200];
static int run(void){
 D len=ptrGetEnvironmentVariableW(LIT("LOCALAPPDATA"),dir,1024);
 if(!len||len>210)return 0;
 ptrlstrcatW(dir,LIT("\\PetanqueDeDodoche"));
 ptrCreateDirectoryW(dir,0);
 ptrlstrcpyW(path,dir);ptrlstrcatW(path,LIT("\\Dodoche.html"));
 if(!ptrGetTempFileNameW(dir,LIT("pdd"),0,tmp))return 0;
 N h=ptrCreateFileW(tmp,0x40000000,0,0,2,0x80,0);
 D size=(D)(page_end-page),written=0;
 if(h==-1){ptrDeleteFileW(tmp);return 0;}
 int ok=ptrWriteFile(h,page,size,&written,0);
 ptrCloseHandle(h);
 if(!ok||written!=size||!ptrMoveFileExW(tmp,path,9)){ptrDeleteFileW(tmp);return 0;}
 D cap=4096;
 if(ptrUrlCreateFromPathW(path,url,&cap,0)>=0){
  ptrlstrcpyW(arg,LIT("--app=\""));ptrlstrcatW(arg,url);ptrlstrcatW(arg,LIT("\""));
  const W* roots[]={LIT("ProgramFiles(x86)"),LIT("ProgramFiles"),LIT("LOCALAPPDATA")};
  for(int i=0;i<3;i++){
   D n=ptrGetEnvironmentVariableW(roots[i],edge,1024);if(!n||n>900)continue;
   ptrlstrcatW(edge,LIT("\\Microsoft\\Edge\\Application\\msedge.exe"));
   if(ptrGetFileAttributesW(edge)!=0xffffffffu && ptrShellExecuteW(0,LIT("open"),edge,arg,0,1)>32)return 1;
  }
 }
 return ptrShellExecuteW(0,LIT("open"),path,0,0,1)>32;
}
void entry(void){
 if(!run())ptrMessageBoxW(0,LIT("Impossible de lancer l’application. Ouvrez Dodoche.html depuis le ZIP dans Microsoft Edge."),LIT("LA PETANQUE DE DODOCHE"),16);
 ptrExitProcess(0);
}
