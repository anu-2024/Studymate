def create_study_plan(m):
 w=sorted(m,key=lambda x:x['mastery']); topics=[x['topic'] for x in w[:3]] or ['your weakest topic']; return {'Today':[f'Review {topics[0]}',f'Solve 10 questions on {topics[0]}'],'Tomorrow':[f'Study {topics[min(1,len(topics)-1)]}','Take a mini quiz'],'Weekend':['Attempt a revision test','Review previous mistakes']}
