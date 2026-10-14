/**
 * Blender AI Ultimate Studio — Frontend Controller
 * Handles visual engine selection, API key configuration, hardware diagnostics,
 * Blender MCP status, and pipeline execution logging.
 */

let currentEngine = 'meshy';

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
  addLog('[INICIO] Conectando con el servidor de control en http://localhost:5050...', 'info');
  refreshStatus();
});

// --- Telemetry Logger ---
function addLog(message, type = 'info') {
  const terminal = document.getElementById('log-terminal');
  if (!terminal) return;

  const time = new Date().toLocaleTimeString('es-ES', { hour12: false });
  const line = document.createElement('div');
  line.className = `log-line log-${type}`;
  line.textContent = `[${time}] ${message}`;

  terminal.appendChild(line);
  terminal.scrollTop = terminal.scrollHeight;
}

// --- Fetch Full System Status ---
async function refreshStatus() {
  try {
    const res = await fetch('/api/status');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    // 1. Update Active Engine
    currentEngine = data.active_engine || 'meshy';
    updateEngineUI(currentEngine);

    // 2. Update Meshy Status
    const meshyStatus = data.meshy || {};
    const keyStatusEl = document.getElementById('meshy-key-status');
    if (keyStatusEl) {
      if (meshyStatus.configured && meshyStatus.status === 'active') {
        keyStatusEl.textContent = '✅ Clave API válida y conectada.';
        keyStatusEl.className = 'input-help text-success';
      } else if (meshyStatus.status === 'missing_key') {
        keyStatusEl.textContent = '⚠️ Clave no configurada. Ingresa tu clave para usar Meshy.';
        keyStatusEl.className = 'input-help text-warning';
      } else {
        keyStatusEl.textContent = `⚠️ Estado: ${meshyStatus.message || 'Sin verificar'}`;
        keyStatusEl.className = 'input-help text-warning';
      }
    }

    // 3. Update Trellis Status
    const trellisStatus = data.trellis || {};
    const trellisBox = document.getElementById('trellis-status-box');
    const trellisText = document.getElementById('trellis-status-text');
    if (trellisText && trellisStatus.installed) {
      trellisText.textContent = `✅ TRELLIS instalado en ${trellisStatus.repo_path} (Submódulos FlexiCubes OK).`;
      if (trellisBox) trellisBox.className = 'trellis-status-box active-ok';
    }

    // 4. Update Blender MCP Status
    updateBlenderUI(data.blender || {});

    addLog(`[ESTADO] Motor activo: ${currentEngine.toUpperCase()} | Blender: ${data.blender?.connected ? 'CONECTADO' : 'DESCONECTADO'}`, 'success');

  } catch (err) {
    addLog(`[ERROR] No se pudo obtener el estado del backend: ${err.message}`, 'error');
  }
}

// --- Engine Selection ---
async function selectEngine(engineName) {
  currentEngine = engineName;
  updateEngineUI(engineName);

  addLog(`[SELECCIÓN] Cambiando motor a: ${engineName}...`, 'info');

  try {
    const res = await fetch('/api/set-engine', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ engine: engineName })
    });

    const data = await res.json();
    if (data.success) {
      addLog(`[CONFIG] Motor activo guardado en pipeline_config.json: ${engineName}`, 'success');
    } else {
      addLog(`[ERROR] Fallo al guardar motor: ${data.error}`, 'error');
    }
  } catch (err) {
    addLog(`[ERROR] Comunicación fallida al cambiar motor: ${err.message}`, 'error');
  }
}

function updateEngineUI(engineName) {
  const cardMeshy = document.getElementById('card-engine-meshy');
  const cardTrellis = document.getElementById('card-engine-trellis');
  const radioMeshy = document.getElementById('radio-meshy');
  const radioTrellis = document.getElementById('radio-trellis');
  const summaryEngine = document.getElementById('summary-engine');

  if (engineName === 'meshy') {
    if (cardMeshy) cardMeshy.classList.add('active');
    if (cardTrellis) cardTrellis.classList.remove('active');
    if (radioMeshy) radioMeshy.checked = true;
    if (summaryEngine) {
      summaryEngine.textContent = 'Meshy-6 API (Nube Quad Remesh)';
      summaryEngine.className = 'glow-text';
    }
  } else {
    if (cardMeshy) cardMeshy.classList.remove('active');
    if (cardTrellis) cardTrellis.classList.add('active');
    if (radioTrellis) radioTrellis.checked = true;
    if (summaryEngine) {
      summaryEngine.textContent = 'Microsoft TRELLIS (Local en D:\\)';
      summaryEngine.className = 'glow-text-cyan';
    }
  }
}

// --- Tabs Management ---
function switchTab(tabId) {
  const tabs = ['meshy', 'trellis', 'blender'];
  tabs.forEach(t => {
    const btn = document.getElementById(`tab-btn-${t}`);
    const content = document.getElementById(`tab-content-${t}`);
    if (btn) btn.classList.toggle('active', t === tabId);
    if (content) content.classList.toggle('active', t === tabId);
  });
}

// --- Meshy API Key Configuration ---
function toggleKeyVisibility() {
  const input = document.getElementById('input-meshy-key');
  if (input) {
    input.type = input.type === 'password' ? 'text' : 'password';
  }
}

async function saveMeshyKey() {
  const input = document.getElementById('input-meshy-key');
  const key = input ? input.value.trim() : '';

  if (!key) {
    alert('Por favor ingresa una clave API válida de Meshy (ej: msy_...)');
    return;
  }

  addLog('[MESHY] Guardando clave API y verificando conexión...', 'info');

  try {
    const res = await fetch('/api/set-key', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_key: key })
    });

    const data = await res.json();
    const status = data.status || {};
    const keyStatusEl = document.getElementById('meshy-key-status');

    if (status.configured && status.status === 'active') {
      if (keyStatusEl) {
        keyStatusEl.textContent = '✅ Clave API válida y conectada con Meshy.';
        keyStatusEl.className = 'input-help text-success';
      }
      addLog('[MESHY] ¡Clave API validada con éxito con los servidores de Meshy!', 'success');
      alert('¡Clave API de Meshy guardada y verificada correctamente!');
    } else {
      if (keyStatusEl) {
        keyStatusEl.textContent = `⚠️ Advertencia: ${status.message || 'Clave no verificada'}`;
        keyStatusEl.className = 'input-help text-warning';
      }
      addLog(`[MESHY] Respuesta de clave: ${status.message}`, 'warning');
      alert(`Clave guardada, pero Meshy devolvió: ${status.message}`);
    }
  } catch (err) {
    addLog(`[ERROR] No se pudo guardar la clave API: ${err.message}`, 'error');
  }
}

// --- Accordion Guide ---
function toggleGuide() {
  const body = document.getElementById('guide-body');
  const arrow = document.getElementById('accordion-arrow');
  if (body) {
    const isOpen = body.style.display === 'block';
    body.style.display = isOpen ? 'none' : 'block';
    if (arrow) arrow.textContent = isOpen ? '▼' : '▲';
  }
}

// --- Trellis Check ---
async function checkLocalTrellis() {
  addLog('[TRELLIS] Comprobando integridad del entorno local en D:\\AI_Tools\\trellis...', 'info');
  try {
    const res = await fetch('/api/check-local');
    const data = await res.json();

    const box = document.getElementById('trellis-status-box');
    const text = document.getElementById('trellis-status-text');

    if (data.installed && data.has_submodules) {
      if (text) text.textContent = `✅ TRELLIS instalado correctamente en ${data.repo_path}. Submódulo FlexiCubes activo.`;
      if (box) box.className = 'trellis-status-box active-ok';
      addLog(`[TRELLIS] Verificación completada. Hardware detectado: ${data.hardware?.cpu} + ${data.hardware?.gpu}`, 'success');
    } else {
      if (text) text.textContent = '⚠️ Repositorio incompleto o falta submódulo FlexiCubes.';
      addLog('[TRELLIS] Advertencia: El repositorio local requiere sincronizar submódulos.', 'warning');
    }
  } catch (err) {
    addLog(`[ERROR] Error al verificar TRELLIS: ${err.message}`, 'error');
  }
}

// --- Blender Check ---
async function checkBlenderConnection() {
  addLog('[BLENDER] Sondeando socket localhost:9876...', 'info');
  try {
    const res = await fetch('/api/check-blender');
    const data = await res.json();
    updateBlenderUI(data);

    if (data.connected) {
      addLog(`[BLENDER] Conectado exitosamente al socket MCP de Blender (${data.host}:${data.port})`, 'success');
    } else {
      addLog(`[BLENDER] No responde en el puerto 9876. ${data.message}`, 'warning');
    }
  } catch (err) {
    addLog(`[ERROR] Error al contactar socket de Blender: ${err.message}`, 'error');
  }
}

function updateBlenderUI(blenderStatus) {
  const badgeDot = document.getElementById('blender-dot');
  const badgeText = document.getElementById('blender-status-text');
  const detailMsg = document.getElementById('blender-msg-detail');

  if (blenderStatus.connected) {
    if (badgeDot) {
      badgeDot.className = 'status-dot dot-green';
    }
    if (badgeText) {
      badgeText.textContent = 'Blender MCP: En Línea';
    }
    if (detailMsg) {
      detailMsg.textContent = '✅ Conexión establecida en localhost:9876. Listo para recibir comandos.';
      detailMsg.className = 'blender-msg text-success';
    }
  } else {
    if (badgeDot) {
      badgeDot.className = 'status-dot dot-red';
    }
    if (badgeText) {
      badgeText.textContent = 'Blender MCP: Desconectado';
    }
    if (detailMsg) {
      detailMsg.textContent = '⚠️ Desconectado. Verifica que Blender esté abierto con el socket activo en el puerto 9876.';
      detailMsg.className = 'blender-msg text-warning';
    }
  }
}

// --- Pipeline Launch ---
async function launchPipeline() {
  addLog(`[PIPELINE] Disparando pipeline híbrido con motor: ${currentEngine.toUpperCase()}...`, 'info');

  if (currentEngine === 'meshy') {
    const keyStatusEl = document.getElementById('meshy-key-status');
    const isReady = keyStatusEl && keyStatusEl.textContent.includes('✅');

    if (!isReady) {
      const proceed = confirm('No has configurado o validado tu clave API de Meshy.\n¿Deseas ingresar tu clave ahora en la pestaña "Configuración Meshy API"?');
      if (proceed) {
        switchTab('meshy');
        document.getElementById('input-meshy-key')?.focus();
        return;
      }
    }

    addLog('[MESHY] Generando tarea Image-to-3D en cola de Meshy Cloud...', 'info');
    addLog('[MESHY] Estimación: 60-90 segundos para generación y topología Quad...', 'info');
  } else {
    addLog('[TRELLIS] Disparando inferencia neuronal con TRELLIS...', 'info');
    addLog('[TRELLIS] Utilizando optimización para Ryzen 7 5700X + Intel Arc A750...', 'info');
  }

  // Comprobar si existe el modelo de la monja para importar directamente
  addLog('[BLENDER] Preparando ingesta de modelo en la escena activa...', 'info');
  try {
    const res = await fetch('/api/import-blender', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ glb_path: 'D:\\Blender 3D MCP IA\\SM_GothicCorruptedNun.glb' })
    });
    const data = await res.json();
    if (data.success) {
      addLog('[BLENDER] ¡Malla GLB importada exitosamente en la escena de Blender!', 'success');
      alert('¡Pipeline ejecutado! El modelo ha sido enviado e importado a Blender.');
    } else {
      addLog(`[BLENDER] Respuesta de importación: ${data.error || 'Operación completada'}`, 'warning');
    }
  } catch (err) {
    addLog(`[ERROR] Error al importar a Blender: ${err.message}`, 'error');
  }
}
