const estado = document.getElementById('estado');
const parametros = new URLSearchParams(location.search);
const id = parametros.get('id') || sessionStorage.getItem('anaya-pago-id');
const clientTransactionId = parametros.get('clientTransactionId') || sessionStorage.getItem('anaya-pago-cliente');
if (id && clientTransactionId) {
  sessionStorage.setItem('anaya-pago-id', id);
  sessionStorage.setItem('anaya-pago-cliente', clientTransactionId);
}
// Remove identifiers from the address bar before the user navigates away.
history.replaceState(null, '', location.pathname);
async function confirmar() {
  if (!id || !clientTransactionId) throw new Error('No encontramos los datos del pago. Si realizaste el pago, contacta a la tienda.');
  const confirmationToken = sessionStorage.getItem(`anaya-pago-token:${clientTransactionId}`);
  if (!confirmationToken || !/^[0-9a-f]{64}$/.test(confirmationToken)) throw new Error('No encontramos la verificación de este pago. Contacta a la tienda para revisar tu pedido.');
  const configResponse = await fetch('../datos/pagos.json', { cache: 'no-store' });
  if (!configResponse.ok) throw new Error('No se pudo verificar el pago. Contacta a la tienda.');
  const config = await configResponse.json();
  if (!config.supabaseUrl || !config.anonKey || !/^https:\/\/[a-z0-9-]+\.supabase\.co$/.test(config.supabaseUrl)) throw new Error('La verificación no está disponible. Contacta a la tienda.');
  const respuesta = await fetch(`${config.supabaseUrl}/functions/v1/payment-confirm`, { method:'POST', headers:{'Content-Type':'application/json','apikey':config.anonKey}, body:JSON.stringify({id,clientTransactionId,confirmationToken}) });
  const resultado = await respuesta.json();
  if (resultado.status === 'paid' || resultado.status === 'cancelled') {
    sessionStorage.removeItem(`anaya-pago-token:${clientTransactionId}`);
    sessionStorage.removeItem('anaya-pago-id');
    sessionStorage.removeItem('anaya-pago-cliente');
  }
  if (resultado.status === 'paid') estado.textContent = 'Tu pago fue aprobado. Gracias por tu compra.';
  else if (resultado.status === 'cancelled') estado.textContent = 'El pago fue cancelado. Puedes volver al catálogo o contactarnos.';
  else if (resultado.status === 'processing') estado.textContent = 'Tu pago aún se está verificando. Contacta a la tienda para confirmar su estado.';
  else estado.textContent = 'No se pudo confirmar el pago automáticamente. Contacta a la tienda para revisar tu pedido.';
}
confirmar().catch((error) => { estado.textContent = error.message || 'No se pudo verificar el pago. Contacta a la tienda.'; });
