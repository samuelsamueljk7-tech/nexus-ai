let listening=false, thinking=false, talking=false;
const $=id=>document.getElementById(id);
const app=$('app'), character=$('characterContainer'), status=$('status'), subtitle=$('subtitle'), response=$('response'), micButton=$('micButton'), stateToast=$('toast');
const commandForm=$('commandForm'), commandInput=$('commandInput');

function toast(message){stateToast.textContent=message;stateToast.classList.add('show');clearTimeout(window.__toast);window.__toast=setTimeout(()=>stateToast.classList.remove('show'),2200)}
function setCharacterState(s){character.dataset.state=s;app.dataset.state=s;}
function startThinking(){thinking=true;talking=false;setCharacterState('thinking');status.textContent='Thinking…';subtitle.textContent='NEXUS is processing your request.';$('eyebrow').textContent='NEXUS CORE';}
function showAIResponse(message){listening=false;thinking=false;talking=true;setCharacterState('talking');status.textContent='NEXUS';subtitle.textContent='Your request is complete.';response.textContent=message;$('eyebrow').textContent='SPARK RESPONSE';}
function returnToIdle(){talking=false;thinking=false;setCharacterState('idle');status.textContent="Hey, I'm NEXUS.";subtitle.textContent='Your AI assistant is ready.';response.textContent='';$('eyebrow').textContent='YOUR AI ASSISTANT';}

async function sendSparkCommand(text){text=String(text||'').trim();if(!text)return;startThinking();commandInput.value='';try{const res=await fetch('/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({command:text})});const data=await res.json();if(!res.ok||!data.success)throw new Error(data.response||'NEXUS command failed.');showAIResponse(data.response||'Done.');if('speechSynthesis' in window&&data.response){speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(data.response);u.rate=1.02;u.pitch=1;u.onend=()=>setTimeout(returnToIdle,500);speechSynthesis.speak(u)}else setTimeout(returnToIdle,2400)}catch(e){console.error(e);showAIResponse(e.message||'I could not complete that command.');toast(e.message||'NEXUS error');setTimeout(returnToIdle,2200)}}
commandForm.addEventListener('submit',e=>{e.preventDefault();sendSparkCommand(commandInput.value)});

document.querySelectorAll('.quick-actions button').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('.quick-actions button').forEach(x=>x.classList.remove('active'));btn.classList.add('active');sendSparkCommand(btn.dataset.command);setTimeout(()=>btn.classList.remove('active'),1000)}));

let recognition=null;
if('SpeechRecognition' in window||'webkitSpeechRecognition' in window){const R=window.SpeechRecognition||window.webkitSpeechRecognition;recognition=new R();recognition.lang='en-US';recognition.interimResults=false;recognition.continuous=false;recognition.onresult=e=>sendSparkCommand(e.results[0][0].transcript);recognition.onerror=e=>{console.error(e);listening=false;setCharacterState('idle');toast('Microphone unavailable or permission denied.');};recognition.onend=()=>{listening=false;if(!thinking&&!talking)returnToIdle()}}
function startListening(){if(!recognition){commandInput.focus();toast('Use the text field — browser speech recognition is unavailable.');return}if(listening)return;listening=true;setCharacterState('listening');$('eyebrow').textContent='LISTENING';status.textContent="I'm listening…";subtitle.textContent='Tell me what you need.';response.textContent='';try{recognition.start()}catch(e){}}
function stopListening(){if(recognition)try{recognition.stop()}catch(e){}listening=false}
micButton.addEventListener('click',()=>listening?stopListening():startListening());

document.addEventListener('keydown',e=>{if(e.code==='Space'&&!e.repeat&&!['INPUT','TEXTAREA'].includes(document.activeElement.tagName)){e.preventDefault();listening?stopListening():startListening()}if(e.key==='Escape')returnToIdle();if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();commandInput.focus()}});
$('settingsButton').addEventListener('click',()=>toast('NEXUS settings are coming soon.'));

/* login */
const loginScreen=$('loginScreen'),loginForm=$('loginForm'),loginEmail=$('loginEmail'),loginPassword=$('loginPassword'),loginMessage=$('loginMessage');
function openSparkSession(label=''){loginScreen.classList.add('hidden');if(label){setTimeout(()=>{status.textContent=`Welcome to NEXUS, ${label}.`;subtitle.textContent='Your AI assistant is ready.'},450)}}
function loginUser(email){const remember=$('rememberMe').checked;(remember?localStorage:sessionStorage).setItem('spark_session','1');(remember?localStorage:sessionStorage).setItem('spark_user',email);openSparkSession(email.split('@')[0])}
loginForm.addEventListener('submit',e=>{e.preventDefault();if(!loginEmail.value.trim()||!loginPassword.value){loginMessage.textContent='Enter your email and password.';return}loginMessage.textContent='Opening local NEXUS session…';setTimeout(()=>loginUser(loginEmail.value.trim()),300)});
$('guestButton').addEventListener('click',()=>{sessionStorage.setItem('spark_session','1');sessionStorage.setItem('spark_user','Guest');loginMessage.textContent='Opening guest NEXUS session…';setTimeout(()=>openSparkSession('Guest'),250)});
$('passwordToggle').addEventListener('click',()=>{const hidden=loginPassword.type==='password';loginPassword.type=hidden?'text':'password';$('passwordToggle').textContent=hidden?'HIDE':'SHOW'});
$('forgotButton').addEventListener('click',()=>loginMessage.textContent='Password recovery will be connected to your NEXUS account service.');
$('logoutButton').addEventListener('click',()=>{localStorage.removeItem('spark_session');localStorage.removeItem('spark_user');sessionStorage.removeItem('spark_session');sessionStorage.removeItem('spark_user');loginScreen.classList.remove('hidden');loginForm.reset();loginMessage.textContent='';loginPassword.type='password';$('passwordToggle').textContent='SHOW';returnToIdle()});
window.addEventListener('load',()=>{setCharacterState('idle');if(localStorage.getItem('spark_session')==='1'||sessionStorage.getItem('spark_session')==='1')openSparkSession()});
