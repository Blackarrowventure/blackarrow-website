// Website Supabase (orders, customer accounts), server side only.
async function db(method, path, body, prefer) {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) throw new Error('supabase_not_configured');
  const headers = { apikey: key, Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' };
  if (prefer) headers.Prefer = prefer;
  const r = await fetch(url + '/rest/v1/' + path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  const text = await r.text();
  if (!r.ok) {
    const e = new Error('supabase_' + r.status);
    e.body = text.slice(0, 300);
    throw e;
  }
  return text ? JSON.parse(text) : null;
}

// Inserts an order row. If the newer columns (details, ...) are not in the
// table yet, retries without them so checkout keeps working either way.
async function insertOrder(table, row, extra) {
  try {
    return await db('POST', table, Object.assign({}, row, extra), 'return=minimal');
  } catch (e) {
    if (extra && /column|schema cache/i.test(e.body || '')) {
      console.error(table + ': newer columns missing, run supabase/3d-order-details.sql');
      return db('POST', table, row, 'return=minimal');
    }
    throw e;
  }
}

// The signed-in website customer behind a browser access token, or null.
async function websiteUser(token) {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!token || !url || !key || typeof token !== 'string' || token.length > 4000) return null;
  const r = await fetch(url + '/auth/v1/user', { headers: { apikey: key, Authorization: 'Bearer ' + token } });
  if (!r.ok) return null;
  const u = await r.json().catch(() => null);
  return u && u.id ? u : null;
}

function bearer(req) {
  const h = String((req.headers && (req.headers.authorization || req.headers.Authorization)) || '');
  return h.startsWith('Bearer ') ? h.slice(7).trim() : '';
}

module.exports = { db, insertOrder, websiteUser, bearer };
