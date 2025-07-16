export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Only POST requests allowed" });
  }


  const isDemo =
    process.env.VERCEL ||             
    process.env.NEXT_PUBLIC_DEMO === "true";

  if (isDemo) {
    
    const mock = {
      trajectory: [
        [0, 0, -8],
        [3, 2, -8],
        [6, 4, -8],
        [10, 8, -8]
      ],
      status: "demo"
    };
    return res.status(200).json(mock);
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/fly", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body)
    });

    if (!response.ok) {
      const errorText = await response.text();
      return res.status(500).json({ error: "Backend error", detail: errorText });
    }

    const data = await response.json();
    return res.status(200).json(data);
  } catch (e) {
    return res.status(500).json({ error: "Could not reach backend", detail: e.message });
  }
}
