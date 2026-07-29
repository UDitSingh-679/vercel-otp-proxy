export default async function handler(req, res) {
  let email, access_token;

  if (req.method === "POST") {
    email = req.body?.email;
    access_token = req.body?.access_token;
  } else {
    email = req.query.email;
    access_token = req.query.access_token;
  }

  if (!email) return res.status(400).json({ error: "email required" });
  if (!access_token) return res.status(400).json({ error: "access_token required" });

  const results = [];

  // Approach 1: GET with query params
  try {
    const r1 = await fetch(
      "https://100067.connect.garena.com/game/account_security/bind:send_otp?" +
      new URLSearchParams({ access_token, email, app_id: "100067", channel: "email" }),
      { headers: { "User-Agent": "GarenaMSDK/4.0.19P9 (Android 9; en; US)" } }
    );
    results.push({ method: "GET", status: r1.status, body: await r1.text() });
  } catch (e) { results.push({ method: "GET", error: e.message }); }

  // Approach 2: POST JSON with access_token in body
  try {
    const r2 = await fetch(
      "https://100067.connect.garena.com/game/account_security/bind:send_otp",
      {
        method: "POST",
        headers: { "User-Agent": "GarenaMSDK/4.0.19P9 (Android 9; en; US)", "Content-Type": "application/json" },
        body: JSON.stringify({ email, access_token, app_id: 100067, channel: "email" })
      }
    );
    results.push({ method: "POST_JSON", status: r2.status, body: await r2.text() });
  } catch (e) { results.push({ method: "POST_JSON", error: e.message }); }

  // Approach 3: POST x-www-form-urlencoded
  try {
    const r3 = await fetch(
      "https://100067.connect.garena.com/game/account_security/bind:send_otp",
      {
        method: "POST",
        headers: { "User-Agent": "GarenaMSDK/4.0.19P9 (Android 9; en; US)", "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ email, access_token, app_id: "100067", channel: "email" })
      }
    );
    results.push({ method: "POST_FORM", status: r3.status, body: await r3.text() });
  } catch (e) { results.push({ method: "POST_FORM", error: e.message }); }

  res.json(results);
}
