from pathlib import Path
import os
version=int(Path("VERSION").read_text())
apk=Path(f"dist/Dodoche-v{version}.apk")
import struct as S, hashlib as H,zlib,zipfile,base64,datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs7
def P(*v):return S.pack('<'+'I'*len(v),*v)
def U(*v):return S.pack('<'+'H'*len(v),*v)
def leb(n):return bytes([n]) if n<128 else bytes([128+n%128])+leb(n//128)
A='Landroid/app/Activity;'; M='Lfr/famille/dodochepetanque/Main;'; W='Landroid/webkit/WebView;'; Q='Landroid/webkit/WebSettings;'; C='Landroid/webkit/WebChromeClient;'; B='Landroid/os/Bundle;'; T='Ljava/lang/String;';X='Landroid/content/Context;';V='Landroid/view/View;'
methods=[(A,'<init>','V',()),(M,'<init>','V',()),(A,'onCreate','V',(B,)),(M,'onCreate','V',(B,)),(W,'<init>','V',(X,)),(W,'getSettings',Q,()),(Q,'setJavaScriptEnabled','V',('Z',)),(Q,'setDomStorageEnabled','V',('Z',)),(C,'<init>','V',()),(W,'setWebChromeClient','V',(C,)),(W,'loadUrl','V',(T,)),(A,'setContentView','V',(V,))]
K='Lzz/LicenseChrome;';R='Landroid/webkit/PermissionRequest;';J='Landroid/webkit/JsResult;';Z='[Ljava/lang/String;';O='Ljava/lang/Object;';URI='Landroid/net/Uri;'
methods += [(K,'<init>','V',()),(K,'onPermissionRequest','V',(R,)),(R,'grant','V',(Z,)),(K,'onJsAlert','Z',(W,T,T,J)),(C,'onJsAlert','Z',(W,T,T,J)),(T,'equals','Z',(O,)),(W,'getContext',X,()),(A,'requestPermissions','V',(Z,'I')),(J,'confirm','V',()),(A,'checkSelfPermission','I',(T,)),(R,'getOrigin',URI,()),(URI,'getScheme',T,()),(R,'deny','V',())]
methods.append((Q,'setAllowUniversalAccessFromFileURLs','V',('Z',)))
types=set();strings={'file:///android_asset/index.html','dodoche-request-camera','android.permission.CAMERA','android.webkit.resource.VIDEO_CAPTURE','file'};protos=set()
def short(p):return ''.join('L' if t.startswith('[') else t[0] for t in (p[0],*p[1]))
for c,n,r,args in methods:types.update([c,r,*args]);strings.update([n,short((r,args))]);protos.add((r,args))
ss=sorted(strings|types);ty=sorted(types);pr=sorted(protos,key=lambda p:(ty.index(p[0]),tuple(map(ty.index,p[1]))));ms=sorted(methods,key=lambda m:(ty.index(m[0]),ss.index(m[1]),pr.index(m[2:])))
so=112;to=so+4*len(ss);po=to+4*len(ty);mo=po+12*len(pr);co=mo+8*len(ms);do=co+64;d=bytearray()
def off():return do+len(d)
def align():d.extend(bytes(-off()%4))
def put(x):o=off();d.extend(x);return o
si=[put(leb(len(x))+x.encode()+b'\0') for x in ss];align();argsmap={}
for _,ar in pr:
 if ar and ar not in argsmap:argsmap[ar]=put(P(len(ar))+U(*map(ty.index,ar)));align()
def inv(op,m,*regs):return [op+len(regs)*4096+(regs[4]*256 if len(regs)>4 else 0),ms.index(methods[m]),sum(r<<(4*i) for i,r in enumerate(regs[:4]))]
def code(reg,ins,outs,words):align();return put(U(reg,ins,outs,0)+P(0,len(words))+U(*words))
init=code(1,1,1,inv(0x70,0,0)+[14])
words=inv(0x6f,2,3,4)+[0x22,ty.index(W)]+inv(0x70,4,0,3)+inv(0x6e,5,0)+[0x010c,0x1212]+inv(0x6e,6,1,2)+inv(0x6e,7,1,2)+inv(0x6e,25,1,2)+[0x0122,ty.index(K)]+inv(0x70,12,1)+inv(0x6e,9,0,1)+[0x011a,ss.index('file:///android_asset/index.html')]+inv(0x6e,10,0,1)+inv(0x6e,11,3,0)+[14]
on=code(5,2,2,words)
ki=code(1,1,1,inv(0x70,8,0)+[14])
def string(reg,value):return [0x1a+(reg<<8),ss.index(value)]
def array(reg,tmp,value):
 return [0x1012+(tmp<<8),0x23+(reg<<8)+(tmp<<12),ty.index(Z)]+string(tmp,value)+[0x0212,0x4d+(tmp<<8),(2<<8)+reg]
w=inv(0x6e,22,4)+[0x000c]+inv(0x6e,23,0)+[0x000c]+string(1,'file')+inv(0x6e,17,1,0)+[0x000a]
w += [0x0039,6]+inv(0x6e,24,4)+[14]
perm=code(5,2,2,w+array(0,1,'android.webkit.resource.VIDEO_CAPTURE')+inv(0x6e,14,4,0)+[14])
# v3=this, v4=WebView, v5=url, v6=message, v7=result
w=string(0,'dodoche-request-camera')+inv(0x6e,17,0,6)+[0x000a,0x0039,7]+inv(0x6f,16,3,4,5,6,7)+[0x000a,0x000f]
w+=inv(0x6e,18,4)+[0x000c,0x001f,ty.index(A)]+string(1,'android.permission.CAMERA')+inv(0x6e,21,0,1)+[0x010a]
req=[0x1112,0x1123,ty.index(Z)]+string(2,'android.permission.CAMERA')+[0x0512,0x024d,0x0501,0x1212]+inv(0x6e,19,0,1,2)
w += [0x0138,len(req)+2]+req+inv(0x6e,20,7)+[0x1012,0x000f]
alertcode=code(8,5,5,w)
def classdata(direct,virtual):
 raw=bytes([0,0,len(direct),len(virtual)])
 for group in (direct,virtual):
  last=0
  for idx,flags,loc in sorted((ms.index(methods[i]),f,o) for i,f,o in group):
   raw+=leb(idx-last)+leb(flags)+leb(loc);last=idx
 return put(raw)
cd=classdata([(1,0x10001,init)],[(3,4,on)])
ck=classdata([(12,0x10001,ki)],[(13,1,perm),(15,1,alertcode)])
align();mp=off()
entries=[(0,1,0),(1,len(ss),so),(2,len(ty),to),(3,len(pr),po),(5,len(ms),mo),(6,2,co),(0x2002,len(ss),si[0]),(0x1001,len(argsmap),min(argsmap.values())),(0x2001,5,init),(0x2000,2,cd),(0x1000,1,mp)]
put(P(len(entries))+b''.join(U(t,0)+P(n,o) for t,n,o in entries))
dex=bytearray(b'dex\n035\0'+bytes(24)+P(off(),112,0x12345678,0,0,mp,len(ss),so,len(ty),to,len(pr),po,0,0,len(ms),mo,2,co,len(d),do)+P(*si)+P(*map(ss.index,ty))+b''.join(P(ss.index(short(p)),ty.index(p[0]),argsmap.get(p[1],0)) for p in pr)+b''.join(U(ty.index(c),pr.index((r,a)))+P(ss.index(n)) for c,n,r,a in ms)+P(ty.index(M),1,ty.index(A),0,0xffffffff,0,cd,0)+P(ty.index(K),1,ty.index(C),0,0xffffffff,0,ck,0)+d);dex[12:32]=H.sha1(dex[32:]).digest();dex[8:12]=P(zlib.adler32(dex[12:]))
# Binary Android manifest
attrs={'label':0x1010001,'icon':0x1010002,'name':0x1010003,'exported':0x1010010,'minSdkVersion':0x101020c,'targetSdkVersion':0x1010270,'versionCode':0x101021b,'versionName':0x101021c}
st=list(attrs);none=0xffffffff
def ix(s):
 if s not in st:st.append(s)
 return st.index(s)
uri=ix('http://schemas.android.com/apk/res/android');prefix=ix('android')
def chunk(t,h,data):return U(t,h)+P(len(data)+8)+data
def node(t,data):return chunk(t,16,P(1,none)+data)
xml=node(0x100,P(prefix,uri))
def tag(n,aa):
 global xml
 aa=sorted(aa,key=lambda a:attrs.get(a[0],0));data=b''
 for k,v in aa:
  t=1 if k=="icon" else 3 if isinstance(v,str) else 18 if isinstance(v,bool) else 16
  val=ix(v) if t==3 else int(v)
  data+=P(uri if k in attrs else none,ix(k),val if t==3 else none)+U(8)+bytes([0,t])+P(val)
 xml+=node(0x102,P(none,ix(n))+U(20,20,len(aa),0,0,0)+data)
def end(n):
 global xml
 xml+=node(0x103,P(none,ix(n)))
tag('manifest',[('package','fr.famille.dodocheconcours26'),('versionCode',version),('versionName',f'{version}.0')]);tag('uses-sdk',[('minSdkVersion',24),('targetSdkVersion',32)]);end('uses-sdk');tag('uses-permission',[('name','android.permission.CAMERA')]);end('uses-permission');tag('uses-permission',[('name','android.permission.INTERNET')]);end('uses-permission');tag('application',[('label',f'LA PETANQUE DE DODOCHE · v{version}'),('icon',0x7f010000)]);tag('activity',[('name','fr.famille.dodochepetanque.Main'),('exported',True)]);tag('intent-filter',[]);tag('action',[('name','android.intent.action.MAIN')]);end('action');tag('category',[('name','android.intent.category.LAUNCHER')]);end('category')
for n in ['intent-filter','activity','application','manifest']:end(n)
xml+=node(0x101,P(prefix,uri));raw=b'';offset=[]
for s in st:
 b=s.encode('utf-16le');offset.append(len(raw));raw+=U(len(b)//2)+b+U(0)
raw+=bytes(-len(raw)%4);pool=chunk(1,28,P(len(st),0,0,28+4*len(st),0)+P(*offset)+raw)
files={'AndroidManifest.xml':chunk(3,8,pool+chunk(0x180,8,P(*attrs.values()))+xml),'classes.dex':dex,'assets/index.html':open('android/index.html','rb').read()}
def strings(items):
 data=b'';offset=[]
 for name in items:
  offset.append(len(data));value=name.encode('utf-16le');data+=U(len(value)//2)+value+U(0)
 data+=bytes(-len(data)%4)
 return chunk(1,28,P(len(items),0,0,28+4*len(items),0)+P(*offset)+data)
types=strings(['drawable']);keys=strings(['boules'])
spec=chunk(0x202,16,P(1,1,0))
config=P(64)+bytes(60)
entry=U(8,0)+P(0)+U(8)+bytes([0,3])+P(0)
typ=chunk(0x201,84,P(1,1,88)+config+P(0)+entry)
pkgname='fr.famille.dodocheconcours26'.encode('utf-16le').ljust(256,b'\x00')
package=chunk(0x200,288,P(127)+pkgname+P(288,1,288+len(types),1,0)+types+keys+spec+typ)
files['resources.arsc']=chunk(2,12,P(1)+strings(['res/drawable/boules.png'])+package)
files['res/drawable/boules.png']=files['assets/icon.png']=open('android/icon.png','rb').read()

files['assets/PDFJS-LICENSE.txt']=open('android/PDFJS-LICENSE.txt','rb').read()
files['assets/reader.js']=open('android/reader.js','rb').read()
from pathlib import Path
files['assets/ZXing-NOTICES.txt']=Path('android/ZXing-NOTICES.txt').read_bytes()
def digest(b):return base64.b64encode(H.sha256(b).digest())
sections={n:b'Name: '+n.encode()+b'\r\nSHA-256-Digest: '+digest(b)+b'\r\n\r\n' for n,b in files.items()}
mf=b'Manifest-Version: 1.0\r\n\r\n'+b''.join(sections.values());sf=b'Signature-Version: 1.0\r\nSHA-256-Digest-Manifest: '+digest(mf)+b'\r\n\r\n'+b''.join(b'Name: '+n.encode()+b'\r\nSHA-256-Digest: '+digest(b)+b'\r\n\r\n' for n,b in sections.items())
from pathlib import Path
keyfile=Path(os.environ['DODOCHE_SIGNING_KEY'])
key=serialization.load_pem_private_key(keyfile.read_bytes(),None)
name=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'La Familiale de Dodoche')]);cert=x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key()).serial_number(1).not_valid_before(datetime.datetime(2025,1,1)).not_valid_after(datetime.datetime(2050,1,1)).sign(key,hashes.SHA256())
if H.sha256(cert.public_bytes(serialization.Encoding.DER)).hexdigest() != 'a0f196212984431ac48c42122a1332e10af5b2ec4df6bd4846b9daf07b5f44ee': raise SystemExit('La signature doit correspondre à la v26.')
sig=pkcs7.PKCS7SignatureBuilder().set_data(sf).add_signer(cert,key,hashes.SHA256()).sign(serialization.Encoding.DER,[pkcs7.PKCS7Options.DetachedSignature,pkcs7.PKCS7Options.Binary])
files.update({'META-INF/MANIFEST.MF':mf,'META-INF/CERT.SF':sf,'META-INF/CERT.RSA':sig})
with zipfile.ZipFile(apk,'w',zipfile.ZIP_DEFLATED) as z:
 for n,b in files.items():
  if n=='resources.arsc':
   info=zipfile.ZipInfo(n)
   needed=(-z.fp.tell()-30-len(n))%4
   if needed:info.extra=U(0xcafe,needed)+bytes(needed)
   z.writestr(info,b)
  else:z.writestr(n,b)
from cryptography.hazmat.primitives.asymmetric import padding
def lp(b):return P(len(b))+b
def q(n):return S.pack('<Q',n)
file=Path(apk)
raw=file.read_bytes()
endpos=raw.rindex(b'PK\x05\x06')
end=raw[endpos:]
centralpos=S.unpack_from('<I',end,16)[0]
local,central=raw[:centralpos],raw[centralpos:endpos]
parts=[local,central,end]
def sha(b):return H.sha256(b).digest()
def content_hash(parts):
 chunks=[section[i:i+1048576] for section in parts for i in range(0,len(section),1048576)]
 return sha(b'\x5a'+P(len(chunks))+b''.join(sha(b'\xa5'+lp(b)) for b in chunks))
alg=P(0x0103)
signed=lp(lp(alg+lp(content_hash(parts))))+lp(lp(cert.public_bytes(serialization.Encoding.DER)))+lp(b'')
signature=key.sign(signed,padding.PKCS1v15(),hashes.SHA256())
public=key.public_key().public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)
value=lp(lp(lp(signed)+lp(lp(alg+lp(signature)))+lp(public)))
pair=q(4+len(value))+P(0x7109871a)+value
size=q(len(pair)+24);block=size+pair+size+b'APK Sig Block 42'
file.write_bytes(local+block+central+end[:16]+P(centralpos+len(block))+end[20:])
