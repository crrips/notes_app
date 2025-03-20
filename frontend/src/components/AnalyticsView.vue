<template>
  <div class="analytics-view">

    <div class="analytics-container">
      <div class="analytics-section combined-section">
        <h3 class="section-title">General Analytics</h3>
        <div class="analytics-item">
          <strong>Total Words:</strong> {{ analytics.total_word_count }}
        </div>
        <div class="analytics-item">
          <strong>Average Note Length:</strong> {{ analytics.avg_note_length.toFixed(2) }} words
        </div>
        <div class="chart-container">
          <div class="chart-bar" :style="{ width: getWordCountBarWidth() }"></div>
        </div>

        <h3 class="section-title">Longest Notes</h3>
        <table class="notes-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Length</th>
              <th>Words</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="note in analytics.top_3_longest_notes" :key="note.id">
              <td>{{ note.name }}</td>
              <td>{{ note.description_length }}</td>
              <td>{{ note.word_count }}</td>
            </tr>
          </tbody>
        </table>

        <h3 class="section-title">Shortest Notes</h3>
        <table class="notes-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Length</th>
              <th>Words</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="note in analytics.top_3_shortest_notes" :key="note.id">
              <td>{{ note.name }}</td>
              <td>{{ note.description_length }}</td>
              <td>{{ note.word_count }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="analytics-section">
        <h3 class="section-title">Most Common Words</h3>
        <ul class="word-list">
          <li v-for="(word, index) in analytics.most_common_words" :key="index" class="word-item">
            {{ word[0] }}: {{ word[1] }} times
            <div class="word-bar-container">
              <div class="word-bar" :style="{ width: getWordBarWidth(word[1]) }"></div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';

export default {
  setup() {
    const analytics = ref({
      total_word_count: 0,
      avg_note_length: 0,
      most_common_words: [],
      top_3_longest_notes: [],
      top_3_shortest_notes: [],
    });
    
    onMounted(async () => {
      try {
        const response = await fetch('http://localhost:8000/analytics');
        if (response.ok) {
          analytics.value = await response.json();
        } else {
          console.error('Failed to fetch analytics data');
        }
      } catch (error) {
        console.error('Error fetching analytics data:', error);
      }
    });

    const maxWordCount = computed(() => {
      if (analytics.value.most_common_words.length === 0) return 1;
      return Math.max(...analytics.value.most_common_words.map(word => word[1]));
    });

    const maxWordNote = computed(() => {
      if (analytics.value.top_3_longest_notes.length === 0) return 1;
      return Math.max(...analytics.value.top_3_longest_notes.map(note => note.word_count));
    });

    const getWordCountBarWidth = () => {
      const percentage = (maxWordNote.value / analytics.value.total_word_count) * 100;
      console.log(maxWordNote.value / analytics.value.total_word_count) * 100;
      return `${Math.min(percentage, 100)}%`;
    };

    const getWordBarWidth = (count) => {
      const percentage = (count / maxWordCount.value) * 100;
      return `${Math.min(percentage, 100)}%`;
    };

    return { analytics, getWordCountBarWidth, getWordBarWidth, maxWordCount };
  },
};
</script>

<style scoped>
.analytics-view {
  min-width: 80%;
  font-family: 'Arial', sans-serif;

  margin: 20px auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.analytics-title {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.analytics-container {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

.analytics-section {
  width: 40%;
  min-width: 200px;
  margin: 10px;
  padding: 20px;
  background-color: #fff;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.section-title {
  color: #1c4c80;
  margin-bottom: 15px;
  font-size: 1.3em;
}

.analytics-item {
  margin-bottom: 10px;
  font-size: 1em;
  color: #555;
}

.word-list {
  list-style: none;
  padding: 0;
}

.word-item {
  padding: 8px 12px;
  border-bottom: 1px solid #eee;
  font-size: 0.95em;
  color: #333;
}

.notes-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.notes-table th,
.notes-table td {
  padding: 10px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.notes-table th {
  background-color: #f0f0f0;
  font-weight: 600;
}

.notes-table tbody tr:hover {
  background-color: #f5f5f5;
}

.chart-container {
  width: 100%;
  height: 20px;
  background-color: #eee;
  border-radius: 4px;
  margin-top: 10px;
}

.chart-bar {
  height: 100%;
  background-color: #4CAF50;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.word-bar-container {
  width: 100%;
  height: 10px;
  background-color: #f0f0f0;
  border-radius: 3px;
  margin-top: 5px;
}

.word-bar {
  height: 100%;
  background-color: #2196F3;
  border-radius: 3px;
  transition: width 0.3s ease;
}
</style>