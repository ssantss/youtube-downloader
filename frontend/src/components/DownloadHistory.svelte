<script>
  import { downloads } from '../stores/downloads';

  function formatDate(dateString) {
    return new Date(dateString).toLocaleString();
  }
</script>

<div class="history-container">
  <h2>Historial de Descargas</h2>
  
  {#if $downloads.length === 0}
    <p class="empty-state">No hay descargas recientes</p>
  {:else}
    <div class="downloads-list">
      {#each $downloads as download (download.id)}
        <div class="download-item" animate:flip>
          <img src={download.thumbnail} alt="Thumbnail" class="thumbnail"/>
          <div class="info">
            <h3>{download.title}</h3>
            <p class="date">{formatDate(download.downloadDate)}</p>
          </div>
          <div class="status">
            <span class="success">✅</span>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .history-container {
    margin-top: 2rem;
    padding: 1rem;
  }

  h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }

  .downloads-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .download-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: #f5f5f5;
    border-radius: 8px;
    animation: slideIn 0.3s ease;
  }

  .thumbnail {
    width: 80px;
    height: 45px;
    object-fit: cover;
    border-radius: 4px;
  }

  .info {
    flex: 1;
  }

  .info h3 {
    margin: 0;
    font-size: 1rem;
  }

  .date {
    margin: 0;
    font-size: 0.8rem;
    color: #666;
  }

  .empty-state {
    text-align: center;
    color: #666;
    padding: 2rem;
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style> 