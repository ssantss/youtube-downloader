<script>
  import { onMount } from 'svelte';
  import { addDownload } from '../stores/downloads';
  
  let url = '';
  let message = 'Ingresa una URL de YouTube';
  let isLoading = false;
  let isValidUrl = false;
  let videoInfo = null;

  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
  console.log(BACKEND_URL);
  const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$/;

  $: isValidUrl = youtubeRegex.test(url);

  async function pasteFromClipboard() {
    try {
      const text = await navigator.clipboard.readText();
      url = text;
      validateUrl(text);
    } catch (err) {
      message = 'Error al acceder al portapapeles';
    }
  }

  async function getVideoInfo(videoUrl) {
    try {
      const response = await fetch(`https://www.youtube.com/oembed?url=${videoUrl}&format=json`);
      const data = await response.json();
      return {
        title: data.title,
        author: data.author_name,
        thumbnail: data.thumbnail_url
      };
    } catch (error) {
      console.error('Error obteniendo info del video:', error);
      return null;
    }
  }

  async function validateUrl(value) {
    if (!value) {
      message = 'Ingresa una URL de YouTube';
      videoInfo = null;
      return;
    }
    if (!youtubeRegex.test(value)) {
      message = 'URL inválida. Debe ser un enlace de YouTube';
      videoInfo = null;
      return;
    }
    
    videoInfo = await getVideoInfo(value);
    message = videoInfo ? 'URL válida' : 'No se pudo obtener información del video';
  }

  async function handleSubmit() {
    if (!isValidUrl) {
      message = 'Por favor ingresa una URL válida de YouTube';
      return false;
    }

    isLoading = true;
    message = 'Descargando video';

    try {
      const response = await fetch(`${BACKEND_URL}/download/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url })
      });
      
      if (!response.ok) {
        throw new Error('Error en la descarga');
      }

      message = 'Procesando video';

      const contentDisposition = response.headers.get('content-disposition');
      const filename = contentDisposition
        ? contentDisposition.includes('filename*=UTF-8')
          ? decodeURIComponent(contentDisposition.split('filename*=UTF-8\'\'')[1])
          : decodeURIComponent(contentDisposition.split('filename=')[1].replace(/["']/g, ''))
        : 'video.mp4';

      const blob = await response.blob();
      
      if (!blob.size) {
        throw new Error('Archivo descargado inválido');
      }

      message = 'Guardando video...';
      
      const downloadUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = filename;
      
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      
      window.URL.revokeObjectURL(downloadUrl);

      addDownload({
        title: videoInfo.title,
        thumbnail: videoInfo.thumbnail,
        fileName: filename,
        url: url
      });

      message = `¡Video <strong>${filename}</strong> descargado con éxito!`;
      url = '';
      videoInfo = null;
      return true;
    } catch (error) {
      console.error('Error:', error);
      message = `Error: ${error.message || 'Error al procesar la descarga'}`;
      return false;
    } finally {
      isLoading = false;
    }
  }

  function clearInput() {
    url = '';
    message = 'Ingresa una URL de YouTube';
    videoInfo = null;
  }

  // Cargar URL y descargar automáticamente
  onMount(async () => {
    const params = new URLSearchParams(window.location.search);
    const urlParam = params.get('url');
    if (urlParam) {
      url = urlParam;
      await validateUrl(urlParam);
      if (isValidUrl) {
        await handleSubmit();
      }
    }
  });
</script>

{#if videoInfo}
  <div class="video-info">
    <img src={videoInfo.thumbnail} alt="Video thumbnail" class="thumbnail"/>
    <div class="info">
      <h3>{videoInfo.title}</h3>
      <p>Por: {videoInfo.author}</p>
    </div>
  </div>
{/if}

<form on:submit|preventDefault={handleSubmit}>
  <div class="input-container">
    <div class="input-group">
      <input 
        type="text" 
        bind:value={url} 
        on:input={(e) => validateUrl(e.target.value)}
        placeholder="Pega la URL del video de YouTube"
        disabled={isLoading}
        class:valid={isValidUrl && url}
        class:invalid={!isValidUrl && url}
      />
      <button 
        type="button" 
        on:click={url ? clearInput : pasteFromClipboard}
        disabled={isLoading}
        class="paste-btn"
        title={url ? "Limpiar" : "Pegar URL"}
      >
        {#if url}
          ❌
        {:else}
          📋
        {/if}
      </button>
    </div>

    <button 
      type="submit" 
      disabled={isLoading || !isValidUrl}
      class="download-btn"
    >
      {#if isLoading}
        <span class="loading-message">
          Descargando<span class="loading-dots"><span>.</span><span>.</span><span>.</span></span>
        </span>
      {:else}
        Descargar
      {/if}
    </button>
  </div>
</form>

{#if message}
  <div class="alert" class:alert-success={isValidUrl && !isLoading}
                     class:alert-error={!isValidUrl && url}
                     class:alert-info={!url || isLoading}
                     class:pulsing={isLoading}>
    <div class="alert-icon">
      {#if isValidUrl && !isLoading}
        ✅
      {:else if !isValidUrl && url}
        ⚠️
      {:else}
        ℹ️
      {/if}
    </div>
    <div class="alert-content">
      {#if isLoading}
        <p class="loading-message">
          {message}<span class="loading-dots"><span>.</span><span>.</span><span>.</span></span>
        </p>
      {:else}
        <p>{@html message}</p>
      {/if}
    </div>
  </div>
{/if}

<style>
  .input-container {
    display: flex;
    gap: 10px;
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
  }

  .input-group {
    position: relative;
    flex: 1;
    display: flex;
    align-items: center;
  }

  input {
    width: 100%;
    padding: 12px;
    padding-right: 40px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: #ffffff;
    color: #333333;
  }

  input:focus {
    border-color: #646cff;
    outline: none;
    background: #fafafa;
  }

  input.valid {
    border-color: #4CAF50;
    background: #f8fff8;
    color: #000000;
  }

  input.invalid {
    border-color: #f44336;
    background: #fff8f8;
  }

  .paste-btn {
    position: absolute;
    right: 8px;
    background: none;
    border: none;
    padding: 8px;
    cursor: pointer;
    opacity: 0.6;
    transition: all 0.3s ease;
    color: #666666;
    font-size: 0.9rem;
  }

  .paste-btn:hover {
    opacity: 1;
    color: #333333;
    transform: scale(1.1);
  }

  .download-btn {
    padding: 12px 24px;
    background: #ff0000;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    min-width: 120px;
  }

  .download-btn:hover:not(:disabled) {
    background: #cc0000;
    transform: translateY(-1px);
  }

  .download-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .video-info {
    margin: 20px auto 30px;
    max-width: 800px;
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 15px;
    background: #f5f5f5;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    animation: slideDown 0.3s ease;
  }

  .thumbnail {
    width: 120px;
    height: auto;
    border-radius: 4px;
  }

  .info {
    flex: 1;
    text-align: left;
  }

  .info h3 {
    margin: 0 0 8px 0;
    font-size: 16px;
    color: #333;
  }

  .info p {
    margin: 0;
    font-size: 14px;
    color: #666;
  }

  .alert {
    margin: 20px auto;
    max-width: 800px;
    padding: 12px 16px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 12px;
    animation: slideIn 0.3s ease;
    background: #ffffff;
    border: 2px solid #e0e0e0;
  }

  .alert-success {
    background: #f8fff8;
    border-color: #4CAF50;
    color: #1e4620;
  }

  .alert-error {
    background: #fff8f8;
    border-color: #f44336;
    color: #991b1b;
  }

  .alert-info {
    background: #fafafa;
    border-color: #646cff;
    color: #333333;
  }

  .alert-icon {
    font-size: 1.2rem;
  }

  .alert-content {
    flex: 1;
    text-align: center;
  }

  .alert-content p {
    margin: 0;
    font-size: 0.95rem;
  }

  .loading-message {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
  }

  .loading-dots {
    display: inline-flex;
  }

  .loading-dots span {
    animation: loadingDots 1.4s infinite;
    opacity: 0;
  }

  .loading-dots span:nth-child(1) { animation-delay: 0s; }
  .loading-dots span:nth-child(2) { animation-delay: 0.2s; }
  .loading-dots span:nth-child(3) { animation-delay: 0.4s; }

  @keyframes loadingDots {
    0%, 100% { opacity: 0; }
    50% { opacity: 1; }
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(5px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .alert.pulsing {
    animation: pulseBorder 1.5s ease-in-out infinite;
  }

  @keyframes pulseBorder {
    0% {
      border-color: #646cff;
      box-shadow: 0 0 0 0 rgba(100, 108, 255, 0.4);
    }
    70% {
      border-color: #646cff;
      box-shadow: 0 0 0 10px rgba(100, 108, 255, 0);
    }
    100% {
      border-color: #646cff;
      box-shadow: 0 0 0 0 rgba(100, 108, 255, 0);
    }
  }
</style> 