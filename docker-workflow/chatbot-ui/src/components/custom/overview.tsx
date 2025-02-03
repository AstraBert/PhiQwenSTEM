import { motion } from 'framer-motion';
import { BotMessageSquare, FlaskConical } from 'lucide-react';

export const Overview = () => {
  return (
    <>
    <motion.div
      key="overview"
      className="max-w-3xl mx-auto md:mt-20"
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.98 }}
      transition={{ delay: 0.75 }}
    >
      <div className="rounded-xl p-6 flex flex-col gap-8 leading-relaxed text-center max-w-xl">
        <p className="flex flex-row justify-center gap-4 items-center">
          <BotMessageSquare size={44}/>
          <span>+</span>
          <FlaskConical size={44}/>
        </p>
        <p>
          Hello, I am <strong className="text-blue-500">phiSTEM</strong>, a reasoning chatbot assistant for Physics, Chemistry, Math and Biochemistry<br />
          Powered by <strong><a href='https://huggingface.co/' className="text-blue-500 underline">HuggingFace</a></strong> and <strong><a href='https://qdrant.tech/' className="text-blue-500 underline">Qdrant</a></strong>.
        </p>
      </div>
    </motion.div>
    </>
  );
};
