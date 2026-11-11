from pathlib import Path
from subprocess import run
from zipfile import ZipFile, ZIP_DEFLATED
import os
import struct
import sys

root = Path(__file__).resolve().parents[1]
os.chdir(root)
version = int(Path('VERSION').read_text())
out = Path('dist')
out.mkdir(exist_ok=True)
run([sys.executable, 'scripts/android.py'], check=True)
def compile_windows(arguments):
    run(arguments, cwd='windows', check=True)
compile_windows(['gcc','-Os','-fno-ident','-fpie','-fno-omit-frame-pointer','-fno-stack-protector','-fno-asynchronous-unwind-tables','-mabi=ms','-c','launcher.c','-o','../dist/launcher.o'])
compile_windows(['as','--64','imports-fixed.s','-o','../dist/imports.o'])
exe = out/'Petanque-de-Dodoche.exe'
run(['ld','-mi386pep','--section-start','.winimp=0x403000','--section-start','.rdata=0x404000','--image-base','0x400000','--subsystem','windows','--entry','entry','-o',exe,out/'launcher.o',out/'imports.o'],check=True)
data = bytearray(exe.read_bytes())
optional = struct.unpack_from('<I',data,60)[0]+24
sections = optional+struct.unpack_from('<H',data,optional-4)[0]
addresses = [struct.unpack_from('<I',data,i+12)[0] for i in range(sections,sections+40*struct.unpack_from('<H',data,optional-18)[0],40) if data[i:i+7]==b'.winimp']
if addresses != [0x3000]:
    raise ValueError('Disposition des imports Windows inattendue')
struct.pack_into('<II',data,optional+120,addresses[0],100)
struct.pack_into('<I',data,optional+64,0)
exe.write_bytes(data)
for name, files in [(f'Dodoche-v{version}',[out/f'Dodoche-v{version}.apk']), (f'Petanque-de-Dodoche-Windows-v{version}',[exe,Path('windows/Dodoche.html')])]:
    with ZipFile(out/(name+'.zip'),'w',ZIP_DEFLATED) as archive:
        for path in files+[Path('Historique-des-versions.txt')]:
            archive.write(path,path.name)
        if exe in files:
            archive.write('android/ZXing-NOTICES.txt','Licences/ZXing.txt')
