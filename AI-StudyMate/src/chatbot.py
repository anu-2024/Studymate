import os,re
MODEL_ID=os.getenv('STUDYMATE_MODEL','Qwen/Qwen2.5-1.5B-Instruct')
class LocalLLM:
 def __init__(self): self.model=None; self.tokenizer=None; self.error=None
 def _load(self):
  if self.model is not None:return
  try:
   from transformers import AutoTokenizer,AutoModelForCausalLM
   self.tokenizer=AutoTokenizer.from_pretrained(MODEL_ID); self.model=AutoModelForCausalLM.from_pretrained(MODEL_ID,low_cpu_mem_usage=True); self.model.eval()
  except Exception as e:self.error=e
 def generate(self,prompt,max_new_tokens=300):
  self._load()
  if self.model is None:return 'Local model could not be loaded: '+str(self.error)
  import torch
  msgs=[{'role':'system','content':'You are AI StudyMate, a careful academic tutor. Use only supplied study context. If the context is insufficient, say so.'},{'role':'user','content':prompt}]
  text=self.tokenizer.apply_chat_template(msgs,tokenize=False,add_generation_prompt=True); inp=self.tokenizer(text,return_tensors='pt')
  with torch.no_grad(): out=self.model.generate(**inp,max_new_tokens=max_new_tokens,do_sample=False)
  return self.tokenizer.decode(out[0][inp['input_ids'].shape[-1]:],skip_special_tokens=True).strip()
def answer_question(llm,store,q):
 hits=store.search(q,5)
 if not hits:return {'answer':'I could not find sufficient information in the uploaded study materials.','confidence':0,'sources':[]}
 ctx='\n\n'.join(f"[Source: {h['source']}, page {h['page']}]\n{h['text']}" for h in hits)
 ans=llm.generate(f'Answer using ONLY this context. Explain for a student. Do not invent unsupported facts.\n\nCONTEXT:\n{ctx}\n\nQUESTION:\n{q}',260)
 conf=max(35,min(98,50+45*max(h['score'] for h in hits))); return {'answer':ans,'confidence':conf,'sources':hits}
