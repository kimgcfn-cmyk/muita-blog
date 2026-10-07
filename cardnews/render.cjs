const {chromium}=require('/opt/node22/lib/node_modules/playwright');
const fs=require('fs'),path=require('path');
(async()=>{
 const dir=path.join(__dirname,'html'),out=path.join(__dirname,'png');fs.mkdirSync(out,{recursive:true});
 const files=JSON.parse(fs.readFileSync(path.join(dir,'_files.json')));
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const p=await b.newPage({viewport:{width:1080,height:1080}});
 for(const f of files){await p.goto('file://'+path.join(dir,f));await p.evaluate(()=>document.fonts.ready);
  const ov=await p.evaluate(()=>{const m=document.querySelector('.main,.bd');return m&&m.scrollHeight>m.clientHeight+2});
  if(ov)console.log('OVERFLOW',f);
  await p.screenshot({path:path.join(out,f.replace('.html','.png'))});}
 await b.close();
})();
