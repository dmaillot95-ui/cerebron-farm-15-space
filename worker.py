import os, json, time
from gradio_client import Client

role=os.environ.get('ROLE','SPACE_ANALYST')
mission=open('MISSION.md',encoding='utf-8').read()
models=['huggingface-projects/llama-3.2-3B-Instruct','huggingface-projects/gemma-2-9b-it']
model=models[hash(role)%len(models)]
prompt=f'''You are role {role} in CEREBRON Farm 15 Space.\n{mission}\nProduce a rigorous specialist report. Separate ESTABLISHED, DERIVED, SIMULATED, CONJECTURAL, UNKNOWN. Identify assumptions, equations/units where relevant, failure modes, verification steps, evidence needed, contradictions, and transferable conclusions. Never claim a simulation is a test.'''
result={'role':role,'model':model,'status':'FAILED','output':''}
try:
    c=Client(model, verbose=False)
    out=c.predict(message=prompt, system_message='Rigorous aerospace engineering analysis. CLAIM <= EVIDENCE.', max_tokens=1800, temperature=0.35, top_p=0.9, api_name='/chat')
    result['status']='SUCCESS'; result['output']=str(out)
except Exception as e:
    result['error']=repr(e)
os.makedirs('out',exist_ok=True)
with open(f'out/{role}.json','w',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2)
if result['status']!='SUCCESS': raise SystemExit(2)
