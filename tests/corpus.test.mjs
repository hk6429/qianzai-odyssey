import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {regions,companions,chapterStory} from '../story.js';
const read=n=>JSON.parse(readFileSync(new URL('../data/'+n+'.json',import.meta.url)));
const bank=read('questions'),works=read('works'),curriculum=read('curriculum');
const canon=s=>s.replace(/[^\u3400-\u9fff]/g,'');
test('10,000 unique original excerpts, not repeated question variants',()=>{assert.equal(bank.length,10000);assert.equal(new Set(bank.map(q=>canon(q.quote))).size,10000);assert.equal(new Set(bank.map(q=>q.id)).size,10000);});
test('every answer is traceable to continuous original text and unambiguous distinct options',()=>{
 for(const q of bank){const w=works[q.workId];assert.ok(w,q.id);assert.ok(canon(w.content).includes(canon(q.left+q.answer)),q.id);assert.equal(q.era,w.era);assert.equal(q.era,Math.floor(q.chapter/10));assert.equal(q.genre,w.genre);assert.equal(q.author,w.author);assert.equal(q.options.length,4);assert.equal(new Set(q.options).size,4);assert.ok(q.options.includes(q.answer));for(const option of q.options){if(option!==q.answer)assert.ok(!w.content.includes(option));}assert.match(q.sourceURL,/^https:\/\/github\.com\/(aopao\/chinese-gushiwen|snowtraces\/poetry-source)\/blob\/[a-f0-9]{40}\//);assert.ok(!/[□�]/.test(q.quote));assert.ok(!q.quote.includes('為政子曰'));assert.ok(!q.quote.includes('傳不習乎，子曰')); }
});
test('100 chapters follow exactly ten requested eras, without mixing',()=>{
 assert.deepEqual(regions.map(r=>r.name),['先秦','漢朝','三國','魏晉六朝','隋唐','五代十國','宋','元','明','清']);assert.equal(curriculum.length,100);
 assert.deepEqual(curriculum.flatMap(c=>c.ids),bank.map(q=>q.id));
 assert.deepEqual(regions.map((_,i)=>bank.filter(q=>q.era===i).length),[1000,800,500,900,2200,400,2000,600,800,800]);
 for(const c of curriculum){assert.equal(c.era,Math.floor(c.id/10));assert.equal(c.ids.length,c.quota);for(const id of c.ids)assert.equal(bank.find(q=>q.id===id).chapter,c.id);}
});
test('poetry, ci, qu, prose, parallel prose and essential classic anchors exist',()=>{
 for(const g of ['詩','詞','曲','古文','駢文','辭賦'])assert.ok(bank.filter(q=>q.genre===g).length>=20,g);
 for(const [era,phrase] of [[0,'學而不思則罔'],[0,'吾將上下而求索'],[2,'先帝創業'],[3,'採菊東籬下'],[3,'風煙俱淨'],[4,'落霞與孤鶩齊飛'],[6,'明月幾時有'],[6,'但願人長久'],[7,'枯藤老樹昏鴉'],[9,'人生若只如初見']])assert.ok(bank.some(q=>q.era===era&&q.quote.includes(phrase)),phrase);
 assert.ok(bank.filter(q=>q.era===7&&q.genre==='曲').length>400);assert.ok(bank.filter(q=>q.era===6&&q.genre==='詞').length>400);
 assert.ok(!bank.some(q=>q.era<4&&['詞','曲'].includes(q.genre)));
 for(const q of bank){if(q.author==='諸葛亮'||q.author==='鍾會')assert.equal(q.era,2);if(['嵇康','阮籍','劉伶'].includes(q.author))assert.equal(q.era,3);if(q.author.startsWith('劉向'))assert.equal(q.era,1);}
});
test('ten mentors and 100 distinct story chapters',()=>{assert.equal(companions.length,10);assert.equal(new Set(Array.from({length:100},(_,i)=>chapterStory(i).title)).size,100);for(let i=0;i<10;i++){assert.equal(regions[i].steps.length,10);assert.ok(bank.some(q=>q.era===i&&(q.author===companions[i].name||companions[i].name==='納蘭性德'&&q.author==='納蘭性德')));}});
