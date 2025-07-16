import { useState } from "react";
import Plot from "react-plotly.js";

export default function Home() {
  const [start, setStart] = useState({ x: 0, y: 0, z: -8 });
  const [goal,  setGoal]  = useState({ x: 10, y: 10, z: -8 });
  const [traj,  setTraj]  = useState([]);       // trajectory array
  const [waiting, setWaiting] = useState(false);

  // ------------- send request -------------
  const apiCall = async () => {
    setWaiting(true);
    const res = await fetch("/api/fly", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        start: Object.values(start),
        goal:  Object.values(goal)
      })
    });
    const js   = await res.json();
    setTraj(js.trajectory || []);
    setWaiting(false);
  };

  // ------------- numeric input component -------------
  const Num = ({ obj, setObj, k, prefix }) => (
    <input
      key={`${prefix}-${k}`}
      type="number"
      step="0.1"
      value={obj[k]}
      onChange={e => setObj({ ...obj, [k]: parseFloat(e.target.value) })}
      className="border p-2 rounded w-20 mr-1"
    />
  );

  // ------------- render -------------
  return (
    <main style={{ fontFamily: "sans-serif", padding: 32, maxWidth: 800 }}>
      <h1>UAV Point‑to‑Point Demo</h1>

      <div style={{ display: "flex", alignItems: "center", gap: 6, flexWrap: "wrap", marginBottom: 12 }}>
        <span>Start:</span>
        {["x","y","z"].map(k => <Num key={`s-${k}`} obj={start} setObj={setStart} k={k} prefix="s" />)}
        <span style={{ marginLeft: 12 }}>Goal:</span>
        {["x","y","z"].map(k => <Num key={`g-${k}`} obj={goal}  setObj={setGoal}  k={k} prefix="g" />)}
        <button
          onClick={apiCall}
          disabled={waiting}
          style={{ padding: "8px 16px", marginLeft: 12 }}
        >
          {waiting ? "Flying…" : "Send"}
        </button>
      </div>

      {/* ---- top‑down XY plot ---- */}
      {traj.length > 1 && (
        <Plot
          data={[
            {
              x: traj.map(p => p[0]),
              y: traj.map(p => p[1]),
              mode: "lines+markers",
              marker: { size: 4 },
              line: { shape: "spline" },
              name: "trajectory"
            }
          ]}
          layout={{
            title: "Top‑down XY path",
            xaxis: { title: "X (m)" },
            yaxis: { title: "Y (m)" },
            height: 400,
            autosize: true,
            margin: { t: 40, l: 40, r: 10, b: 40 }
          }}
          style={{ width: "100%" }}
          useResizeHandler
        />
      )}

      {/* raw JSON for debugging */}
      <pre style={{ background: "#111", color: "#0f0", padding: 12, maxHeight: 180, overflow: "auto" }}>
        {JSON.stringify(traj, null, 2)}
      </pre>
    </main>
  );
}
