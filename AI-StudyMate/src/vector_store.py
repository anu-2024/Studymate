from pathlib import Path
import pickle,numpy as np
class LocalVectorStore:
 def __init__(self,path='data/vector_store'):
  self.path=Path(path); self.path.mkdir(parents=True,exist_ok=True); self.index=None; self.items=[]; self.embedder=None; self._load()
 def _embed(self):
  if self.embedder is None:
   from sentence_transformers import SentenceTransformer; self.embedder=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
  return self.embedder
 def add(self,chunks):
  if not chunks:return
  import faiss
  e=self._embed().encode([x['text'] for x in chunks],normalize_embeddings=True,show_progress_bar=False).astype('float32')
  if self.index is None:self.index=faiss.IndexFlatIP(e.shape[1])
  self.index.add(e); self.items.extend(chunks); self.persist()
 def search(self,q,k=5):
  if self.index is None:return []
  e=self._embed().encode([q],normalize_embeddings=True).astype('float32'); scores,ids=self.index.search(e,min(k,len(self.items)))
  return [{**self.items[int(i)],'score':float(s)} for s,i in zip(scores[0],ids[0]) if i>=0]
 def count(self):return len(self.items)
 def persist(self):
  if self.index is None:return
  import faiss; faiss.write_index(self.index,str(self.path/'index.faiss')); pickle.dump(self.items,open(self.path/'items.pkl','wb'))
 def _load(self):
  try:
   import faiss; fp=self.path/'index.faiss'; ip=self.path/'items.pkl'
   if fp.exists() and ip.exists(): self.index=faiss.read_index(str(fp)); self.items=pickle.load(open(ip,'rb'))
  except Exception: self.index=None; self.items=[]
