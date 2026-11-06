import {signal,type Capture,type Profile} from '../fixtures/signals';
export type State={page:string;profile:Profile;running:boolean;ch1:boolean;ch2:boolean;timeDiv:number;voltsDiv:number;zoom:number;cursor:number;capture:Capture;note:string};
export const state:State={page:'Automotive',profile:'CKP inductief',running:true,ch1:true,ch2:true,timeDiv:10,voltsDiv:1,zoom:1,cursor:.5,capture:signal('CKP inductief'),note:''};
const listeners=new Set<()=>void>();export function update(p:Partial<State>){Object.assign(state,p);if(p.profile)state.capture=signal(p.profile);listeners.forEach(f=>f())}export function subscribe(f:()=>void){listeners.add(f)}
