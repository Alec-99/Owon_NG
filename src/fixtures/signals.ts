export type Profile = 'CKP inductief'|'PWM actuator'|'Lambda narrowband';
export type Capture = {source:'simulation'|'import'|'hardware';profile:Profile;sampleRate:number;samples:number[];capturedAt:string};
export function signal(profile:Profile,n=1200):Capture {const samples=Array.from({length:n},(_,i)=>{const t=i/n;if(profile==='CKP inductief')return Math.sin(t*2*Math.PI*12)*(Math.floor(t*60)%60<58?1:.15);if(profile==='PWM actuator')return (t*8%1)<.42?1:-.15;return .45+Math.sin(t*2*Math.PI*2)*.32});return {source:'simulation',profile,sampleRate:12000,samples,capturedAt:new Date(0).toISOString()}}
export function peakToPeak(x:number[]){return Math.max(...x)-Math.min(...x)}
