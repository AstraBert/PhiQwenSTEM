import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Brain, LockOpen, Footprints } from 'lucide-react';
import { Button } from '@/components/ui/button';

export const Landing: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-blue-50">
      {/* Hero Section */}
      <div className="container mx-auto px-4 pt-20 pb-16">
        <div className="text-center max-w-3xl mx-auto">
          <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Meet PhiQwenSTEM
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Your intelligent companion for mastering STEM subjects. Get step-by-step guidance, 
            instant feedback, and deepen your understanding of complex concepts.
          </p>
          <Button 
            onClick={() => navigate('/chat')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-6 rounded-lg text-lg font-semibold transition-all hover:scale-105"
          >
            Start Learning Now
            <ArrowRight className="ml-2" />
          </Button>
        </div>
      </div>

      {/* Features Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
            <div className="bg-blue-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
              <Brain className="text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold mb-3">Large Knowledge Base</h3>
            <p className="text-gray-600">
              Based on a curated subset of <a href='https://huggingface.co/datasets/EricLu/SCP-116K' className="text-blue-700 underline">EricLu/SCP-116K</a> HuggingFace dataset, our knowledge base collects more than 15,000 STEM-related question and answers.
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
            <div className="bg-purple-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
              <LockOpen className="text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold mb-3">Open Source</h3>
            <p className="text-gray-600">
              PhiQwenSTEM is open source and fully reproducible in a local setting: check out the <a href='https://github.com/AstraBert/PhiQwenSTEM' className="text-purple-700 underline">GitHub repository</a>!
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
            <div className="bg-indigo-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
              <Footprints className="text-indigo-600" />
            </div>
            <h3 className="text-xl font-semibold mb-3">Step-By-Step Solution</h3>
            <p className="text-gray-600">
              Each solution is to your problems is given guiding you step-by-step towards the answer, starting from scratch.
            </p>
          </div>
        </div>
      </div>

      {/* Social Proof Section */}
      <div className="bg-white py-16">
        <div className="container mx-auto px-4">
          <div className="text-center max-w-2xl mx-auto">
            <h2 className="text-3xl font-bold mb-8">Created for Students</h2>
            <div className="grid grid-cols-3 gap-8 text-center">
              <div>
                <p className="text-4xl font-bold text-blue-600 mb-2">10</p>
                <p className="text-gray-600">STEM subjects</p>
              </div>
              <div>
                <p className="text-4xl font-bold text-purple-600 mb-2">15k+</p>
                <p className="text-gray-600">Questions in its database</p>
              </div>
              <div>
                <p className="text-4xl font-bold text-indigo-600 mb-2">Free</p>
                <p className="text-gray-600">To use for everyone</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-3xl font-bold mb-6">Ready to Excel in STEM?</h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Let PhiQwenSTEM guide you through complex concepts and start learning!
        </p>
        <Button 
          onClick={() => navigate('/chat')}
          className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-6 rounded-lg text-lg font-semibold transition-all hover:scale-105"
        >
          Begin Your Journey
          <ArrowRight className="ml-2" />
        </Button>
      </div>
    </div>
  );
};