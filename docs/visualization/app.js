/**
 * Placeholder visualization app.
 * Next step: drop network.geojson + traj_*.json into ./data and this will animate.
 */
async function loadJSON(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Failed to load ${path}: ${res.status}`);
  return await res.json();
}

let map, roadsLayer, bridgesLayer;
let truckMarkers = new Map();
let scenarioIndex = null;
let currentScenario = null;
let t = 0;
let speed = 1;
let animHandle = null;
let isPlaying = false;

function lerp(a, b, u) { return a + (b - a) * u; }

function interpTimeline(timeline, t) {
  if (!timeline || timeline.length === 0) return null;
  if (t <= timeline[0][0]) return { lat: timeline[0][1], lon: timeline[0][2] };
  const last = timeline[timeline.length - 1];
  if (t >= last[0]) return { lat: last[1], lon: last[2] };
  for (let i = 0; i < timeline.length - 1; i++) {
    const a = timeline[i], b = timeline[i + 1];
    if (t >= a[0] && t <= b[0]) {
      const dt = (b[0] - a[0]) || 1;
      const u = (t - a[0]) / dt;
      return { lat: lerp(a[1], b[1], u), lon: lerp(a[2], b[2], u) };
    }
  }
  return null;
}

function initMap() {
  map = L.map("map", { preferCanvas: true }).setView([23.685, 90.3563], 7);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors"
  }).addTo(map);
}

function styleRoad(feature) {
  const isBridge = !!feature.properties?.is_bridge;
  const bridgeId = feature.properties?.bridge_id;
  const broken = currentScenario?.broken_bridges?.includes(bridgeId);
  if (isBridge) return { weight: 4, opacity: 0.9, color: broken ? "#e74c3c" : "#2ecc71" };
  return { weight: 2, opacity: 0.6, color: "#666" };
}

async function renderNetwork() {
  const network = await loadJSON("./data/network.geojson");
  if (roadsLayer) roadsLayer.remove();
  roadsLayer = L.geoJSON(network, { style: styleRoad }).addTo(map);
  try { map.fitBounds(roadsLayer.getBounds(), { padding: [20, 20] }); } catch {}
}

async function renderBridges() {
  try {
    const bridges = await loadJSON("./data/bridges.geojson");
    if (bridgesLayer) bridgesLayer.remove();
    bridgesLayer = L.geoJSON(bridges, {
      pointToLayer: (f, latlng) => {
        const id = f.properties?.bridge_id;
        const broken = currentScenario?.broken_bridges?.includes(id);
        return L.circleMarker(latlng, {
          radius: 6, weight: 1, opacity: 1, fillOpacity: 0.9,
          color: broken ? "#c0392b" : "#1e8449",
          fillColor: broken ? "#e74c3c" : "#2ecc71"
        });
      }
    }).addTo(map);
  } catch { /* optional */ }
}

function clearTrucks() {
  for (const m of truckMarkers.values()) m.remove();
  truckMarkers.clear();
}

function ensureTruckMarker(truckId, lat, lon) {
  if (truckMarkers.has(truckId)) return truckMarkers.get(truckId);
  const marker = L.circleMarker([lat, lon], {
    radius: 5, weight: 1, opacity: 1, fillOpacity: 0.9,
    color: "#1f77b4", fillColor: "#3498db"
  }).addTo(map);
  marker.bindTooltip(`Truck: ${truckId}`);
  truckMarkers.set(truckId, marker);
  return marker;
}

function updateTrucks() {
  if (!currentScenario) return;
  for (const tr of (currentScenario.trucks || [])) {
    const pos = interpTimeline(tr.timeline, t);
    if (!pos) continue;
    const marker = ensureTruckMarker(tr.truck_id, pos.lat, pos.lon);
    marker.setLatLng([pos.lat, pos.lon]);
  }
}

function tick() {
  if (!isPlaying || !currentScenario) return;
  const dt = 1 / 30;
  t += dt * speed;
  const end = currentScenario.t_end ?? 0;
  if (t > end) t = end;
  document.getElementById("timeVal").textContent = Math.floor(t);
  updateTrucks();
  if (t >= end) { pause(); return; }
  animHandle = requestAnimationFrame(tick);
}

function play() {
  if (!currentScenario) return;
  isPlaying = true;
  document.getElementById("playBtn").disabled = true;
  document.getElementById("pauseBtn").disabled = false;
  animHandle = requestAnimationFrame(tick);
}

function pause() {
  isPlaying = false;
  document.getElementById("playBtn").disabled = false;
  document.getElementById("pauseBtn").disabled = true;
  if (animHandle) cancelAnimationFrame(animHandle);
  animHandle = null;
}

async function loadScenario(file) {
  pause();
  t = 0;
  document.getElementById("timeVal").textContent = "0";

  currentScenario = await loadJSON(`./data/${file}`);

  const broken = (currentScenario.broken_bridges || []).join(", ") || "None";
  document.getElementById("scenarioMeta").innerHTML = `
    <div><b>Scenario:</b> ${currentScenario.scenario_name || file}</div>
    <div><b>Broken bridges:</b> ${broken}</div>
    <div><b>Duration:</b> ${currentScenario.t_end ?? "?"} s</div>
    <div><b>Trucks:</b> ${(currentScenario.trucks || []).length}</div>
  `;

  await renderNetwork();
  await renderBridges();

  clearTrucks();
  updateTrucks();
}

async function initUI() {
  scenarioIndex = await loadJSON("./data/scenarios.json");
  const select = document.getElementById("scenarioSelect");
  select.innerHTML = "";
  for (const s of scenarioIndex.scenarios) {
    const opt = document.createElement("option");
    opt.value = s.file;
    opt.textContent = s.label;
    select.appendChild(opt);
  }
  select.addEventListener("change", (e) => loadScenario(e.target.value));
  document.getElementById("playBtn").addEventListener("click", play);
  document.getElementById("pauseBtn").addEventListener("click", pause);

  const speedEl = document.getElementById("speed");
  const speedVal = document.getElementById("speedVal");
  speedEl.addEventListener("input", () => {
    speed = parseFloat(speedEl.value);
    speedVal.textContent = `${speed}×`;
  });

  await loadScenario(scenarioIndex.scenarios[0].file);
}

(async function main() {
  initMap();
  await initUI();
})();
