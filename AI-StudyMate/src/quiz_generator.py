import json,re
def generate_quiz(llm,store,topic,difficulty,n=5):
 hits=store.search(topic,8); ctx='\n'.join(f"[{h['source']} p.{h['page']}] {h['text']}" for h in hits)
 raw=llm.generate(f'''Create exactly {n} quiz questions about {topic} using ONLY this context. Difficulty: {difficulty}. Return ONLY a JSON array. Each object: type,topic,difficulty,question,options,answer. For MCQ use 4 options and answer exactly one option. For short answer use options [].\nCONTEXT:\n{ctx}''',500)
 try:return json.loads(re.search(r'\[.*\]',raw,re.S).group(0))[:n]
 except:return fallback(topic,difficulty,n,hits)
def fallback(topic,difficulty,n,hits):
 text=hits[0]['text'] if hits else topic; s=[x.strip() for x in re.split(r'(?<=[.!?])\s+',text) if len(x)>30] or [text]
 return [{'type':'Short Answer','topic':topic,'difficulty':difficulty,'question':f'Explain this point from the study material: {s[i%len(s)]}','options':[],'answer':s[i%len(s)][:80]} for i in range(n)]
