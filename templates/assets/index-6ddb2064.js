import{H as S}from"./core-cdc9db85.js";import{u as k}from"./settings-c1a8956e.js";import{d as C,$ as w,r as F,f as N,H as o,I as B,U as u,S as _,N as e,J as V,a3 as b,R as c,c as j,a4 as E,M as H,F as R}from"./vue-3732522d.js";import{E as $,F as I,P as J,ar as M}from"./naiveUI-5e433394.js";import{b as T}from"./index-831a2fe3.js";import"./lodash-18690875.js";import"./ionicons5-ced7f89a.js";const U=["textContent"],D=C({__name:"index",setup(P){const i=k(),{content:n}=w(i),t=F(!1),{getSettingsFile:d,saveSettingsFile:m,setContent:f}=i;N(async()=>{await d("hosts")});let a="";const g=async l=>{t.value=l,l?a=`${n.value}`:n.value!==a&&await f(a)},x=async()=>{await m("hosts"),t.value=!1};return(l,s)=>{const p=$,y=I,v=J,h=M;return o(),B(R,null,[u(y,{justify:"end"},{default:_(()=>[u(p,{type:e(t)?"warning":"primary",onClick:s[0]||(s[0]=r=>g(!e(t)))},{default:_(()=>[V("span",{textContent:b(e(t)?"取消":"编辑")},null,8,U)]),_:1},8,["type"]),e(t)?(o(),c(p,{key:0,type:"success",onClick:x},{default:_(()=>[j(" 保存 ")]),_:1})):E("",!0)]),_:1}),e(t)?(o(),c(v,{key:0,value:e(n),"onUpdate:value":s[1]||(s[1]=r=>H(n)?n.value=r:null),class:"code mt-2",type:"textarea",placeholder:""},null,8,["value"])):(o(),c(h,{key:1,code:e(n),"show-line-numbers":"",class:"text-16px px-2 mt-2",hljs:e(S),language:"host"},null,8,["code","hljs"]))],64)}}});const Q=T(D,[["__scopeId","data-v-04d40d28"]]);export{Q as default};
