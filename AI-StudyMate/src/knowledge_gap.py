def analyze_gaps(m):
 weak=sorted(m,key=lambda x:x['mastery'])[:5]; strong=sorted(m,key=lambda x:x['mastery'],reverse=True)[:5]; return {'weak':weak,'strong':strong,'message':'Prioritize weak concepts, then retake a quiz to verify improvement.'}
