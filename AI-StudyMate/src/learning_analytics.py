def readiness_score(m): return 0 if not m else max(0,min(100,sum(x['mastery'] for x in m)/len(m)))
