import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Image from 'next/image';

const carouselItems = [
  {
    title: "Detección Precisa",
    description: "Nuestra IA analiza con precisión el estado de tus mazorcas de cacao",
    image: "/images/cacao/1.jpg"
  },
  {
    title: "Resultados Instantáneos",
    description: "Obtén resultados en segundos sobre el estado de tus cultivos",
    image: "/images/cacao/2.jpg"
  },
  {
    title: "Tecnología Avanzada",
    description: "Utilizamos modelos de IA de última generación para el análisis",
    image: "/images/cacao/3.jpg"
  },
  {
    title: "Fácil de Usar",
    description: "Interfaz intuitiva diseñada para agricultores y expertos",
    image: "/images/cacao/4.jpg"
  }
];

export default function InfoCarousel() {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((current) => (current + 1) % carouselItems.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="w-full py-8 rounded-xl overflow-hidden">
      <div className="container mx-auto px-4">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            initial={{ opacity: 0, scale: 1.1 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            transition={{ duration: 0.7 }}
            className="relative h-[400px] rounded-2xl overflow-hidden"
          >
            <Image
              src={carouselItems[currentIndex].image}
              alt={carouselItems[currentIndex].title}
              fill
              className="object-cover"
              priority
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/50 to-transparent">
              <div className="absolute bottom-0 left-0 right-0 p-8 text-center">
                <motion.h3
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.2 }}
                  className="text-3xl font-bold text-white mb-4 drop-shadow-lg"
                >
                  {carouselItems[currentIndex].title}
                </motion.h3>
                <motion.p
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.3 }}
                  className="text-xl text-gray-100 max-w-2xl mx-auto drop-shadow-lg"
                >
                  {carouselItems[currentIndex].description}
                </motion.p>
              </div>
            </div>
          </motion.div>
        </AnimatePresence>
        <div className="flex justify-center space-x-2 mt-4">
          {carouselItems.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentIndex(index)}
              className={`w-2 h-2 rounded-full transition-all ${
                index === currentIndex ? 'bg-brown-600 w-4' : 'bg-brown-300'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}