<template>
    <div class="edit-note-form">
      <h2 class="form-title">Edit Note</h2>
      <div class="form-group">
        <label for="name" class="form-label">Title:</label>
        <input v-model="editedNote.name" id="name" placeholder="Enter title" class="form-input" />
      </div>
      <div class="form-group">
        <label for="description" class="form-label">Description:</label>
        <textarea v-model="editedNote.description" id="description" placeholder="Enter description" class="form-input description-input"></textarea>
      </div>
      <div class="form-actions">
        <button @click="saveNote" class="btn btn-save">Update</button>
        <button @click="clearForm" class="btn btn-cancel">Cancel</button>
      </div>
    </div>
  </template>
  
<script>
  import { ref, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  
  export default {
    setup() {
      const route = useRoute();
      const router = useRouter();
      const noteId = route.params.id;
      const editedNote = ref({
        id: noteId,
        name: '',
        description: '',
      });
  
      onMounted(async () => {
        try {
          const response = await fetch(`http://localhost:8000/notes/${noteId}`);
          if (response.ok) {
            const data = await response.json();
            editedNote.value = {
              id: noteId,
              name: data.name,
              description: data.description,
            };
          } else {
            console.error('Failed to fetch note for editing');
            router.push('/');
          }
        } catch (error) {
          console.error('Error fetching note:', error);
          router.push('/');
        }
      });

      return { editedNote };
    },

    methods: {
      clearForm() {
        this.newNote = { name: '', description: '' };
        this.$router.push('/');
      },
  
      async saveNote() {
        try {
          const requestBody = JSON.stringify({
            id: this.editedNote.id,
            name: this.editedNote.name,
            description: this.editedNote.description,
          });
  
          console.log("Request body:", requestBody);
  
          const response = await fetch(`http://localhost:8000/notes/${this.editedNote.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: requestBody,
          });
  
          console.log("Server response:", response);
          
          if (response.ok) {
            console.log('Note saved successfully');
            this.clearForm();
            this.$router.push('/');
          } else {
            console.error("Error 1 while saving note:", response);
          }
        } catch (error) {
          console.error("Error 2 while saving note:", error);
        }
      },
    }

  };
</script>
  
<style scoped>
.edit-note-form {
  min-width: 50%;
  margin: 50px auto;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

.form-title {
  text-align: center;
  margin-bottom: 25px;
  color: #333;
  font-size: 1.8em;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 600;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1em;
  color: #333;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
}

.form-input:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.description-input {
  resize: vertical;
  min-height: 150px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 25px;
}

.btn {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 1em;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-left: 10px;
}

.btn-save {
  background-color: #28a745;
  color: white;
}

.btn-cancel {
  background-color: #dc3545;
  color: white;
}

.btn-save:hover,
.btn-cancel:hover {
  filter: brightness(95%);
}
</style>