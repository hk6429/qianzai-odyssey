from pathlib import Path
import json,re,hashlib,subprocess,collections,random
R=Path(__file__).resolve().parents[1]
ERAS=['先秦','漢朝','三國','魏晉六朝','隋唐','五代十國','宋','元','明','清']
TARGET=[1000,800,500,900,2200,400,2000,600,800,800]
# Bibliographic overrides are explicit; source labels are retained separately.
OVERRIDE={'曹操':2,'曹植':2,'曹丕':2,'諸葛亮':2,'王粲':2,'陳琳':2,'徐幹':2,'劉楨':2,'阮瑀':2,'應瑒':2,'楊修':2,'薛道衡':4,'李密':3,'西晉·李密':3,'鍾會':2,'嵇康':3,'阮籍':3,'劉伶':3,'裴秀':3,'劉向':1,'劉向 撰':1,'劉向 編':1}
MAP={'先秦':0,'秦':0,'兩漢':1,'漢':1,'三國':2,'魏晉':3,'晉':3,'南北朝':3,'隋代':4,'隋':4,'唐代':4,'唐':4,'五代':5,'五代十國':5,'宋代':6,'宋':6,'元代':7,'元':7,'明代':8,'明':8,'清代':9,'清':9}
SKIP_AUTHORS={'于右任','陳曾壽','陳三立','蘇曼殊','顧隨','王國維','秋瑾','梁啟超','魯迅','黃節','弘一','柳亞子','陳獨秀','郁達夫','馬一浮','陳寅恪','夏曾佑','屈大均','錢謙益','陳子龍','顧炎武','吳偉業','黃宗羲','王夫之','施閏章','朱彝尊','陳維崧','吳嘉紀'}
PINWEN=['滕王閣序','與朱元思書','與陳伯之書','北山移文','答謝中書書','哀江南賦序']
FAMOUS=['學而時習之','不亦說乎','有朋自遠方來','知之為知之','學而不思則罔','己所不欲','三人行','生於憂患','天將降大任','富貴不能淫','窮則獨善其身','路漫漫其修遠兮','路曼曼其修遠兮','關關雎鳩','蒹葭蒼蒼','老驥伏櫪','對酒當歌','本是同根生','捐軀赴國難','非淡泊無以明志','採菊東籬下','山氣日夕佳','落霞與孤鶩齊飛','秋水共長天一色','海內存知己','床前明月光','舉頭望明月','天生我材必有用','長風破浪會有時','會當凌絕頂','國破山河在','野火燒不盡','舉杯邀明月','但願人長久','明月幾時有','大江東去','不識廬山真面目','人生自古誰無死','眾裡尋他千百度','尋尋覓覓','無可奈何花落去','問君能有幾多愁','剪不斷','小樓昨夜又東風','枯藤老樹昏鴉','興','桃花塢裡桃花庵','粉骨碎身渾不怕','我勸天公重抖擻','人生若只如初見','山一程','江山代有才人出']
def loadjson(p):
 text=p.read_text()
 try:return json.loads(text)
 except json.JSONDecodeError:return [json.loads(l) for l in text.splitlines() if l.strip()]
def trad(obj):
 result=subprocess.run(['opencc','-c','s2tw.json'],input=json.dumps(obj,ensure_ascii=False),text=True,capture_output=True,check=True)
 return json.loads(result.stdout)
def clean(text):
 text=text.replace('\\n','\n').replace('\\u3000',' ').replace('\\r','')
 text=re.sub(r'<[^>]+>','',text)
 text=re.sub(r'\([^)]*\)|（[^）]*）|\[[^]]*\]|【[^】]*】','',text)
 text=re.sub(r'[ \t\u3000]+','',text)
 return text.replace('“','「').replace('”','」').replace('‘','『').replace('’','』').strip()
def canon(text):return re.sub(r'[^\u3400-\u9fff]','',text)
works=[]
meta={'repo':'aopao/chinese-gushiwen','commit':'c2345d0abf2404b8b3601e4afc2e8fd12f90d6c8'}
for p in sorted((R/'sources/raw/gushiwen/guwen').glob('*.json')):
 for line,q in enumerate(loadjson(p),1):
  works.append(dict(title=q['title'],author=q['writer'],sourceDynasty=q['dynasty'],content=q['content'],tags=q.get('type',[]),origin='gushiwen',sourceFile=str(p.relative_to(R)),sourceIndex=line-1,sourceURL='https://github.com/'+meta['repo']+'/blob/'+meta['commit']+'/'+str(p.relative_to(R/'sources/raw/gushiwen'))+'#L'+str(line),priority=0))
# Five Dynasties and early periods get additional primary-text coverage; major
# dynasties use the selected anthology instead of unbounded corpus dumps.
meta2={'repo':'snowtraces/poetry-source','commit':'815fd2d12d231a1ad47dfe422e942e069264b2a2'}
for p in sorted((R/'sources/raw/poetry-source/source').glob('*/*/*.base.json')):
 form,dyn=p.parts[-3:-1]
 if dyn not in ['汉','三国','晋','南北朝','五代十国'] and not(form=='曲' and dyn=='元'):continue
 for i,q in enumerate(loadjson(p)):
  works.append(dict(title=q['title'],author=q['authorName'],sourceDynasty=q['dynasty'],content='\n'.join(q['content']),tags=[form],origin='poetry-source',sourceFile=str(p.relative_to(R)),sourceIndex=i,sourceURL='https://github.com/'+meta2['repo']+'/blob/'+meta2['commit']+'/'+str(p.relative_to(R/'sources/raw/poetry-source')),priority=1))
# Record only ancient original texts; no modern translation or commentary is used.
works=trad(works)
# Conversion can also change strings inside filenames, so source pointers are restored.
raw=[]
for p in sorted((R/'sources/raw/gushiwen/guwen').glob('*.json')):
 for line,q in enumerate(loadjson(p),1):raw.append((str(p.relative_to(R)),line-1,'https://github.com/'+meta['repo']+'/blob/'+meta['commit']+'/'+str(p.relative_to(R/'sources/raw/gushiwen'))+'#L'+str(line)))
for p in sorted((R/'sources/raw/poetry-source/source').glob('*/*/*.base.json')):
 form,dyn=p.parts[-3:-1]
 if dyn not in ['汉','三国','晋','南北朝','五代十国'] and not(form=='曲' and dyn=='元'):continue
 for i,q in enumerate(loadjson(p)):raw.append((str(p.relative_to(R)),i,'https://github.com/'+meta2['repo']+'/blob/'+meta2['commit']+'/'+str(p.relative_to(R/'sources/raw/poetry-source'))))
for w,(f,i,u) in zip(works,raw):w.update(sourceFile=f,sourceIndex=i,sourceURL=u)
# Reject authors whose biographies identify births after 1850: do not smuggle
# modern writing into Qing based on a birth-dynasty label.
biographies=[q for p in (R/'sources/raw/gushiwen/writer').glob('*.json') for q in loadjson(p)]
late=[]
for q in biographies:
 m=re.search(r'[（(][^）)]*?(1[89]\d{2})',q.get('simpleIntro','')[:160])
 if m and int(m[1])>=1850:late.append(q['name'])
SKIP_AUTHORS.update(trad(late))
seenworks=set();accepted=[];rejects=collections.Counter()
for w in works:
 author=w['author'].strip();dyn=w['sourceDynasty'];era=OVERRIDE.get(author,MAP.get(dyn))
 if era is None or author in SKIP_AUTHORS:rejects['outside-period-or-cross-era']+=1;continue
 if '後出師表' in w['title'] or '后出師表' in w['title']:rejects['disputed-attribution']+=1;continue
 content=clean(w['content']);key=(author,canon(content))
 if key in seenworks:rejects['duplicate-work']+=1;continue
 seenworks.add(key)
 if not content or '□' in content or '�' in content:rejects['damaged-work']+=1;continue
 genre='詩'
 tags=' '.join(w['tags'])
 if any(t in w['title'] for t in PINWEN):genre='駢文'
 elif any(t in tags for t in ['文言文','古文觀止','散文','書信','公文']):genre='古文'
 elif '辭賦' in tags or any(t in w['title'] for t in ['離騷','歸去來兮辭']):genre='辭賦'
 elif (era>=7 and '曲' in w['tags']) or (era==7 and any(t in w['title'] for t in ['天淨沙','山坡羊','折桂令','水仙子','沉醉東風','殿前歡','蟾宮曲','四塊玉','一枝花','雙調','越調','中呂','正宮','南呂'])):genre='曲'
 elif era>=4 and (any(t in w['title'] for t in ['菩薩蠻','浣溪沙','水調歌頭','念奴嬌','虞美人','蝶戀花','滿江紅','如夢令','卜算子','江城子','青玉案','西江月','雨霖鈴','定風波','聲聲慢','破陣子','臨江仙','鷓鴣天','相見歡','浪淘沙','漁家傲','清平樂','木蘭花','採桑子','鵲橋仙','鷓鴣','訴衷情','南鄉子','賀新郎','沁園春','滿庭芳','釵頭鳳','一剪梅','醉花陰','蘇幕遮','謁金門','摸魚兒','長相思','玉樓春','八聲甘州','憶江南','生查子','更漏子']) or '詞' in w['tags']):genre='詞'
 if genre=='詞' and era==4 and any(t in w['title'] for t in ['長相思','鷓鴣']) and not any(t in tags for t in ['宋詞','詞牌','唐五代詞']):genre='詩'
 w.update(author=author,era=era,content=content,genre=genre,id='w-'+hashlib.sha256((author+'|'+w['title']+'|'+content).encode()).hexdigest()[:16]);accepted.append(w)
# Famous-sentence anthology is used only as a ranking signal, not as an authority.
sentences=trad(loadjson(R/'sources/raw/gushiwen/sentence/sentence1-10000.json'))
famousset={canon(s['name']) for s in sentences}
pools=[[] for _ in ERAS];seen=set()
for w in accepted:
 n=0
 excerpt_text=re.sub(r'《[^》]+》(?=\s*(?:\n|$))','',w['content'])
 for sentence in re.split('[。；]',excerpt_text.replace('\n\n','。').replace('\n','').replace('？','，').replace('！','，')):
  sentence=re.sub('[「」『』《》〈〉]','',sentence).strip('：:，,、')
  clauses=[c.strip() for c in re.split('[，,]',sentence) if c.strip()]
  for k in range(0,len(clauses)-1,2):
   left,right=clauses[k:k+2]
   if not(3<=len(left)<=32 and 3<=len(right)<=18):continue
   if not re.fullmatch('[\u3400-\u9fff：、]+',left+right):continue
   if any(t in left+right for t in ['一作','譯文','註釋','拼音','作者','其一其二']):continue
   key=canon(left+right)
   if key not in canon(w['content']):continue
   if key in seen:continue
   seen.add(key);quote=left+'，'+right+'。'
   famous=key in famousset or any(t in left+right for t in FAMOUS if len(t)>2)
   priority=(0 if famous else 1,0 if w['genre'] in ['駢文','古文','曲','辭賦'] else 1,w['priority'],n)
   pools[w['era']].append(dict(id='q-'+hashlib.sha256(key.encode()).hexdigest()[:16],workId=w['id'],left=left,answer=right,quote=quote,famous=famous,rank=priority,era=w['era']))
   n+=1
bywork={w['id']:w for w in accepted}
selected=[];curriculum=[];seenids=set()
for era,(pool,target) in enumerate(zip(pools,TARGET)):
 print(ERAS[era],len(pool),'available /',target,'target',flush=True)
 if len(pool)<target:raise ValueError('Insufficient source material '+ERAS[era])
 # Round-robin across works after curated quotes; avoid a single long text filling a dynasty.
 pool.sort(key=lambda q:q['rank']);chosen=[];counts=collections.Counter()
 for cap in [3,6,12,30,1000]:
  for q in pool:
   if len(chosen)>=target:break
   if q['id'] in seenids or counts[q['workId']] >= (1000 if q['famous'] else max(cap,12) if bywork[q['workId']]['genre']=='駢文' else cap):continue
   chosen.append(q);counts[q['workId']]+=1;seenids.add(q['id'])
  if len(chosen)>=target:break
 # Famous pieces stay at the front; author/work grouping thereafter makes coherent small chapters.
 chosen.sort(key=lambda q:(not q['famous'],bywork[q['workId']]['priority'],q['rank'][1],bywork[q['workId']]['author'],bywork[q['workId']]['title'],q['id']))
 for local in range(10):
  part=chosen[local*(target//10):(local+1)*(target//10)];chapter=era*10+local
  genres=collections.Counter(bywork[q['workId']]['genre'] for q in part);authors=collections.Counter(bywork[q['workId']]['author'] for q in part)
  curriculum.append(dict(id=chapter,era=era,local=local,quota=len(part),focus='、'.join(genres.keys()),authors=[a for a,_ in authors.most_common(3)],ids=[q['id'] for q in part]))
  for q in part:q['chapter']=chapter
 selected+=chosen
# Distractors are real different lines from the SAME historical chapter group,
# length-matched when possible, deterministically sampled and shuffled.
answerpools={era:list(dict.fromkeys(x['answer'] for x in pool)) for era,pool in enumerate(pools)}
lengthpools={(era,length):[a for a in answers if abs(len(a)-length)<=2] for era,answers in answerpools.items() for length in range(3,19)}
for q in selected:
 w=bywork[q['workId']];rng=random.Random(q['id']);pool=lengthpools[q['era'],len(q['answer'])]
 candidates=rng.sample(pool,min(len(pool),40));candidates=[a for a in candidates if a!=q['answer'] and a not in w['content']]
 if len(candidates)<3:candidates=[a for a in pool if a!=q['answer'] and a not in w['content']]
 options=[q['answer']]+candidates[:3]
 if len(options)!=4:raise ValueError('Not enough distinct distractors')
 rng.shuffle(options);q.update(options=options,question=f'〈{w["title"]}〉中，「{q["left"]}，＿＿＿＿」應接哪一句？',author=w['author'],work=w['title'],genre=w['genre'],dynasty=w['sourceDynasty'],eraName=ERAS[q['era']],type='名句續寫',level=ERAS[q['era']],difficulty='入門' if q['famous'] else '進階',explain=f'本題所據原文為「{q["quote"]}」；「{q["answer"]}」承接前句。可展開完整原文，對照上下文再記憶。',source=f'{w["author"]}〈{w["title"]}〉',sourceURL=w['sourceURL']);del q['rank']
used={q['workId'] for q in selected};exportworks={key:{k:v for k,v in bywork[key].items() if k not in ['priority','tags']} for key in sorted(used)}
(R/'data/questions.json').write_text(json.dumps(selected,ensure_ascii=False,separators=(',',':')))
(R/'data/works.json').write_text(json.dumps(exportworks,ensure_ascii=False,separators=(',',':')))
(R/'data/curriculum.json').write_text(json.dumps(curriculum,ensure_ascii=False,separators=(',',':')))
audit=dict(questions=len(selected),uniqueQuotes=len({canon(q['quote']) for q in selected}),works=len(exportworks),eras=[dict(name=ERAS[i],count=TARGET[i],available=len(pools[i]),genres=dict(collections.Counter(q['genre'] for q in selected if q['era']==i)),authors=len({q['author'] for q in selected if q['era']==i})) for i in range(10)],rejected=dict(rejects),conversion='OpenCC s2tw.json, original source preserved',classificationOverrides=OVERRIDE,excludedAuthors=sorted(SKIP_AUTHORS),sourcePolicy='Ancient original texts only; no modern notes, translations, commentary, or portraits.',rankedFamous=sum(q['famous'] for q in selected))
(R/'docs/corpus-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
print('DONE',audit['questions'],'unique excerpts',audit['uniqueQuotes'],'works',len(exportworks),'genres',collections.Counter(q['genre'] for q in selected),flush=True)
