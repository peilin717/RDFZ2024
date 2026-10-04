#!/usr/bin/env python3
"""Local static audio preview with byte ranges (needed for Ogg seek/duration).
No dependencies beyond the standard library. Binds loopback by default.
"""
import argparse,os,re,shutil
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
DEFAULT=Path(__file__).resolve().parents[4]/'music-work'
class RangeHandler(SimpleHTTPRequestHandler):
 def send_head(self):
  self.remaining=None;path=Path(self.translate_path(self.path));value=self.headers.get('Range')
  if not value or not path.is_file():return super().send_head()
  match=re.fullmatch(r'bytes=(\d*)-(\d*)',value.strip())
  if not match or not any(match.groups()):return super().send_head()
  size=path.stat().st_size;first,last=match.groups()
  if first:start=int(first);end=min(int(last),size-1) if last else size-1
  else:start=max(0,size-int(last));end=size-1
  if start>=size or end<start:
   self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.send_header('Content-Length','0');self.end_headers();return None
  try:stream=path.open('rb')
  except OSError:self.send_error(404);return None
  stream.seek(start);self.remaining=end-start+1
  self.send_response(206);self.send_header('Content-type',self.guess_type(str(path)));self.send_header('Content-Length',str(self.remaining));self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Last-Modified',self.date_time_string(path.stat().st_mtime));self.end_headers();return stream
 def end_headers(self):self.send_header('Accept-Ranges','bytes');super().end_headers()
 def copyfile(self,source,outputfile):
  if self.remaining is None:return super().copyfile(source,outputfile)
  left=self.remaining
  while left:
   data=source.read(min(65536,left))
   if not data:break
   outputfile.write(data);left-=len(data)
 def log_message(self,*args):pass
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--port',type=int,default=4176);ap.add_argument('--bind',default='127.0.0.1');ap.add_argument('--directory',default=os.environ.get('RDFZ_MUSIC_WORK',str(DEFAULT)));a=ap.parse_args()
 print(f'Original soundtrack preview: http://{a.bind}:{a.port}/preview.html',flush=True)
 ThreadingHTTPServer((a.bind,a.port),partial(RangeHandler,directory=a.directory)).serve_forever()
