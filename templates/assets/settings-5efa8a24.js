import{g as f}from"./getList-041abf44.js";import{k as y,g as S}from"./index-78dd3789.js";import{V as w,r as l}from"./vue-080993b5.js";const{message:s}=S(),m=async()=>await f("config/system"),d=async e=>await f("config/config",e),h=async e=>{const{msg:n,code:i}=await y("config/config",e);switch(i){case 0:return s==null||s.success(n),!0;default:return s==null||s.error(n),!1}},x=w("settings",()=>{const e=l({index:"root",name:"Root",children:[]}),n=l(""),i=(t,c)=>{c.children.length=0;for(const o in t){const g={index:o,name:typeof t[o]=="object"?"":t[o],children:[]};c.children.push(g),typeof t[o]=="object"&&i(t[o],g)}},u=async()=>{const t=await m();i(t,e.value)},a=async t=>{n.value=t},r=async t=>{await a(await d({name:t}))};return{getSettingsToml:u,getSettingsFile:r,saveSettingsFile:async t=>{await h({name:t,content:n.value})&&await r(t)},setContent:a,content:n,treeData:e}});export{x as u};