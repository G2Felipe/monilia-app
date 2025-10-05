'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import toast from 'react-hot-toast';
import axios from 'axios';
import Image from 'next/image';
import { ImageUploader } from '@/components/ImageUploader';
import Header from '@/components/Header';
import InfoCarousel from '@/components/InfoCarousel';
import HistorySection from '@/components/HistorySection';
import Footer from '@/components/Footer';
import type { Prediction } from '@/types/Prediction';

export default function Home() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(false);

  const handleImageUpload = async (file: File) => {
    setSelectedImage(file);
    setLoading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await axios.post('http://localhost:8000/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      const newPrediction = {
        ...response.data.prediction,
        imageUrl: URL.createObjectURL(file),
        timestamp: new Date().toISOString()
      };
      
      setPrediction(newPrediction);
      setPredictions(prev => [newPrediction, ...prev]);
      toast.success('¡Predicción completada!');
    } catch (error) {
      console.error('Error al procesar la imagen:', error);
      toast.error('Error al procesar la imagen');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-brown-50 to-brown-100">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-bold text-brown-900 mb-4">
            Detector de Moniliasis en Cacao
          </h1>
          <p className="text-brown-700 text-xl max-w-2xl mx-auto">
            Utiliza nuestra tecnología de IA para detectar la presencia de moniliasis en tus mazorcas de cacao
          </p>
        </motion.div>
        
        <InfoCarousel />

        <div className="mt-16 max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Panel izquierdo: Subida y vista previa */}
            <div className="bg-brown-800 rounded-2xl shadow-xl p-8">
              <div className="space-y-6">
                <div className="text-center">
                  <h3 className="text-2xl font-bold text-brown-100 mb-2">Analizar Imagen</h3>
                  <p className="text-brown-200">Sube una imagen clara de la mazorca de cacao para obtener los mejores resultados</p>
                </div>
                
                <div className="flex justify-center">
                  <div className="w-full max-w-md">
                    <ImageUploader onImageUpload={handleImageUpload} loading={loading} />
                  </div>
                </div>

                <AnimatePresence mode="wait">
                  {selectedImage && (
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      className="relative"
                    >
                      <div className="aspect-square w-full rounded-xl overflow-hidden border-4 border-brown-100 shadow-lg">
                        <Image
                          src={selectedImage ? URL.createObjectURL(selectedImage) : ''}
                          alt="Vista previa"
                          fill
                          className="object-cover"
                        />
                      </div>
                      {loading && (
                        <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center rounded-xl">
                          <div className="text-white text-center">
                            <div className="animate-spin rounded-full h-12 w-12 border-4 border-white border-t-transparent mb-2"></div>
                            <p>Analizando imagen...</p>
                          </div>
                        </div>
                      )}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>

            {/* Panel derecho: Resultados */}
            <div className="relative">
              <AnimatePresence mode="wait">
                {prediction ? (
                  <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    className="h-full"
                  >
                    <div className="bg-gradient-to-br from-brown-50 to-brown-100 rounded-2xl shadow-xl p-8 h-full">
                      <div className="space-y-6">
                        <div className="text-center">
                          <h3 className="text-2xl font-bold text-brown-900 mb-2">Resultados del Análisis</h3>
                          <div className={`inline-block px-4 py-2 rounded-full ${
                            prediction?.is_cacao 
                              ? 'bg-green-100 text-green-800 border border-green-200' 
                              : 'bg-red-100 text-red-800 border border-red-200'
                          }`}>
                            {prediction?.is_cacao ? 'Es una mazorca de cacao' : 'No es una mazorca de cacao'}
                          </div>
                        </div>

                        <div className="bg-brown-800 rounded-xl p-6 shadow-sm space-y-4">
                          <div>
                            <h4 className="text-lg font-semibold text-brown-100 mb-3">Clasificación</h4>
                            <div className="text-2xl font-bold text-white text-center p-3 bg-brown-900/40 rounded-lg border border-brown-700">
                              {prediction?.class_name}
                            </div>
                          </div>

                          <div>
                            <div className="flex justify-between items-center mb-2">
                              <h4 className="text-lg font-semibold text-brown-100">Nivel de Confianza</h4>
                              <span className="text-xl font-bold text-white">
                                {prediction?.confidence?.toFixed(1)}%
                              </span>
                            </div>
                            <div className="relative h-4 bg-brown-900/40 rounded-full overflow-hidden border border-brown-700">
                              <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${prediction?.confidence}%` }}
                                transition={{ duration: 0.8, ease: "easeOut" }}
                                className={`absolute h-full rounded-full ${
                                  prediction?.confidence && prediction.confidence > 70
                                    ? 'bg-gradient-to-r from-green-400 to-green-600'
                                    : prediction?.confidence && prediction.confidence > 20
                                    ? 'bg-gradient-to-r from-yellow-400 to-yellow-600'
                                    : 'bg-gradient-to-r from-red-400 to-red-600'
                                }`}
                              />
                            </div>
                          </div>
                        </div>

                        <div className="mt-4 flex justify-between items-center text-sm text-brown-600">
                          <div className="flex items-center">
                            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            {prediction?.timestamp && new Date(prediction.timestamp).toLocaleString()}
                          </div>
                          <button 
                            onClick={() => setSelectedImage(null)}
                            className="text-brown-500 hover:text-brown-700 transition-colors"
                          >
                            Analizar otra imagen
                          </button>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ) : (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="h-full bg-white rounded-2xl shadow-xl p-8 flex items-center justify-center"
                  >
                    <div className="text-center text-brown-600">
                      <div className="w-24 h-24 mx-auto mb-4 bg-brown-50 rounded-full flex items-center justify-center">
                        <svg className="w-12 h-12 text-brown-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                        </svg>
                      </div>
                      <h3 className="text-xl font-semibold text-brown-800 mb-2">Sin resultados aún</h3>
                      <p className="text-brown-500">Sube una imagen para comenzar el análisis</p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </div>

        {/* Sección de Historial */}
        {predictions.length > 0 && (
          <section className="mt-16">
            <HistorySection predictions={predictions} />
          </section>
        )}
      </main>

      <Footer />
    </div>
  );
}
