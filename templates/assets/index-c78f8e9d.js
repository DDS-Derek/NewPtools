import{u as c}from"./website-a01091dc.js";import{d as l,_ as p,r as u,f as _,G as d,Q as f,M as t}from"./vue-080993b5.js";import{a7 as g}from"./naiveUI-1e53cf3e.js";import"./index-6c720e4c.js";import"./lodash-5fc50ca6.js";import"./ionicons5-b765452e.js";import"./download-9fdf4d81.js";import"./getList-b7db4d33.js";import"./baseStyle-3d03bd09.js";const z=l({__name:"index",setup(b){const e=c(),{getSiteList:a}=e,{columns:n,siteList:r}=p(e),i=s=>s.id,o=u(!1);return _(async()=>{o.value=!0,await a(),o.value=!1}),(s,w)=>{const m=g;return d(),f(m,{columns:t(n),data:t(r),"row-key":i,size:"small",loading:t(o),bordered:"",striped:""},null,8,["columns","data","loading"])}}});export{z as default};