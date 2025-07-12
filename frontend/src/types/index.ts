export interface User {
  user_id: string;
  username: string;
  email: string;
  role: 'guest' | 'user' | 'admin';
  created_at: string;
}

export interface Question {
  question_id: string;
  user_id: string;
  title: string;
  description: string;
  created_at: string;
  updated_at?: string;
  author?: User;
  answers?: Answer[];
  tags?: string[];
  vote_count?: number;
  answer_count?: number;
}

export interface Answer {
  answer_id: string;
  question_id: string;
  user_id: string;
  content: string;
  is_accepted: boolean;
  created_at: string;
  author?: User;
  vote_count?: number;
}

export interface Notification {
  id: string;
  user_id: string;
  type: 'answer' | 'comment' | 'mention' | 'vote';
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
  related_id?: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface ApiResponse<T> {
  status: number;
  message: string;
  data: T | null;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  username: string;
  email: string;
  password: string;
}

export interface CreateQuestionData {
  title: string;
  description: string;
  tags: string[];
}

export interface CreateAnswerData {
  content: string;
}

export interface VoteData {
  vote_type: 'upvote' | 'downvote';
}

export interface SearchFilters {
  query?: string;
  tags?: string[];
  sort?: 'newest' | 'oldest' | 'most_voted' | 'most_answered';
  page?: number;
  limit?: number;
} 