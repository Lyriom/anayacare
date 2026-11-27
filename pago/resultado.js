const estado = document.getElementById('estado');
const parametros = new URLSearchParams(location.search);
const id = parametros.get('id');
const clientTransactionId = parametros.get('clientTransactionId');
// Remove identifiers from the address bar before the user navigates away.
history.replaceState(null, '', location.pathname);
async function confirmar() {
  if (!id || !clientTransactionId) throw new Error('No encontramos los datos del pago. Si realizaste el pago, contacta a la tienda.');
  const configResponse = await fetch('../datos/pagos.json', { cache: 'no-store' });
  if (!configResponse.ok) throw new Error('No se pudo verificar el pago. Contacta a la tienda.');
  const config = await configResponse.json();
  if (!config.supabaseUrl || !config.anonKey || !/^https:\/\/[a-z0-9-]+\.supabase\.co$/.test(config.supabaseUrl)) throw new Error('La verificación no está disponible. Contacta a la tienda.');
  const respuesta = await fetch(`${config.supabaseUrl}/functions/v1/payment-confirm`, { method:'POST', headers:{'Content-Type':'application/json','apikey':config.anonKey}, body:JSON.stringify({id,clientTransactionId}) });
  const resultado = await respuesta.json();
  if (resultado.status === 'paid') estado.textContent = 'Tu pago fue aprobado. Gracias por tu compra.';
  else if (resultado.status === 'cancelled') estado.textContent = 'El pago fue cancelado. Puedes volver al catálogo o contactarnos.';
  else if (resultado.status === 'processing') estado.textContent = 'Tu pago aún se está verificando. Contacta a la tienda para confirmar su estado.';
  else estado.textContent = 'No se pudo confirmar el pago automáticamente. Contacta a la tienda para revisar tu pedido.';
}
confirmar().catch((error) => { estado.textContent = error.message || 'No se pudo verificar el pago. Contacta a la tienda.'; });
