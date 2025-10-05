import { motion } from 'framer-motion';

export default function Footer() {
  return (
    <motion.footer 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="bg-brown-900 text-white mt-16"
    >
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h4 className="text-xl font-bold mb-4">CacaoAI Detector</h4>
            <p className="text-brown-200">
              Tecnología de vanguardia para el análisis y detección de enfermedades
              en mazorcas de cacao.
            </p>
          </div>
          <div>
            <h4 className="text-xl font-bold mb-4">Enlaces Rápidos</h4>
            <ul className="space-y-2">
              <li>
                <a href="#inicio" className="text-brown-200 hover:text-white transition-colors">
                  Inicio
                </a>
              </li>
              <li>
                <a href="#historial" className="text-brown-200 hover:text-white transition-colors">
                  Historial
                </a>
              </li>
              <li>
                <a href="#about" className="text-brown-200 hover:text-white transition-colors">
                  Acerca de
                </a>
              </li>
            </ul>
          </div>
          <div>
            <h4 className="text-xl font-bold mb-4">Contacto</h4>
            <ul className="space-y-2 text-brown-200">
              <li>Email: contact@cacaoai.com</li>
              <li>Tel: (123) 456-7890</li>
              <li>Universidad Técnica de Manabí</li>
            </ul>
          </div>
        </div>
        <div className="border-t border-brown-700 mt-8 pt-8 text-center text-brown-300">
          <p>&copy; {new Date().getFullYear()} CacaoAI Detector. Todos los derechos reservados.</p>
        </div>
      </div>
    </motion.footer>
  );
}