// Yes/no for each setting the online checkout and its emails need. Shows
// only whether a setting exists, never its value.
module.exports = (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  const has = (k) => !!process.env[k];
  res.status(200).json({
    paymob: {
      secretKey: has('PAYMOB_SECRET_KEY'),
      publicKey: has('PAYMOB_PUBLIC_KEY'),
      cardIntegration: has('PAYMOB_INTEGRATION_ID'),
      applePayIntegration: has('PAYMOB_INTEGRATION_ID_APPLEPAY'),
      tamaraIntegration: has('PAYMOB_INTEGRATION_ID_TAMARA'),
      hmacSecret: has('PAYMOB_HMAC_SECRET'),
    },
    emails: { emailjsPrivateKey: has('EMAILJS_PRIVATE_KEY'), shopNotifyEmail: has('SHOP_NOTIFY_EMAIL') },
    orderStore: has('SUPABASE_URL') && has('SUPABASE_SERVICE_ROLE_KEY'),
    rewards: has('CRM_SUPABASE_SERVICE_ROLE_KEY'),
  });
};
