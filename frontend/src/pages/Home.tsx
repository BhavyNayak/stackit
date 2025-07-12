import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Question } from '../types';
import apiService from '../services/api';
import { formatDistanceToNow } from 'date-fns';
import toast from 'react-hot-toast';

const Home: React.FC = () => {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [popularTags, setPopularTags] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setIsLoading(true);
      const [questionsResponse, tagsResponse] = await Promise.all([
        apiService.getQuestions({ sort: 'newest', limit: 10 }),
        apiService.getPopularTags()
      ]);

      if (questionsResponse.data) {
        setQuestions(questionsResponse.data);
      }
      if (tagsResponse.data) {
        setPopularTags(tagsResponse.data);
      }
    } catch (error) {
      console.error('Failed to fetch home data:', error);
      toast.error('Failed to load content');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary-600 to-primary-700 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Welcome to StackIt
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-primary-100">
            A collaborative Q&A platform for knowledge sharing and learning
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/questions"
              className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200"
            >
              Browse Questions
            </Link>
            <Link
              to="/ask"
              className="bg-primary-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-400 transition-colors duration-200"
            >
              Ask a Question
            </Link>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Questions Section */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-2xl font-bold text-gray-900">Recent Questions</h2>
              </div>
              <div className="divide-y divide-gray-200">
                {questions.length === 0 ? (
                  <div className="p-6 text-center text-gray-500">
                    No questions yet. Be the first to ask!
                  </div>
                ) : (
                  questions.map((question) => (
                    <div key={question.question_id} className="p-6 hover:bg-gray-50 transition-colors duration-200">
                      <div className="flex items-start space-x-4">
                        <div className="flex flex-col items-center space-y-1 min-w-0">
                          <div className="text-center">
                            <div className="text-lg font-semibold text-gray-900">
                              {question.vote_count || 0}
                            </div>
                            <div className="text-xs text-gray-500">votes</div>
                          </div>
                          <div className="text-center">
                            <div className="text-lg font-semibold text-gray-900">
                              {question.answer_count || 0}
                            </div>
                            <div className="text-xs text-gray-500">answers</div>
                          </div>
                        </div>
                        <div className="flex-1 min-w-0">
                          <Link
                            to={`/questions/${question.question_id}`}
                            className="text-lg font-semibold text-gray-900 hover:text-primary-600 transition-colors duration-200"
                          >
                            {question.title}
                          </Link>
                          <div className="mt-2 flex flex-wrap gap-2">
                            {question.tags?.map((tag) => (
                              <span key={tag} className="tag">
                                {tag}
                              </span>
                            ))}
                          </div>
                          <div className="mt-3 flex items-center text-sm text-gray-500">
                            <span>Asked by {question.author?.username || 'Anonymous'}</span>
                            <span className="mx-2">•</span>
                            <span>{formatDistanceToNow(new Date(question.created_at), { addSuffix: true })}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
              <div className="p-6 border-t border-gray-200">
                <Link
                  to="/questions"
                  className="text-primary-600 hover:text-primary-700 font-medium"
                >
                  View all questions →
                </Link>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Popular Tags */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Popular Tags</h3>
              <div className="flex flex-wrap gap-2">
                {popularTags.length === 0 ? (
                  <p className="text-gray-500 text-sm">No tags yet</p>
                ) : (
                  popularTags.map((tag) => (
                    <Link
                      key={tag}
                      to={`/questions?tags=${encodeURIComponent(tag)}`}
                      className="tag hover:bg-primary-200 transition-colors duration-200"
                    >
                      {tag}
                    </Link>
                  ))
                )}
              </div>
            </div>

            {/* Stats */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Platform Stats</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Questions</span>
                  <span className="font-semibold">{questions.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Active Users</span>
                  <span className="font-semibold">Growing</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Categories</span>
                  <span className="font-semibold">{popularTags.length}</span>
                </div>
              </div>
            </div>

            {/* Get Started */}
            <div className="bg-gradient-to-r from-primary-50 to-primary-100 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Get Started</h3>
              <p className="text-gray-600 text-sm mb-4">
                Join our community and start sharing knowledge today!
              </p>
              <Link
                to="/register"
                className="btn-primary w-full text-center"
              >
                Create Account
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home; 