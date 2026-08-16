import streamlit as st
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
from src.pdf_loader import extract_uploaded_file,build_chunks
from src.vector_store import LocalVectorStore
from src.chatbot import LocalLLM,answer_question
from src.quiz_generator import generate_quiz
from src.database import init_db,save_document,save_attempt,get_dashboard_data,get_topic_mastery
from src.knowledge_gap import analyze_gaps
from src.study_plan import create_study_plan
from src.notes_generator import generate_notes
from src.learning_analytics import readiness_score
st.set_page_config(page_title='AI StudyMate',page_icon='🎓',layout='wide')
@st.cache_resource
def store(): return LocalVectorStore()
@st.cache_resource
def llm(): return LocalLLM()
init_db(); vs=store(); model=llm()
if 'quiz' not in st.session_state: st.session_state.quiz=[]
with st.sidebar:
 st.title('🎓 AI StudyMate'); st.caption('Adaptive RAG Learning Copilot')
 page=st.radio('Navigate',['🏠 Dashboard','📄 Documents','💬 AI Tutor','📝 Quiz','🧠 Knowledge Gaps','🎯 Study Plan','📚 Smart Notes'])
 st.info('No API key required. Uses a public pretrained local Hugging Face model.')
if page=='🏠 Dashboard':
 st.title('AI StudyMate'); st.write('Learn from your materials, practice, discover gaps and adapt.')
 d=get_dashboard_data(); m=get_topic_mastery(); r=readiness_score(m)
 a,b,c,d4=st.columns(4); a.metric('Documents',d['documents']); b.metric('Questions',d['questions']); c.metric('Quiz Average',f"{d['avg_score']:.0f}%"); d4.metric('Exam Readiness',f'{r:.0f}%')
 if m:
  import pandas as pd
  st.subheader('Topic Mastery'); st.bar_chart(pd.DataFrame(m).set_index('topic')['mastery'])
 else: st.info('Upload material and complete a quiz to build your learning profile.')
 st.subheader('Demo'); st.write('Upload the included trial material → ask a grounded question → generate quiz → submit → inspect gaps → view study plan.')
elif page=='📄 Documents':
 st.title('📄 Smart Document Upload'); fs=st.file_uploader('Upload PDF, TXT or Markdown',type=['pdf','txt','md'],accept_multiple_files=True)
 if fs and st.button('Process documents',type='primary'):
  for f in fs:
   text,pages=extract_uploaded_file(f); chunks=build_chunks(text,pages,f.name); vs.add(chunks); save_document(f.name,len(pages))
  vs.persist(); st.success(f'Processed {len(fs)} document(s).')
 st.write('Indexed chunks:',vs.count()); st.caption('Trial material: data/sample_materials/machine_learning_trial.md')
elif page=='💬 AI Tutor':
 st.title('💬 AI Tutor')
 if vs.count()==0: st.warning('Upload a study document first.')
 else:
  q=st.text_area('Ask a question',placeholder='Explain logistic regression in simple terms.')
  if st.button('Ask AI',type='primary') and q.strip():
   with st.spinner('Retrieving evidence and generating answer...'): res=answer_question(model,vs,q)
   st.markdown('### Answer'); st.write(res['answer']); st.metric('Confidence',f"{res['confidence']:.0f}%")
   st.markdown('### Sources')
   for s in res['sources']:
    with st.expander(f"{s['source']} — Page {s['page']}"): st.write(s['text'])
elif page=='📝 Quiz':
 st.title('📝 AI Quiz Generator'); topic=st.text_input('Topic','Machine Learning'); diff=st.selectbox('Difficulty',['Easy','Medium','Hard']); n=st.slider('Questions',3,10,5)
 if st.button('Generate Quiz',type='primary'):
  if vs.count()==0: st.warning('Upload study material first.')
  else:
   with st.spinner('Generating questions from study material...'): st.session_state.quiz=generate_quiz(model,vs,topic,diff,n)
 if st.session_state.quiz:
  answers={}
  for i,q in enumerate(st.session_state.quiz):
   st.markdown(f"**Q{i+1}. {q['question']}**")
   answers[i]=st.radio('Answer',q.get('options',[]) or ['Type answer'],key=f'q{i}') if q.get('options') else st.text_input('Answer',key=f'q{i}')
  if st.button('Submit Quiz',type='primary'):
   correct=0
   for i,q in enumerate(st.session_state.quiz):
    ua=str(answers.get(i,'')); ok=ua.strip().lower()==str(q['answer']).strip().lower(); correct+=ok; save_attempt(q['topic'],q['difficulty'],ua,q['answer'],ok)
   st.success(f'Score: {correct}/{len(st.session_state.quiz)} ({100*correct/len(st.session_state.quiz):.0f}%)')
elif page=='🧠 Knowledge Gaps':
 st.title('🧠 Knowledge Gap Detection'); m=get_topic_mastery()
 if not m: st.info('Complete a quiz first.')
 else:
  r=analyze_gaps(m); x,y=st.columns(2)
  with x:
   st.subheader('Strong Topics')
   for a in r['strong']: st.success(f"{a['topic']}: {a['mastery']:.0f}%")
  with y:
   st.subheader('Needs Attention')
   for a in r['weak']: st.error(f"{a['topic']}: {a['mastery']:.0f}%")
  st.info(r['message'])
elif page=='🎯 Study Plan':
 st.title('🎯 Personalized Study Plan'); m=get_topic_mastery()
 if not m: st.info('Complete a quiz first.')
 else:
  for day,tasks in create_study_plan(m).items():
   st.subheader(day)
   for task in tasks: st.checkbox(task,key=day+task)
elif page=='📚 Smart Notes':
 st.title('📚 Smart Notes Generator'); topic=st.text_input('Topic','Machine Learning'); kind=st.selectbox('Generate',['Summary','Revision Notes','Flashcards','Formula Sheet','Cheat Sheet'])
 if st.button('Generate',type='primary'):
  if vs.count()==0: st.warning('Upload material first.')
  else:
   with st.spinner('Creating notes...'): st.markdown(generate_notes(model,vs.search(topic,5),topic,kind))
