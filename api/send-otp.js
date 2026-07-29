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

  try {
    const resp = await fetch(
      "https://100067.connect.garena.com/game/account_security/bind:send_otp",
      {
        method: "POST",
        headers: {
          "User-Agent": "GarenaMSDK/4.0.19P9 (Android 9; en; US)",
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({ email, access_token, app_id: "100067", channel: "email" })
      }
    );
    const data = await resp.text();
    res.status(resp.status).send(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}
