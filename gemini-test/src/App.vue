<script setup lang="ts">
import { useTranslation } from "./composables/useTranslation";

const {
  languages,
  inputLanguage,
  outputLanguage,
  inputText,
  translatedText,
  loading,
  error,
  canTranslate,
  translate,
} = useTranslation();
</script>

<template>
  <v-app>
    <v-main class="bg-light-green-lighten-4">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" sm="10" md="8" lg="6">
            <v-card class="mt-4 pa-6" elevation="3">
              <v-card-title class="text-center text-h4 mb-6">
                Translation Service
              </v-card-title>

              <v-card-text>
                <!-- Language Selectors -->
                <v-row>
                  <v-col cols="12" sm="6">
                    <v-select
                      v-model="inputLanguage"
                      :items="languages"
                      label="From"
                      variant="outlined"
                      density="comfortable"></v-select>
                  </v-col>

                  <v-col cols="12" sm="6">
                    <v-select
                      v-model="outputLanguage"
                      :items="languages"
                      label="To"
                      variant="outlined"
                      density="comfortable"></v-select>
                  </v-col>
                </v-row>

                <!-- Text Areas -->
                <v-row>
                  <v-col cols="12" sm="6">
                    <v-textarea
                      v-model="inputText"
                      label="Enter text"
                      variant="outlined"
                      rows="5"
                      auto-grow
                      counter></v-textarea>
                  </v-col>

                  <v-col cols="12" sm="6">
                    <v-textarea
                      v-model="translatedText"
                      label="Translation"
                      variant="outlined"
                      rows="5"
                      readonly
                      :loading="loading"
                      :placeholder="
                        loading
                          ? 'Translating...'
                          : 'Translation will appear here'
                      "></v-textarea>
                  </v-col>
                </v-row>

                <!-- Translate Button -->
                <v-row>
                  <v-col cols="12">
                    <v-btn
                      block
                      color="primary"
                      size="large"
                      :loading="loading"
                      :disabled="!canTranslate || loading"
                      @click="translate">
                      {{ loading ? "Translating..." : "Translate" }}
                      <v-icon end icon="mdi-translate"></v-icon>
                    </v-btn>
                  </v-col>
                </v-row>

                <!-- Error Alert -->
                <v-row v-if="error">
                  <v-col cols="12">
                    <v-alert type="error" variant="tonal" closable>
                      {{ error }}
                    </v-alert>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped>
.v-main {
  min-height: 100vh;
}

.v-card {
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.9) !important;
}

.v-btn {
  text-transform: none;
}

/* Add smooth transitions */
.v-card,
.v-btn,
.v-text-field {
  transition: all 0.3s ease;
}

/* Hover effects */
.v-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1) !important;
}

/* Custom scrollbar for textareas */
:deep(.v-textarea textarea) {
  scrollbar-width: thin;
  scrollbar-color: #4caf50 transparent;
}

:deep(.v-textarea textarea::-webkit-scrollbar) {
  width: 8px;
}

:deep(.v-textarea textarea::-webkit-scrollbar-track) {
  background: transparent;
}

:deep(.v-textarea textarea::-webkit-scrollbar-thumb) {
  background-color: #4caf50;
  border-radius: 4px;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .v-card-title {
    font-size: 1.5rem !important;
  }

  .v-container {
    padding: 12px;
  }
}
</style>
