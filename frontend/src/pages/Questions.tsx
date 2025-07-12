import React, { useState, useEffect, useCallback } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { Question, SearchFilters } from '../types';
import apiService from '../services/api';
import { formatDistanceToNow } from 'date-fns';
import toast from 'react-hot-toast';

const Questions: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filters, setFilters] = useState<SearchFilters>({
    query: searchParams.get('q') || '',
    tags: searchParams.get('tags')?.split(',') || [],
    sort: (searchParams.get('sort') as SearchFilters['sort']) || 'newest',
  });

  const fetchQuestions = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await apiService.getQuestions(filters);
      if (response.data) {
        setQuestions(response.data);
      }
    } catch (error) {
      console.error('Failed to fetch questions:', error);
      toast.error('Failed to load questions');
    } finally {
      setIsLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchQuestions();
  }, [fetchQuestions]);

  const handleFilterChange = (key: string, value: string | string[]) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    
    // Update URL params
    const params = new URLSearchParams();
    if (newFilters.query) params.set('q', newFilters.query);
    if (newFilters.tags && newFilters.tags.length > 0) params.set('tags', newFilters.tags.join(','));
    if (newFilters.sort && newFilters.sort !== 'newest') params.set('sort', newFilters.sort);
    setSearchParams(params);
  };

  const handleTagClick = (tag: string) => {
    const currentTags = filters.tags || [];
    const newTags = currentTags.includes(tag) 
      ? currentTags.filter(t => t !== tag)
      : [...currentTags, tag];
    handleFilterChange('tags', newTags);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Questions</h1>
          <p className="mt-2 text-gray-600">
            Browse and search through all questions
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 sticky top-24">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Filters</h3>
              
              {/* Search */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Search
                </label>
                <input
                  type="text"
                  value={filters.query || ''}
                  onChange={(e) => handleFilterChange('query', e.target.value)}
                  placeholder="Search questions..."
                  className="input-field"
                />
              </div>

              {/* Sort */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sort by
                </label>
                <select
                  value={filters.sort || 'newest'}
                  onChange={(e) => {
                    const sortValue = e.target.value as SearchFilters['sort'];
                    if (sortValue) {
                      handleFilterChange('sort', sortValue);
                    }
                  }}
                  className="input-field"
                >
                  <option value="newest">Newest</option>
                  <option value="oldest">Oldest</option>
                  <option value="most_voted">Most Voted</option>
                  <option value="most_answered">Most Answered</option>
                </select>
              </div>

              {/* Active Tags */}
              {filters.tags && filters.tags.length > 0 && (
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Active Tags
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {filters.tags.map((tag) => (
                      <button
                        key={tag}
                        onClick={() => handleTagClick(tag)}
                        className="tag hover:bg-danger-100 hover:text-danger-800 transition-colors duration-200"
                      >
                        {tag} ×
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Clear Filters */}
              {((filters.query && filters.query.length > 0) || (filters.tags && filters.tags.length > 0) || (filters.sort && filters.sort !== 'newest')) && (
                <button
                  onClick={() => {
                    setFilters({ query: '', tags: [], sort: 'newest' });
                    setSearchParams({});
                  }}
                  className="w-full btn-secondary"
                >
                  Clear Filters
                </button>
              )}
            </div>
          </div>

          {/* Questions List */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200">
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-semibold text-gray-900">
                    {questions.length} Question{questions.length !== 1 ? 's' : ''}
                  </h2>
                  <Link
                    to="/ask"
                    className="btn-primary"
                  >
                    Ask Question
                  </Link>
                </div>
              </div>

              <div className="divide-y divide-gray-200">
                {questions.length === 0 ? (
                  <div className="p-8 text-center">
                    <div className="text-gray-400 text-6xl mb-4">?</div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No questions found</h3>
                    <p className="text-gray-600 mb-4">
                      {(filters.query && filters.query.length > 0) || (filters.tags && filters.tags.length > 0)
                        ? 'Try adjusting your search criteria'
                        : 'Be the first to ask a question!'
                      }
                    </p>
                    <Link
                      to="/ask"
                      className="btn-primary"
                    >
                      Ask Question
                    </Link>
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
                              <button
                                key={tag}
                                onClick={() => handleTagClick(tag)}
                                className="tag hover:bg-primary-200 transition-colors duration-200"
                              >
                                {tag}
                              </button>
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
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Questions; 