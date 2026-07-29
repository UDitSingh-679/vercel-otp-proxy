export default async function handler(req, res) {
  const { email, access_token } = req.query;
  if (!email) return res.status(400).json({ error: "email required" });
  if (!access_token) return res.status(400).json({ error: "access_token required" });

  try {
    const resp = await fetch(
      "https://chngemailcode48.vercel.app/send_otp?" +
      new URLSearchParams({ access_token, email })
    );
    const data = await resp.text();
    res.status(resp.status).send(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}
