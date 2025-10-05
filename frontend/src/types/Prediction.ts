export interface Prediction {
  timestamp: string;
  imageUrl?: string;
  is_cacao: boolean;
  class_name: string;
  confidence: number;
}

export interface HistorySectionProps {
  predictions: Prediction[];
}