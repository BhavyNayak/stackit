import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import RichTextEditor from '../components/RichTextEditor';
import apiService from '../services/api';
import toast from 'react-hot-toast';

const AskQuestion: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [tags, setTags] = useState<string[]>([]);
  const [tagInput, setTagInput] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isAuthenticated) {
    navigate('/login');
    return null;
  }

  const handleAddTag = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && tagInput.trim()) {
      e.preventDefault();
      const newTag = tagInput.trim().toLowerCase();
      if (!tags.includes(newTag) && tags.length < 5) {
        setTags([...tags, newTag]);
        setTagInput('');
      }
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!title.trim()) {
      toast.error('Please enter a title');
      return;
    }
    
    if (!description.trim()) {
      toast.error('Please enter a description');
      return;
    }
    
    if (tags.length === 0) {
      toast.error('Please add at least one tag');
      return;
    }

    try {
      setIsSubmitting(true);
      const response = await apiService.createQuestion({
        title: title.trim(),
        description: description.trim(),
        tags
      });

      if (response.data) {
        toast.success('Question posted successfully!');
        navigate(`/questions/${response.data.question_id}`);
      }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Failed to post question';
      toast.error(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Ask a Question</h1>
          <p className="mt-2 text-gray-600">
            Share your knowledge and help others learn
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Title */}
          <div className="card">
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
              Title *
            </label>
            <input
              type="text"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="What's your question? Be specific."
              className="input-field"
              maxLength={300}
            />
            <p className="mt-1 text-sm text-gray-500">
              {title.length}/300 characters
            </p>
          </div>

          {/* Description */}
          <div className="card">
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
              Description *
            </label>
            <RichTextEditor
              value={description}
              onChange={setDescription}
              placeholder="Provide all the information someone would need to answer your question..."
            />
            <p className="mt-2 text-sm text-gray-500">
              Use the toolbar to format your text, add links, images, and more.
            </p>
          </div>

          {/* Tags */}
          <div className="card">
            <label htmlFor="tags" className="block text-sm font-medium text-gray-700 mb-2">
              Tags *
            </label>
            <input
              type="text"
              id="tags"
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              onKeyDown={handleAddTag}
              placeholder="Add tags (press Enter to add, max 5 tags)"
              className="input-field"
              disabled={tags.length >= 5}
            />
            <p className="mt-1 text-sm text-gray-500">
              Add up to 5 tags to help categorize your question
            </p>
            
            {/* Tag Display */}
            {tags.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-2">
                {tags.map((tag) => (
                  <span
                    key={tag}
                    className="tag flex items-center space-x-1"
                  >
                    <span>{tag}</span>
                    <button
                      type="button"
                      onClick={() => handleRemoveTag(tag)}
                      className="ml-1 text-primary-600 hover:text-primary-800"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Guidelines */}
          <div className="card bg-blue-50 border-blue-200">
            <h3 className="text-lg font-semibold text-blue-900 mb-3">Writing a good question</h3>
            <ul className="space-y-2 text-sm text-blue-800">
              <li>• Be specific and provide enough context</li>
              <li>• Include relevant code examples if applicable</li>
              <li>• Explain what you've already tried</li>
              <li>• Use clear and descriptive language</li>
              <li>• Add appropriate tags to help others find your question</li>
            </ul>
          </div>

          {/* Submit Button */}
          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => navigate('/questions')}
              className="btn-secondary"
            >
              Cancel
            </button>
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
                'Post Question'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AskQuestion; 