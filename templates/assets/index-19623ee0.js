import{u as Re,r as g}from"./download-c8ad9409.js";import{e as Be,f as w,g as Le,b as Fe}from"./index-a0a5d46f.js";import{r as T}from"./baseStyle-3d03bd09.js";import{d as Ne,$ as qe,r as y,h as Oe,o as Ke,H as c,I as Q,U as n,S as t,N as e,F as Y,a6 as Me,R as k,c as l,a3 as _,J as Pe,a4 as E,M as U,n as je}from"./vue-8caab7e7.js";import{F as b,q as Ve,ao as Ae,t as Ie,I as He,Y as Qe,$ as Ye,O as Ee,R as Ge,ad as Je,V as We,r as Xe,ap as Ze,aq as et,ar as tt,aj as nt,a4 as at,U as ot}from"./naiveUI-af4b8138.js";import"./getList-8e4a0623.js";import"./lodash-cc4aae98.js";import"./ionicons5-13bb01b1.js";const lt={style:{height:"100%"}},st=Ne({__name:"index",setup(it){const{message:S,dialog:rt,notification:dt}=Le(),F=Re(),{handleSelected:ut,getRepeatTorrentList:_t,addTorrent:G,getDownloaderList:J,getTorrentProp:pt,handleDefaultDownloader:W,handleDelete:X,handleUpdateDownloading:D,startFresh:Z,handleDeleteModal:ct,clearTimer:N,handleCheckRows:ee,removeBrush:te,handleSelect:ne,handleDownloadLoading:mt,onClickOutside:ae,handleCurrentRow:oe,handleShowDropdown:q,searchTorrent:O,openTorrentInfo:le}=F,{torrentList:K,qBitTorrentColumns:se,transmissionColumns:ie,downloaderList:$,downloaderSpeed:m,defaultDownloader:r,categoryFlag:z,qbHandleOptions:re,trHandleOptions:de,downloadLoading:ue,categories:_e,deleteFiles:R,showTorrentList:pe,checkedRowKeys:ft,timer:ce,deleteModal:x,downloadingTableRef:me,searchKey:B,addTorrentRules:fe,torrentPagination:M,repeatTorrentList:gt,showDropdown:ge,currentRow:yt}=qe(F);y(1e3*60);const{isMobile:ye,isPad:ht,isDesktop:vt}=Be(),P=y(0),j=y(0),h=y(!1),he=d=>{M.value.pageSize=d},ve=d=>({onContextmenu:o=>{o.preventDefault(),oe(d),q(!1),je().then(()=>{q(!0),P.value=o.clientX,j.value=o.clientY})},onDblclick:async o=>{await le(d.hash)}}),we=d=>{const o=d.trackers;let f="";if(o&&o.length>0)switch(o[0].status){case 0:case 4:f="tracker-error";break;case 1:case 3:f="tracker-warning";break}return d.super_seeding&&(f="super-seeding"),`${f}`},s=y({urls:"",category:"",cookie:"",is_paused:!1,upload_limit:0,download_limit:0,is_skip_checking:!1,use_auto_torrent_management:!0}),L=()=>{h.value=!1,s.value.urls=""},V=y(),ke=async()=>{var o;await((o=V.value)==null?void 0:o.validate()),await G(r.value.id,s.value)&&L()};return Oe(async()=>{await J(),$.value.length>0?(await W($.value[0].id),await D(r.value.id),await O()):S==null||S.error("请先添加下载器，然后重试！")}),Ke(async()=>{await N()}),(d,o)=>{const f=Ve,be=Ae,ze=Ie,u=He,xe=Qe,Ce=Ye,i=Ee,A=Ge,Te=Je,Ue=We,Se=Xe,C=Ze,I=et,v=tt,De=nt,H=at,$e=ot;return c(),Q(Y,null,[n(Ue,{hoverable:"",embedded:""},{default:t(()=>[n(ze,{value:e(r).id,"onUpdate:value":[o[0]||(o[0]=a=>e(r).id=a),e(D)],size:"small",type:"card"},{default:t(()=>[(c(!0),Q(Y,null,Me(e($),a=>(c(),k(be,{key:a.id,name:a.id,tab:a.name},{default:t(()=>[n(f,{width:"13",class:"mr-1",src:a.category==="Qb"?"/images/qb32.png":"/images/tr.png","preview-disabled":""},null,8,["src"]),l(" "+_(a.name),1)]),_:2},1032,["name","tab"]))),128))]),_:1},8,["value","onUpdate:value"]),Pe("div",lt,[n(u,{justify:"end"},{default:t(()=>[n(Ce,{accordion:""},{default:t(()=>[n(xe,{title:"",name:"1"},{"header-extra":t(()=>[e(m)?(c(),k(u,{key:0},{default:t(()=>[n(e(b),{type:"success",size:"small"},{default:t(()=>{var a,p;return[l(" ↑"+_(e(g)((a=e(m))==null?void 0:a.up_info_speed))+"/s（"+_(e(g)((p=e(m))==null?void 0:p.up_info_data))+"） ",1)]}),_:1}),n(e(b),{type:"warning",size:"small"},{default:t(()=>{var a,p;return[l(" ↓"+_(e(g)((a=e(m))==null?void 0:a.dl_info_speed))+"/s("+_(e(g)((p=e(m))==null?void 0:p.dl_info_data))+") ",1)]}),_:1})]),_:1})):E("",!0)]),default:t(()=>[n(u,null,{default:t(()=>[n(e(b),{type:"primary",size:"small"},{default:t(()=>{var a;return[l(" 剩余空间： "+_(e(g)((a=e(m))==null?void 0:a.free_space_on_disk)),1)]}),_:1}),n(e(b),{type:"primary",size:"small"},{default:t(()=>[l(" 种子数量： "+_(e(K).length),1)]),_:1}),n(e(b),{type:"primary",size:"small"},{default:t(()=>[l(" 做种体积： "+_(e(g)(e(K).reduce((a,p)=>a+p.size,0))),1)]),_:1})]),_:1})]),_:1})]),_:1}),e(ce)?(c(),k(i,{key:0,size:"tiny",type:"error",onClick:e(N)},{default:t(()=>[l(" 停止 ")]),_:1},8,["onClick"])):(c(),k(i,{key:1,size:"tiny",type:"success",onClick:e(Z)},{default:t(()=>[l(" 刷新 ")]),_:1},8,["onClick"])),n(A,{value:e(B),"onUpdate:value":o[1]||(o[1]=a=>U(B)?B.value=a:null),size:"tiny",onChange:e(O)},null,8,["value","onChange"]),n(i,{size:"tiny",type:"info",secondary:"",onClick:o[2]||(o[2]=a=>e(D)(e(r).id))},{icon:t(()=>[n(w,{icon:"Reload"})]),_:1}),n(i,{size:"tiny",type:"primary",onClick:o[3]||(o[3]=a=>h.value=!0)},{icon:t(()=>[n(w,{icon:"AddOutline"})]),_:1}),e(z)?(c(),k(i,{key:2,size:"tiny",type:"error",onClick:e(te)},{icon:t(()=>[n(w,{icon:"AddOutline"})]),default:t(()=>[l(" 刷流删种 ")]),_:1},8,["onClick"])):E("",!0),n(i,{tag:"a",href:`${e(r).host&&e(r).host.startsWith("http")?"":"http://"}${e(r).host}:${e(r).port}`,target:"_blank",secondary:"",type:"warning",size:"tiny"},{default:t(()=>[l(" 访问 ")]),_:1},8,["href"])]),_:1}),n(Te,{ref_key:"downloadingTableRef",ref:me,columns:e(z)?e(se):e(ie),data:e(pe),loading:e(ue),"min-height":e(ye)?520:680,"paginate-single-page":!1,pagination:e(M),"row-class-name":we,"row-key":a=>a.hash,"row-props":ve,bordered:"","flex-height":"","max-height":"720",size:"small",striped:"","virtual-scroll":"","onUpdate:pageSize":he,"onUpdate:checkedRowKeys":e(ee)},null,8,["columns","data","loading","min-height","pagination","row-key","onUpdate:checkedRowKeys"])])]),_:1}),n(Se,{placement:"bottom-start",trigger:"manual",size:"small",x:e(P),y:e(j),options:e(z)?e(re):e(de),show:e(ge),"on-clickoutside":e(ae),onSelect:e(ne)},null,8,["x","y","options","show","on-clickoutside","onSelect"]),n(I,{show:e(x),"onUpdate:show":o[6]||(o[6]=a=>U(x)?x.value=a:null),class:"custom-card",preset:"card",title:"删除",size:"small",bordered:!1,style:{width:"300px"},segmented:{content:"soft",footer:"soft"}},{"header-extra":t(()=>[n(w,{class:"text-red",icon:"Trash"})]),footer:t(()=>[n(u,{justify:"center"},{default:t(()=>[n(i,{type:"info",onClick:o[5]||(o[5]=a=>x.value=!1)},{default:t(()=>[l(" 取消 ")]),_:1}),n(i,{type:"error",onClick:e(X)},{default:t(()=>[l(" 删除 ")]),_:1},8,["onClick"])]),_:1})]),default:t(()=>[n(u,{justify:"center"},{default:t(()=>[n(C,{value:e(R),"onUpdate:value":o[4]||(o[4]=a=>U(R)?R.value=a:null),round:!1,"rail-style":e(T)},{checked:t(()=>[l(" 删除文件 ")]),unchecked:t(()=>[l(" 保留文件 ")]),_:1},8,["value","rail-style"])]),_:1})]),_:1},8,["show"]),n(I,{show:e(h),"onUpdate:show":o[14]||(o[14]=a=>U(h)?h.value=a:null),class:"custom-card",preset:"card",title:"添加种子",size:"small",bordered:!1,style:{width:"300px"},segmented:{content:"soft",footer:"soft"},onBeforeLeave:L},{"header-extra":t(()=>[n(w,{class:"text-green",icon:"AddOutline"})]),footer:t(()=>[n(u,{justify:"center"},{default:t(()=>[n(i,{type:"info",onClick:L},{default:t(()=>[l(" 取消 ")]),_:1}),n(i,{type:"primary",onClick:ke},{default:t(()=>[l(" 下载 ")]),_:1})]),_:1})]),default:t(()=>[n(u,{vertical:""},{default:t(()=>[n($e,{ref_key:"addTorrentForm",ref:V,class:"site-form","inline-message":"","label-position":"top",size:"small",rules:e(fe),model:e(s),"show-label":!1,"status-icon":""},{default:t(()=>[n(v,{required:"",path:"urls"},{default:t(()=>[n(A,{value:e(s).urls,"onUpdate:value":o[7]||(o[7]=a=>e(s).urls=a),required:"",type:"textarea",placeholder:"种子链接"},null,8,["value"])]),_:1}),n(v,{label:"属性",path:"category"},{default:t(()=>[n(u,null,{default:t(()=>[n(C,{value:e(s).use_auto_torrent_management,"onUpdate:value":o[8]||(o[8]=a=>e(s).use_auto_torrent_management=a),round:!1,size:"small","rail-style":e(T)},{checked:t(()=>[l(" 自动管理 ")]),unchecked:t(()=>[l(" 手动管理 ")]),_:1},8,["value","rail-style"]),n(C,{value:e(s).is_paused,"onUpdate:value":o[9]||(o[9]=a=>e(s).is_paused=a),round:!1,size:"small","rail-style":e(T)},{unchecked:t(()=>[l(" 开始 ")]),checked:t(()=>[l(" 暂停 ")]),_:1},8,["value","rail-style"]),n(C,{value:e(s).is_skip_checking,"onUpdate:value":o[10]||(o[10]=a=>e(s).is_skip_checking=a),round:!1,size:"small","rail-style":e(T)},{checked:t(()=>[l(" 跳过校验 ")]),unchecked:t(()=>[l(" 正常校验 ")]),_:1},8,["value","rail-style"])]),_:1})]),_:1}),n(v,{label:"分类",path:"category"},{default:t(()=>[n(De,{value:e(s).category,"onUpdate:value":o[11]||(o[11]=a=>e(s).category=a),multiple:!1,options:e(_e),filterable:"",tag:e(z),placeholder:"分类/路径",size:"small"},null,8,["value","options","tag"])]),_:1}),n(v,{label:"下载限速",path:"download_limit"},{default:t(()=>[n(H,{value:e(s).download_limit,"onUpdate:value":o[12]||(o[12]=a=>e(s).download_limit=a),size:"small",placeholder:"下载限速：KB/S",step:"100",min:"0","button-placement":"both"},{prefix:t(()=>[l(" ↓ ")]),_:1},8,["value"])]),_:1}),n(v,{label:"上传限速",path:"upload_limit"},{default:t(()=>[n(H,{value:e(s).upload_limit,"onUpdate:value":o[13]||(o[13]=a=>e(s).upload_limit=a),size:"small",placeholder:"上传限速：KB/S",step:"100",min:"0","button-placement":"both"},{prefix:t(()=>[l(" ↑ ")]),_:1},8,["value"])]),_:1})]),_:1},8,["rules","model"])]),_:1})]),_:1},8,["show"])],64)}}});const St=Fe(st,[["__scopeId","data-v-990b2de4"]]);export{St as default};
