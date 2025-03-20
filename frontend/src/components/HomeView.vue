<template>
  <div>
    <NoteList :notes="notes" @note-deleted="fetchNotes" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import NoteList from '../components/NoteList.vue';

export default {
  components: { NoteList },
  setup() {
    const notes = ref([]);

    const fetchNotes = async () => {
      const response = await fetch('http://localhost:8000/notes');
      notes.value = await response.json();
    };

    onMounted(fetchNotes);

    return { notes, fetchNotes };
  }
};
</script>
