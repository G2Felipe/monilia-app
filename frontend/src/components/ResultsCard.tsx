'use client';
import { motion } from 'framer-motion';

interface PredictionResult {
  is_cacao: boolean;
  class_name: string;
  confidence: number;
  timestamp: string;
}

interface ResultsCardProps {
  result: PredictionResult;
}

export function ResultsCard({ result }: ResultsCardProps) {
  const getStatusColor = () => {
    if (!result.is_cacao) return 'bg-red-100 text-red-800';
    if (result.confidence > 90) return 'bg-green-100 text-green-800';
    return 'bg-yellow-100 text-yellow-800';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow-lg overflow-hidden"
    >
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Resultado del Análisis
          </h3>
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor()}`}>
            {result.confidence.toFixed(1)}% confianza
          </span>
        </div>

        <div className="space-y-4">
          <div className={`p-4 rounded-lg ${result.is_cacao ? 'bg-green-50' : 'bg-red-50'}`}>
            <p className={`text-lg font-medium ${result.is_cacao ? 'text-green-800' : 'text-red-800'}`}>
              {result.is_cacao 
                ? `Mazorca de Cacao - Tipo: ${result.class_name}`
                : 'No es una mazorca de cacao'}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-500">Clase Detectada</p>
              <p className="font-medium text-gray-900">{result.class_name}</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-500">Fecha de Análisis</p>
              <p className="font-medium text-gray-900">
                {new Date(result.timestamp).toLocaleString()}
              </p>
            </div>
          </div>

          {result.is_cacao && (
            <div className="mt-4 p-4 bg-blue-50 rounded-lg">
              <h4 className="text-blue-800 font-medium mb-2">Recomendaciones</h4>
              <ul className="text-blue-700 text-sm space-y-2">
                <li>• Monitorear regularmente la mazorca</li>
                <li>• Mantener buena ventilación en el cultivo</li>
                <li>• Realizar podas sanitarias periódicas</li>
              </ul>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}