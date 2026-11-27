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
$('logout').addEventListener('click',async()=>{await supabase.auth.signOut();msg('Sesión cerrada.');await render()});
$('refresh').addEventListener('click',render);
render();
