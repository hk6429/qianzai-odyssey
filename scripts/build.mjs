import {readFile,writeFile,mkdir,copyFile,readdir,rm} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const root=new URL('../',import.meta.url),out=new URL('dist/',root);
const bank=JSON.parse(await readFile(new URL('data/questions.json',root)));
if(bank.length!==10000||new Set(bank.map(q=>q.id)).size!==10000)throw Error('萬題資料驗證失敗');
await rm(out,{recursive:true,force:true});await mkdir(out,{recursive:true});
const files=['cloud-auth.js','cloud-state.js','cloud-model.js','cloud-auth.css','data/cloud-bank.json','index.html','style.css','immersive.css','immersive.js','app.js', 'choice-keyboard.js','journey-progress.js','engine.js','story.js','_headers','SOURCE-NOTICES.md'];
for(const dir of ['data','assets'])await mkdir(new URL(dir+'/',out),{recursive:true});
files.push(...['questions','works','curriculum'].map(n=>'data/'+n+'.json'));
files.push(...(await readdir(new URL('assets/',root))).filter(f=>/\.(webp|svg)$/.test(f)).map(f=>'assets/'+f));
const hashes={};
for(const file of files){await copyFile(new URL(file,root),new URL(file,out));hashes[file]=createHash('sha256').update(await readFile(new URL(file,out))).digest('hex');}
await writeFile(new URL('docs/build-manifest.json',root),JSON.stringify(hashes,null,2));
console.log(`Built ${bank.length} excerpts, 100 chapters, 10 eras; ${files.length} public files.`);
