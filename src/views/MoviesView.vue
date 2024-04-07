<template>
  <div
    style="
      display: grid;
      grid-template-columns: 3fr 3fr 3fr;
      margin: 20px;
      gap: 10px;
      spacing: 10px;
    "
  >
    <div v-for="movie of movies" class="card mb-3" style="max-width: 700px">
      <div class="row no-gutters">
        <div class="col-md-4">
          <img
            v-bind:src="`/api/v1/posters/${movie.poster}`"
            class="card-img"
            alt="movie poster"
          />
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <h5 class="card-title">{{ movie.title }}</h5>
            <p class="card-text">{{ movie.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";

let movies = ref([]);

onMounted(() => {
  fetchMovies();
});

async function fetchMovies() {
  const response = await fetch("/api/v1/movies", {
    method: "GET",
  });
  const moviesData = await response.json();

  movies.value = moviesData.movies;
}
</script>
