import sqlite3
from pathlib import Path
from datetime import datetime
DB=Path('database/studymate.db'); DB.parent.mkdir(parents=True,exist_ok=True)
def conn():return sqlite3.connect(DB)
def init_db():
 c=conn(); c.executescript('''CREATE TABLE IF NOT EXISTS documents(id INTEGER PRIMARY KEY,filename TEXT,pages INTEGER,uploaded_at TEXT); CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY,topic TEXT,difficulty TEXT,user_answer TEXT,correct_answer TEXT,correct INTEGER,created_at TEXT);'''); c.commit(); c.close()
def save_document(f,p):
 c=conn();c.execute('INSERT INTO documents(filename,pages,uploaded_at) VALUES(?,?,?)',(f,p,datetime.now().isoformat()));c.commit();c.close()
def save_attempt(t,d,u,a,ok):
 c=conn();c.execute('INSERT INTO attempts(topic,difficulty,user_answer,correct_answer,correct,created_at) VALUES(?,?,?,?,?,?)',(t,d,u,a,int(ok),datetime.now().isoformat()));c.commit();c.close()
def get_dashboard_data():
 c=conn(); docs=c.execute('SELECT COUNT(*) FROM documents').fetchone()[0]; q=c.execute('SELECT COUNT(*) FROM attempts').fetchone()[0]; avg=c.execute('SELECT COALESCE(AVG(correct)*100,0) FROM attempts').fetchone()[0];c.close();return {'documents':docs,'questions':q,'avg_score':avg}
def get_topic_mastery():
 c=conn(); rows=c.execute('SELECT topic,COUNT(*),SUM(correct),ROUND(AVG(correct)*100,1) FROM attempts GROUP BY topic').fetchall();c.close();return [{'topic':r[0],'attempts':r[1],'correct':r[2],'mastery':float(r[3] or 0)} for r in rows]
