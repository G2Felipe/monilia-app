import { motion } from 'framer-motion';
import Image from 'next/image';
import type { Prediction } from '../types/Prediction';

export default function HistorySection({ predictions = [] }: { predictions: Prediction[] }) {
  return (
    <section id="historial" className="py-12 bg-gradient-to-b from-brown-50/50 to-transparent">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-brown-800 mb-8 text-center">
          Historial de Análisis
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {predictions.map((pred, index) => (
            <motion.div
              key={pred.timestamp}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
            >
              {pred.imageUrl && (
                <div className="relative h-48 w-full">
                  <Image
                    src={pred.imageUrl}
                    alt="Mazorca analizada"
                    fill
                    className="object-cover"
                  />
                </div>
              )}
              <div className="p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-500">
                    {new Date(pred.timestamp).toLocaleDateString()}
                  </span>
                  <span className={`px-2 py-1 rounded-full text-xs ${
                    pred.is_cacao ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {pred.is_cacao ? 'Mazorca de Cacao' : 'No es Mazorca'}
                  </span>
                </div>
                <p className="text-lg font-semibold text-brown-800 mb-1">
                  {pred.class_name}
                </p>
                <div className="flex items-center">
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-brown-600 h-2 rounded-full"
                      style={{ width: `${pred.confidence}%` }}
                    />
                  </div>
                  <span className="ml-2 text-sm text-gray-600">
                    {pred.confidence.toFixed(1)}%
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}