// usage: node render.js in.html out.pdf
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+path.resolve(process.argv[2]),{waitUntil:'networkidle'});
await p.pdf({path:process.argv[3],width:'297mm',height:'210mm',printBackground:true});await b.close();})();
