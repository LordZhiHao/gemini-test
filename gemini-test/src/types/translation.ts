export interface TranslationRequest {
  input_language: string;
  output_language: string;
  text_input: string;
}

export interface TranslationResponse {
  translated_text: string;
}
