import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cx } from 'classix';
import { BotIcon } from './icons';
import { Markdown } from './markdown';
import { message } from "../../interfaces/interfaces";
import { MessageActions } from '@/components/custom/actions';

export const PreviewMessage = ({ message }: { message: message }) => {
  const [displayedContent, setDisplayedContent] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const streamingSpeed = 0.00001;

  useEffect(() => {
    if (message.role === 'assistant') {
      setDisplayedContent('');
      setIsStreaming(true);

      let currentText = '';
      const fullContent = message.content || '';
      let currentIndex = 0;

      const streamInterval = setInterval(() => {
        if (currentIndex < fullContent.length) {
          currentText += fullContent[currentIndex];
          setDisplayedContent(currentText);
          currentIndex++;
        } else {
          setIsStreaming(false);
          clearInterval(streamInterval);
        }
      }, streamingSpeed);

      return () => clearInterval(streamInterval);
    } else {
      setDisplayedContent(message.content || '');
      setIsStreaming(false);
    }
  }, [message.content, message.role]);

  return (
    <motion.div
      className="w-full mx-auto max-w-3xl px-4 group/message"
      initial={{ y: 5, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      data-role={message.role}
    >
      <div
        className={cx(
          'group-data-[role=user]/message:bg-blue-700 dark:group-data-[role=user]/message:bg-muted group-data-[role=user]/message:text-white flex gap-4 group-data-[role=user]/message:px-3 w-full group-data-[role=user]/message:w-fit group-data-[role=user]/message:ml-auto group-data-[role=user]/message:max-w-2xl group-data-[role=user]/message:py-2 rounded-xl'
        )}
      >
        {message.role === 'assistant' && (
          <div className="size-8 flex items-center rounded-full justify-center ring-1 shrink-0 ring-border">
            <BotIcon />
          </div>
        )}

        <div className="flex flex-col w-full">
          <div className="flex flex-col gap-4 text-left">
            <Markdown>{message.role === 'assistant' ? displayedContent : (message.content || '')}</Markdown>
            {message.role === 'assistant' && isStreaming && (
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: [0, 1] }}
                transition={{ repeat: Infinity, duration: 0.5 }}
                className="inline-block w-2 h-4 bg-primary ml-1"
              />
            )}
          </div>

          {message.role === 'assistant' && !isStreaming && (
            <MessageActions message={message} />
          )}
        </div>
      </div>
    </motion.div>
  );
};

export const LoadingDots = () => (
  <span className="inline-flex items-center gap-1">
    {[0, 1, 2].map((dot) => (
      <motion.span
        key={dot}
        className="w-1 h-1 bg-primary rounded-full"
        initial={{ opacity: 0.2 }}
        animate={{ opacity: 1 }}
        transition={{
          duration: 0.5,
          repeat: Infinity,
          repeatType: "reverse",
          delay: dot * 0.2
        }}
      />
    ))}
  </span>
);

export const ThinkingMessage = () => {
  return (
    <div className="flex flex-row gap-4 px-4 w-full md:max-w-3xl mx-auto items-start">
      <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
        <motion.div
          className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full"
          animate={{ rotate: 360 }}
          transition={{
            duration: 1,
            repeat: Infinity,
            ease: "linear"
          }}
        />
      </div>
      <div className="flex-1 space-y-2 overflow-hidden">
        <motion.div
          className="rounded-xl bg-muted p-4"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <p className="text-sm">
            PhiCare is producing its answer
            <LoadingDots />
          </p>
        </motion.div>
      </div>
    </div>
  );
};