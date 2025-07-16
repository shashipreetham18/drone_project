export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Only POST requests allowed" });
  }

  const response = await fetch("http://127.0.0.1:5000/fly", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req.body),
  });

  if (!response.ok) {
    const errorText = await response.text();
    return res.status(500).json({ error: "Backend error", detail: errorText });
  }

  const data = await response.json();
  return res.status(200).json(data);
}
