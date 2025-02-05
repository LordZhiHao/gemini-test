import { ref, computed } from "vue";
import axios from "axios";
import type {
  TranslationRequest,
  TranslationResponse,
} from "@/types/translation";

export function useTranslation() {
  const languages = [
    "English",
    "Spanish",
    "French",
    "German",
    "Italian",
    "Portuguese",
    "Russian",
    "Japanese",
    "Chinese",
    "Korean",
  ];

  const inputLanguage = ref("English");
  const outputLanguage = ref("Spanish");
  const inputText = ref("");
  const translatedText = ref("");
  const loading = ref(false);
  const error = ref<string | null>(null);

  const canTranslate = computed(() => {
    return (
      inputLanguage.value &&
      outputLanguage.value &&
      inputText.value.trim() !== "" &&
      inputLanguage.value !== outputLanguage.value
    );
  });

  const translate = async () => {
    if (!canTranslate.value) return;

    loading.value = true;
    error.value = null;
    translatedText.value = "";

    try {
      const response = await axios.post<TranslationResponse>(
        "http://localhost:8000/translate/",
        {
          input_language: inputLanguage.value,
          output_language: outputLanguage.value,
          text_input: inputText.value,
        } as TranslationRequest
      );

      translatedText.value = response.data.translated_text;
    } catch (e) {
      error.value =
        e instanceof Error ? e.message : "An error occurred during translation";
    } finally {
      loading.value = false;
    }
  };

  return {
    languages,
    inputLanguage,
    outputLanguage,
    inputText,
    translatedText,
    loading,
    error,
    canTranslate,
    translate,
  };
}
