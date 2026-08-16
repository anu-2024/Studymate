def generate_notes(llm,store_hits,topic,kind):
 ctx='\n\n'.join(f"[{x['source']} p.{x['page']}] {x['text']}" for x in store_hits); return llm.generate(f'Create {kind} for {topic} using ONLY this material. Be concise and exam-oriented. Include source references.\n{ctx}',450)
