import { motion } from 'framer-motion';
import Image from 'next/image';

export default function Header() {
  return (
    <motion.header 
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="bg-gradient-to-r from-brown-800 to-brown-900 text-white shadow-lg"
    >
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Image
              src="/images/ui/frijoles.png"
              alt="Cacao AI Logo"
              width={50}
              height={50}
              className="rounded-full bg-white p-2 shadow-lg"
            />
            <div>
              <h1 className="text-2xl font-bold">CacaoAI Detector</h1>
              <p className="text-sm text-brown-200">Análisis Inteligente de Mazorcas de Cacao</p>
            </div>
          </div>
          <nav className="hidden md:flex space-x-8">
            <a href="#inicio" className="hover:text-brown-200 transition-colors">Inicio</a>
            <a href="#historial" className="hover:text-brown-200 transition-colors">Historial</a>
            <a href="#about" className="hover:text-brown-200 transition-colors">Acerca de</a>
          </nav>
        </div>
      </div>
    </motion.header>
  );
}