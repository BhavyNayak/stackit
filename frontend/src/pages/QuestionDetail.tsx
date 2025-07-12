import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Question, Answer } from '../types';
import { useAuth } from '../contexts/AuthContext';
import RichTextEditor from '../components/RichTextEditor';
import apiService from '../services/api';
import { formatDistanceToNow } from 'date-fns';
import toast from 'react-hot-toast';
import { ChevronUpIcon, ChevronDownIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

const QuestionDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const [question, setQuestion] = useState<Question | null>(null);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [newAnswer, setNewAnswer] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchQuestionData = async () => {
    if (!id) return;
    
    try {
      setIsLoading(true);
      const [questionResponse, answersResponse] = await Promise.all([
        apiService.getQuestion(id),
        apiService.getAnswers(id)
      ]);

      if (questionResponse.data) {
        setQuestion(questionResponse.data);
      }
      if (answersResponse.data) {
        setAnswers(answersResponse.data);
      }
    } catch (error) {
      console.error('Failed to fetch question data:', error);
      toast.error('Failed to load question');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestionData();
  }, [id]);

  const handleVote = async (type: 'question' | 'answer', id: string, voteType: 'upvote' | 'downvote') => {
    if (!isAuthenticated) {
      toast.error('Please log in to vote');
      return;
    }

    try {
      if (type === 'question') {
        const response = await apiService.voteQuestion(id, { vote_type: voteType });
        if (response.data) {
          setQuestion(response.data);
        }
      } else {
        const response = await apiService.voteAnswer(id, { vote_type: voteType });
        if (response.data) {
          setAnswers(prev => prev.map(ans => 
            ans.answer_id === id ? response.data! : ans
          ));
        }
      }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Failed to vote';
      toast.error(message);
    }
  };

  const handleSubmitAnswer = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!newAnswer.trim()) {
      toast.error('Please enter an answer');
      return;
    }

    try {
      setIsSubmitting(true);
      const response = await apiService.createAnswer(id!, { content: newAnswer.trim() });
      if (response.data) {
        setAnswers([...answers, response.data]);
        setNewAnswer('');
        toast.success('Answer posted successfully!');
      }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Failed to post answer';
      toast.error(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleAcceptAnswer = async (answerId: string) => {
    try {
      const response = await apiService.acceptAnswer(answerId);
      if (response.data) {
        setAnswers(prev => prev.map(ans => ({
          ...ans,
          is_accepted: ans.answer_id === answerId
        })));
        toast.success('Answer accepted!');
      }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Failed to accept answer';
      toast.error(message);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    );
  }

  if (!question) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Question not found</h2>
          <button
            onClick={() => navigate('/questions')}
            className="btn-primary"
          >
            Back to Questions
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Question */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-8">
          <div className="p-6">
            <div className="flex items-start space-x-4">
              {/* Voting */}
              <div className="flex flex-col items-center space-y-2">
                <button
                  onClick={() => handleVote('question', question.question_id, 'upvote')}
                  className="vote-button"
                >
                  <ChevronUpIcon className="h-6 w-6" />
                </button>
                <span className="text-lg font-semibold text-gray-900">
                  {question.vote_count || 0}
                </span>
                <button
                  onClick={() => handleVote('question', question.question_id, 'downvote')}
                  className="vote-button"
                >
                  <ChevronDownIcon className="h-6 w-6" />
                </button>
              </div>

              {/* Question Content */}
              <div className="flex-1">
                <h1 className="text-2xl font-bold text-gray-900 mb-4">
                  {question.title}
                </h1>
                
                <div className="prose max-w-none mb-4">
                  <div dangerouslySetInnerHTML={{ __html: question.description }} />
                </div>

                <div className="flex flex-wrap gap-2 mb-4">
                  {question.tags?.map((tag) => (
                    <span key={tag} className="tag">
                      {tag}
                    </span>
                  ))}
                </div>

                <div className="flex items-center justify-between text-sm text-gray-500">
                  <div className="flex items-center space-x-4">
                    <span>Asked by {question.author?.username || 'Anonymous'}</span>
                    <span>{formatDistanceToNow(new Date(question.created_at), { addSuffix: true })}</span>
                  </div>
                  {question.user_id === user?.user_id && (
                    <div className="flex space-x-2">
                      <button className="text-primary-600 hover:text-primary-700">
                        Edit
                      </button>
                      <button className="text-danger-600 hover:text-danger-700">
                        Delete
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Answers */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            {answers.length} Answer{answers.length !== 1 ? 's' : ''}
          </h2>

          {answers.length === 0 ? (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
              <p className="text-gray-600 mb-4">No answers yet. Be the first to answer!</p>
            </div>
          ) : (
            <div className="space-y-6">
              {answers.map((answer) => (
                <div
                  key={answer.answer_id}
                  className={`bg-white rounded-lg shadow-sm border ${
                    answer.is_accepted ? 'border-success-300 bg-success-50' : 'border-gray-200'
                  }`}
                >
                  <div className="p-6">
                    <div className="flex items-start space-x-4">
                      {/* Voting */}
                      <div className="flex flex-col items-center space-y-2">
                        <button
                          onClick={() => handleVote('answer', answer.answer_id, 'upvote')}
                          className="vote-button"
                        >
                          <ChevronUpIcon className="h-6 w-6" />
                        </button>
                        <span className="text-lg font-semibold text-gray-900">
                          {answer.vote_count || 0}
                        </span>
                        <button
                          onClick={() => handleVote('answer', answer.answer_id, 'downvote')}
                          className="vote-button"
                        >
                          <ChevronDownIcon className="h-6 w-6" />
                        </button>
                        {answer.is_accepted && (
                          <CheckCircleIcon className="h-6 w-6 text-success-600" />
                        )}
                      </div>

                      {/* Answer Content */}
                      <div className="flex-1">
                        <div className="prose max-w-none mb-4">
                          <div dangerouslySetInnerHTML={{ __html: answer.content }} />
                        </div>

                        <div className="flex items-center justify-between text-sm text-gray-500">
                          <div className="flex items-center space-x-4">
                            <span>Answered by {answer.author?.username || 'Anonymous'}</span>
                            <span>{formatDistanceToNow(new Date(answer.created_at), { addSuffix: true })}</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            {question.user_id === user?.user_id && !answer.is_accepted && (
                              <button
                                onClick={() => handleAcceptAnswer(answer.answer_id)}
                                className="text-success-600 hover:text-success-700 font-medium"
                              >
                                Accept
                              </button>
                            )}
                            {answer.user_id === user?.user_id && (
                              <>
                                <button className="text-primary-600 hover:text-primary-700">
                                  Edit
                                </button>
                                <button className="text-danger-600 hover:text-danger-700">
                                  Delete
                                </button>
                              </>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Answer Form */}
        {isAuthenticated ? (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Your Answer</h3>
            <form onSubmit={handleSubmitAnswer}>
              <RichTextEditor
                value={newAnswer}
                onChange={setNewAnswer}
                placeholder="Write your answer here..."
              />
              <div className="mt-4 flex justify-end">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting ? (
                    <div className="flex items-center space-x-2">
                      <div className="spinner"></div>
                      <span>Posting...</span>
                    </div>
                  ) : (
                    'Post Answer'
                  )}
                </button>
              </div>
            </form>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center">
            <p className="text-gray-600 mb-4">
              Please log in to answer this question
            </p>
            <button
              onClick={() => navigate('/login')}
              className="btn-primary"
            >
              Sign In
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default QuestionDetail; 