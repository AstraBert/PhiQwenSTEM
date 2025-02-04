import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Brain, Lightbulb, Workflow } from 'lucide-react';
import { Button } from '@/components/ui/button';

export const Landing: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-blue-50">
      {/* Hero Section */}
      <div className="container mx-auto px-4 pt-20 pb-16">
        <div className="text-center max-w-3xl mx-auto">
          <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Meet phiSTEM
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
            <h3 className="text-xl font-semibold mb-3">Adaptive Learning</h3>
            <p className="text-gray-600">
              Personalized learning paths that adapt to your pace and understanding,
              ensuring you master each concept thoroughly.
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
            <div className="bg-purple-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
              <Lightbulb className="text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold mb-3">Instant Support</h3>
            <p className="text-gray-600">
              Get immediate help with problem-solving, step-by-step explanations,
              and conceptual clarifications 24/7.
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
            <div className="bg-indigo-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
              <Workflow className="text-indigo-600" />
            </div>
            <h3 className="text-xl font-semibold mb-3">Visual Learning</h3>
            <p className="text-gray-600">
              Complex concepts explained through interactive visualizations and
              clear, engaging examples.
            </p>
          </div>
        </div>
      </div>

      {/* Social Proof Section */}
      <div className="bg-white py-16">
        <div className="container mx-auto px-4">
          <div className="text-center max-w-2xl mx-auto">
            <h2 className="text-3xl font-bold mb-8">Trusted by Students & Educators</h2>
            <div className="grid grid-cols-3 gap-8 text-center">
              <div>
                <p className="text-4xl font-bold text-blue-600 mb-2">95%</p>
                <p className="text-gray-600">Improved Grades</p>
              </div>
              <div>
                <p className="text-4xl font-bold text-purple-600 mb-2">50k+</p>
                <p className="text-gray-600">Active Users</p>
              </div>
              <div>
                <p className="text-4xl font-bold text-indigo-600 mb-2">1M+</p>
                <p className="text-gray-600">Problems Solved</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-3xl font-bold mb-6">Ready to Excel in STEM?</h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Join thousands of students who are already mastering STEM subjects with
          phiSTEM's intelligent guidance.
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