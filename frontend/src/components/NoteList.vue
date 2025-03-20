<template>
  <div class="notes-container">
    <h1 class="notes-title">Notes</h1>
    <ul class="notes-list">
      <li v-for="note in notes" :key="note.id" class="note-item">
        <div class="note-header">
          <strong class="note-name">{{ note.name }}</strong>
          <div class="note-actions">
            <button @click="summarizeNote(note)" class="btn btn-summarize">Summarize</button>
            <button @click="redirectToEditNote(note.id)" class="btn btn-edit">Edit</button>
            <button @click="confirmDelete(note.id)" class="btn btn-delete">Delete</button>
          </div>
        </div>
        <p class="note-description">{{ note.description }}</p>
        <div class="note-metadata">
          <small>Created at: {{ note.created_at }}</small>
          <br />
          <small>Updated: {{ note.updated_at }}</small>
        </div>
      </li>
    </ul>

    <button class="add-note-btn" @click="redirectToAddNote">
      +
    </button>

    <div v-if="showConfirmation" class="confirmation-modal">
      <div class="confirmation-content">
        <p>Are you sure you want to delete this note?</p>
        <div class="confirmation-buttons">
          <button @click="deleteNote(noteToDelete)" class="btn btn-confirm">Yes</button>
          <button @click="cancelDelete" class="btn btn-cancel">No</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default {
  data() {
    return {
      notes: [],
      showConfirmation: false,
      noteToDelete: null,
    };
  },
  mounted() {
    this.fetchNotes();
  },
  methods: {
    redirectToAddNote() {
      this.$router.push('/add_note');
    },
    redirectToEditNote(noteId) {
      this.$router.push(`/edit_note/${noteId}`);
    },
    async fetchNotes() {
      try {
        const response = await fetch('http://localhost:8000/notes');
        const data = await response.json();
        this.notes = data;
        this.notes.sort((a, b) => {
          return new Date(b.updated_at) - new Date(a.updated_at);
        });
        console.log(this.notes);
      } catch (error) {
        console.error('Error fetching notes:', error);
      }
    },
    async summarizeNote(note) {
      try {
        const response = await fetch(`http://localhost:8000/notes/summarize/${note.id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ description: note.description }),
        });
        const data = await response.json();
        if (response.ok) {
          note.summary = data;
          toast(note.summary, {
            autoClose: 7000,
            position: toast.POSITION.TOP_RIGHT,
          });
        } else {
          console.error('Error 1 while summarizing note:', data.message);
        }
      } catch (error) {
        console.error('Error 2 while summarizing note:', error);
      }
    },
    confirmDelete(noteId) {
      this.noteToDelete = noteId;
      this.showConfirmation = true;
    },
    cancelDelete() {
      this.showConfirmation = false;
      this.noteToDelete = null;
    },
    async deleteNote(noteId) {
      if (!noteId) return;
      try {
        const response = await fetch(`http://localhost:8000/notes/${noteId}`, {
          method: 'DELETE',
        });
        if (response.ok) {
          this.notes = this.notes.filter((n) => n.id !== noteId);
          toast.success('Note deleted successfully', {
            autoClose: 3000,
            position: toast.POSITION.TOP_RIGHT,
          });
          this.showConfirmation = false;
          this.noteToDelete = null;
        } else {
          const data = await response.json();
          console.error('Error 1 while deleting note:', data.message);
        }
      } catch (error) {
        console.error('Error 2 while deleting note:', error);
      }
    },
  },
};
</script>

<style scoped>
.notes-container {
  font-family: 'Arial', sans-serif;
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f8f8f8;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.notes-title {
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.notes-list {
  list-style: none;
  padding: 0;
}

.note-item {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.note-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.note-name {
  color: #1c4c80;
  font-size: 1.2em;
}

.note-actions {
  display: flex;
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  margin-left: 5px;
  cursor: pointer;
  font-size: 0.9em;
}

.btn-summarize {
  background-color: #28a745;
  color: white;
}

.btn-edit {
  background-color: #007bff;
  color: white;
}

.btn-delete {
  background-color: #dc3545;
  color: white;
}

.note-description {
  color: #333;
  line-height: 1.6;
}

.note-metadata {
  color: #777;
  font-size: 0.8em;
  margin-top: 10px;
}

.add-note-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 50px;
  height: 50px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 1.5em;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.confirmation-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.confirmation-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.confirmation-buttons {
  margin-top: 20px;
}

.btn-confirm,
.btn-cancel {
  padding: 8px 16px;
  margin: 0 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-confirm {
  background-color: #28a745;
  color: white;
}

.btn-cancel {
  background-color: #dc3545;
  color: white;
}
</style>