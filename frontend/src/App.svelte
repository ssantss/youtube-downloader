<script lang="ts">
  // @ts-ignore
  import SearchVideo from './components/SearchVideo.svelte';
  import DownloadHistory from './components/DownloadHistory.svelte';
</script>

<main>
  <h1>YouTube Downloader</h1>
  <SearchVideo />
  <DownloadHistory />
</main>

<style>
  main {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
  }
</style>
