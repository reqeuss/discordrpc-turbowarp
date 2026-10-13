(function (Scratch) {
"use strict";
const URL = "ws://127.0.0.1:32123";
const defaults = {
 details:"", state:"", startTimestamp:"", endTimestamp:"",
 largeImageKey:"", largeImageText:"", smallImageKey:"", smallImageText:"",
 partyId:"", partySize:"", partyMax:"", joinSecret:"", spectateSecret:"", instance:"true"
};
const fields = [
 ["Details","details"],["State","state"],["Start timestamp (Unix seconds)","startTimestamp"],
 ["End timestamp (Unix seconds)","endTimestamp"],["Large image key","largeImageKey"],
 ["Large image text","largeImageText"],["Small image key","smallImageKey"],
 ["Small image text","smallImageText"],["Party ID","partyId"],["Party size","partySize"],
 ["Party maximum","partyMax"],["Join secret","joinSecret"],["Spectate secret","spectateSecret"],
 ["Instance (true/false)","instance"]
].map(([text,value])=>({text,value}));
class DiscordRPC {
 constructor(){this.fields={...defaults};this.ws=null;this.pending=null;this.timer=null;this.status="Disconnected";this.error="";this.stopped=false;this.connect();}
 getInfo(){return {id:"reqeussdiscordrpc",name:"Discord Rich Presence",color1:"#5865F2",color2:"#4752C4",color3:"#364099",blocks:[
 {opcode:"setField",blockType:Scratch.BlockType.COMMAND,text:"set [FIELD] to [VALUE]",arguments:{FIELD:{type:Scratch.ArgumentType.STRING,menu:"fields"},VALUE:{type:Scratch.ArgumentType.STRING,defaultValue:"Playing a game"}}},
 {opcode:"updatePresence",blockType:Scratch.BlockType.COMMAND,text:"update presence"},
 {opcode:"clearPresence",blockType:Scratch.BlockType.COMMAND,text:"clear presence"},
 {opcode:"reconnect",blockType:Scratch.BlockType.COMMAND,text:"reconnect to bridge"},
 {opcode:"connectionStatus",blockType:Scratch.BlockType.REPORTER,text:"RPC connection status"},
 {opcode:"getField",blockType:Scratch.BlockType.REPORTER,text:"current value of [FIELD]",arguments:{FIELD:{type:Scratch.ArgumentType.STRING,menu:"fields"}}}
 ],menus:{fields:{acceptReporters:false,items:fields}}};}
 connect(){
  if(this.stopped||this.ws&&(this.ws.readyState===WebSocket.OPEN||this.ws.readyState===WebSocket.CONNECTING))return;
  this.status="Connecting to bridge";
  try{const ws=new WebSocket(URL);this.ws=ws;
   ws.onopen=()=>{if(this.ws!==ws)return;this.status="Bridge connected";this.error="";if(this.pending){const p=this.pending;this.pending=null;this.send(p);}};
   ws.onmessage=e=>{try{const m=JSON.parse(String(e.data));if(m.type==="status")this.status=String(m.status||this.status);if(m.type==="ack"&&!m.ok)this.error=String(m.error||"Bridge rejected update");}catch(_){}};
   ws.onerror=()=>{if(this.ws===ws){this.status="Bridge connection error";this.error="Check that the Python bridge is running.";}};
   ws.onclose=()=>{if(this.ws===ws)this.ws=null;if(!this.stopped){this.status="Bridge disconnected";this.schedule();}};
  }catch(e){this.error=String(e);this.status="WebSocket unavailable";this.schedule();}
 }
 schedule(){if(this.stopped||this.timer!==null)return;this.timer=setTimeout(()=>{this.timer=null;this.connect();},2000);}
 reconnect(){this.error="";if(this.timer!==null)clearTimeout(this.timer);this.timer=null;if(this.ws){try{this.ws.close();}catch(_){}this.ws=null;}this.connect();}
 setField(a){const k=String(a.FIELD||"");if(Object.prototype.hasOwnProperty.call(this.fields,k))this.fields[k]=String(a.VALUE??"").slice(0,256);}
 getField(a){const k=String(a.FIELD||"");return Object.prototype.hasOwnProperty.call(this.fields,k)?this.fields[k]:"";}
 clean(v){const s=String(v??"").trim();return s||null;}
 num(v){const s=String(v??"").trim();if(!s)return null;const n=Number(s);return Number.isFinite(n)?Math.trunc(n):null;}
 payload(){const f=this.fields;const i=String(f.instance).trim().toLowerCase();return {action:"update",details:this.clean(f.details),state:this.clean(f.state),start:this.num(f.startTimestamp),end:this.num(f.endTimestamp),largeImage:this.clean(f.largeImageKey),largeText:this.clean(f.largeImageText),smallImage:this.clean(f.smallImageKey),smallText:this.clean(f.smallImageText),partyId:this.clean(f.partyId),partySize:this.num(f.partySize),partyMax:this.num(f.partyMax),joinSecret:this.clean(f.joinSecret),spectateSecret:this.clean(f.spectateSecret),instance:!["false","0","no","off"].includes(i)};}
 send(p){if(!this.ws||this.ws.readyState!==WebSocket.OPEN){this.pending=p;this.status="Waiting for bridge";this.connect();return false;}try{this.ws.send(JSON.stringify(p));this.status="Update sent to bridge";return true;}catch(e){this.pending=p;this.error=String(e);this.status="Send failed";return false;}}
 updatePresence(){const p=this.payload();this.pending=p;if(this.ws&&this.ws.readyState===WebSocket.OPEN){this.pending=null;this.send(p);}else{this.connect();this.status="Update queued";}}
 clearPresence(){this.pending=null;this.send({action:"clear"});}
 connectionStatus(){return this.error?this.status+" — "+this.error:this.status;}
}
Scratch.extensions.register(new DiscordRPC());
})(Scratch);
