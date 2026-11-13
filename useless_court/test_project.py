import sys, tempfile, os, json
from pathlib import Path
root=Path(__file__).parent
sys.path.insert(0,str(root))
from core.cases import GROUPS,load_cases,filter_cases
from core.trial import new_trial,available_evidence,submit_evidence,case_rebuttals,respond
from core.jury import judge
from core.verdict import make_verdict
from core.storage import save_case,history
cases=load_cases()
assert len(cases)==155 and len(GROUPS)==12
assert len({c['name'] for c in cases})==155
assert len(filter_cases(cases,group='AI·미래기술'))==10
assert len(filter_cases(cases,keyword='외계인'))>=1
for case in cases:
  for side in ['원고 측','피고 측']:
    trial=new_trial(case,side)
    evidence=available_evidence(case)
    assert len(evidence)==8,(case['name'],len(evidence))
    assert len({e['name'] for e in evidence})==8
    submit_evidence(trial,[0,1,2],{})
    rebuttals=case_rebuttals(case,side)
    assert len(rebuttals)==3
    for i in range(3):
       assert len(rebuttals[i]['choices'])==4
       assert rebuttals[i]['opponent']
       respond(trial,i%3)
    assert trial['stage']=='ready_for_jury'
    result=judge(trial)
    doc=make_verdict(trial,result)
    assert len(result['votes'])==3
    assert result['verdict'] in ('유죄','무죄')
    assert len(doc['text'])>40
print('PASS 310 complete trials; 155 cases; 12 groups; 8 evidences; 3 rounds')
