import{h as f,e as h}from"./index-831a2fe3.js";import{d as g,$ as w,r as x,f as b,H as k,R as v,S as o,U as s,N as e,c as y,J as i}from"./vue-3732522d.js";import{E as B,F as D,am as N,J as C}from"./naiveUI-5e433394.js";import"./lodash-18690875.js";import"./ionicons5-ced7f89a.js";const S=i("span",null,"下载器",-1),V={style:{height:"100%"}},F=g({__name:"index",setup(z){const{isMobile:l,isPad:J,isDesktop:L}=f(),t=h(),{getDownloaderList:_,editDownloader:d}=t,{downloaderList:r,columns:c}=w(t),n=x(!1);return b(async()=>{n.value=!0,await _(),n.value=!1}),(M,a)=>{const u=D,m=N,p=C;return k(),v(p,{hoverable:"",embedded:""},{header:o(()=>[s(u,{justify:"space-between"},{default:o(()=>[S,s(e(B),{type:"success",size:"small",onClick:a[0]||(a[0]=P=>e(d)(0))},{default:o(()=>[y(" 添加 ")]),_:1})]),_:1})]),default:o(()=>[i("div",V,[s(m,{columns:e(c),data:e(r),loading:e(n),"min-height":e(l)?520:680,bordered:"","flex-height":"","max-height":"720",size:"small",striped:""},null,8,["columns","data","loading","min-height"])])]),_:1})}}});export{F as default};
