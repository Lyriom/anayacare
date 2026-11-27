import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.119.2';
import {config} from './config.js';
const $ = (id) => document.getElementById(id);
const supabase = createClient(config.url,config.anonKey);
const msg = (s) => $('message').textContent = s;
const money = cents => new Intl.NumberFormat('es-EC',{style:'currency',currency:'USD'}).format(cents/100);
async function render(){
 const {data:{session}}=await supabase.auth.getSession();
 $('login').hidden=!!session; $('dashboard').hidden=!session; $('logout').hidden=!session;
 if(!session)return;
 const {data,error}=await supabase.from('orders').select('created_at,customer_name,customer_email,customer_phone,total_cents,status,order_items(name,unit_cents,quantity)').order('created_at',{ascending:false}).limit(100);
 if(error){msg('No tienes acceso o no se pudieron cargar los pedidos.');return;}
 $('orders').replaceChildren();
 for(const o of data){
  const tr=document.createElement('tr');
  for(const value of [new Date(o.created_at).toLocaleString('es-EC'),o.customer_name,`${o.customer_email} · ${o.customer_phone}`,money(o.total_cents),({pending:'Pendiente',confirming:'Verificando',paid:'Pagado',cancelled:'Cancelado',needs_review:'Por revisar'})[o.status]||o.status]){
   const td=document.createElement('td');td.textContent=value;tr.append(td);
  }
  const cell=document.createElement('td');
  const details=document.createElement('details');
  const summary=document.createElement('summary');summary.textContent='Ver productos';details.append(summary);
  const items=document.createElement('ul');items.className='order-items';
  for(const item of o.order_items || []){
   const li=document.createElement('li');
   li.textContent=`${item.quantity} × ${item.name} · ${money(item.unit_cents)} c/u · ${money(item.unit_cents * item.quantity)}`;
   items.append(li);
  }
  if(!items.childElementCount){const li=document.createElement('li');li.textContent='No hay detalles disponibles.';items.append(li);}
  details.append(items);cell.append(details);tr.append(cell);$('orders').append(tr);
 }
 msg(data.length?'':'Aún no hay pedidos.');
}
$('form').addEventListener('submit',async e=>{e.preventDefault();msg('Ingresando…');const {error}=await supabase.auth.signInWithPassword({email:$('email').value,password:$('password').value});$('password').value='';if(error){msg('No se pudo iniciar sesión. Revisa tus datos.');return}msg('');await render()});
$('logout').addEventListener('click',async()=>{$('password-form').reset();$('password-message').textContent='';await supabase.auth.signOut();msg('Sesión cerrada.');await render()});
$('password-form').addEventListener('submit',async e=>{
 e.preventDefault();
 const password=$('new-password').value, confirmation=$('confirm-password').value, notice=$('password-message'), button=$('change-password');
 if(password!==confirmation){notice.textContent='Las contraseñas no coinciden.';$('confirm-password').focus();return;}
 if(password.length<12 || password.length>72){notice.textContent='La contraseña debe tener entre 12 y 72 caracteres.';$('new-password').focus();return;}
 button.disabled=true;notice.textContent='Actualizando contraseña…';
 try{
  const {error}=await supabase.auth.updateUser({password});
  if(error){notice.textContent='No se pudo cambiar la contraseña. Inicia sesión de nuevo e inténtalo otra vez.';return;}
  $('password-form').reset();notice.textContent='Tu contraseña se actualizó correctamente.';
 }catch{notice.textContent='No se pudo cambiar la contraseña. Comprueba tu conexión e inténtalo de nuevo.';}
 finally{button.disabled=false;}
});
$('refresh').addEventListener('click',render);
render();
