<template>
  <form
    @submit.prevent="saveMovie"
    ref="movieFormRef"
    id="movieForm"
    style="display: flex; flex-direction: column; gap: 20px"
  >
    <div class="alert alert-success" role="alert" v-if="successfullyCreated">
      Form successfully saved
    </div>
    <div
      class="alert alert-danger"
      role="alert"
      v-if="formErrors && formErrors.length > 0 && !successfullyCreated"
    >
      <li v-for="error in formErrors">
        {{ error }}
      </li>
    </div>
    <div
      class="alert alert-danger"
      role="alert"
      v-if="formErrors == true && !successfullyCreated"
    >
      An error occurred while creating the movie
    </div>
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
import { ref, onMounted, router } from "vue";

let csrf_token = ref("");
let formErrors = ref([]);
let successfullyCreated = ref(false);

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
      if (
        data &&
        Object.keys(data).length > 0 &&
        Object.keys(data)[0] == "errors"
      ) {
        successfullyCreated.value = false;
        formErrors.value = data?.errors;
      } else {
        successfullyCreated.value = true;
        this.$refs.movieFormRef.reset();
      }
    })
    .catch(function (error) {
      formErrors.value = true;
      successfullyCreated.value = false;
    });
}
</script>
