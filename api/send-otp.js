export default async function handler(req, res) {
  const { email } = req.query;
  if (!email) return res.status(400).json({ error: "email required" });

  try {
    const resp = await fetch(
      "https://100067.connect.garena.com/game/account_security/bind:send_otp",
      {
        method: "POST",
        headers: {
          "User-Agent": "GarenaMSDK/4.0.19P9 (Android 9; en; US)",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, app_id: 100067, channel: "email" })
      }
    );
    const data = await resp.text();
    res.status(resp.status).send(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}
