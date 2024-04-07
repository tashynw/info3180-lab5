<template>
  <form
    @submit.prevent="saveMovie"
    id="movieForm"
    style="display: flex; flex-direction: column; gap: 20px"
  >
    <div class="form-group">
      <label for="title">Title</label>
      <input name="title" class="form-control" placeholder="Enter title" />
    </div>
    <div class="form-group">
      <label for="description">Description</label>
      <textarea
        name="description"
        class="form-control"
        placeholder="Enter description"
      ></textarea>
    </div>
    <div class="form-group">
      <label for="poster">Poster</label>
      <input name="poster" class="form-control" type="file" />
    </div>
    <div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");

function getCsrfToken() {
  fetch("/api/v1/csrf-token")
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    });
}

onMounted(() => {
  getCsrfToken();
});

function saveMovie() {
  let movieForm = document.getElementById("movieForm");
  let form_data = new FormData(movieForm);

  fetch("/api/v1/movies", {
    method: "POST",
    body: form_data,
    headers: {
      "X-CSRFToken": csrf_token.value,
    },
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      // display a success message
      console.log(data);
    })
    .catch(function (error) {
      console.log(error);
    });
}
</script>
