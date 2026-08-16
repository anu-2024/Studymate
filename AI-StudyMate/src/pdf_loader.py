import re
def extract_uploaded_file(f):
 raw=f.getvalue(); name=f.name.lower()
 if name.endswith('.pdf'):
  import fitz; doc=fitz.open(stream=raw,filetype='pdf'); pages=[p.get_text('text') for p in doc]; return '\n'.join(pages),pages
 text=raw.decode('utf-8','ignore'); return text,[text]
def build_chunks(text,pages,source,chunk_size=900,overlap=120):
 out=[]
 for pn,page in enumerate(pages,1):
  s=re.sub(r'\s+',' ',page).strip(); start=0
  while start<len(s):
   end=min(len(s),start+chunk_size); out.append({'text':s[start:end],'source':source,'page':pn})
   if end==len(s): break
   start=end-overlap
 return out
