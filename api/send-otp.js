export default async function handler(req, res) {
  const email = req.method === "POST" ? req.body?.email : req.query.email;
  if (!email) return res.status(400).json({ error: "email required" });

  try {
    const resp = await fetch(
      "https://sso-register-killersharmabot.vercel.app/send-email?" +
      new URLSearchParams({ email })
    );
    const data = await resp.text();
    res.status(resp.status).send(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}
