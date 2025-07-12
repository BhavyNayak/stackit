import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { 
  User, 
  Question, 
  Answer, 
  Notification, 
  ApiResponse,
  LoginCredentials,
  RegisterCredentials,
  CreateQuestionData,
  CreateAnswerData,
  VoteData,
  SearchFilters
} from '../types';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: '/api',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor to handle errors
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(credentials: LoginCredentials): Promise<ApiResponse<{ user: User; token: string }>> {
    const response: AxiosResponse<ApiResponse<{ user: User; token: string }>> = await this.api.post('/users/login', credentials);
    return response.data;
  }

  async register(credentials: RegisterCredentials): Promise<ApiResponse<{ user: User; token: string }>> {
    const response: AxiosResponse<ApiResponse<{ user: User; token: string }>> = await this.api.post('/users/register', credentials);
    return response.data;
  }

  async getCurrentUser(): Promise<ApiResponse<User>> {
    const response: AxiosResponse<ApiResponse<User>> = await this.api.get('/users/me');
    return response.data;
  }

  // Question endpoints
  async getQuestions(filters?: SearchFilters): Promise<ApiResponse<Question[]>> {
    const params = new URLSearchParams();
    if (filters?.query) params.append('query', filters.query);
    if (filters?.tags) filters.tags.forEach(tag => params.append('tags', tag));
    if (filters?.sort) params.append('sort', filters.sort);
    if (filters?.page) params.append('page', filters.page.toString());
    if (filters?.limit) params.append('limit', filters.limit.toString());

    const response: AxiosResponse<ApiResponse<Question[]>> = await this.api.get(`/questions?${params.toString()}`);
    return response.data;
  }

  async getQuestion(id: string): Promise<ApiResponse<Question>> {
    const response: AxiosResponse<ApiResponse<Question>> = await this.api.get(`/questions/${id}`);
    return response.data;
  }

  async createQuestion(data: CreateQuestionData): Promise<ApiResponse<Question>> {
    const response: AxiosResponse<ApiResponse<Question>> = await this.api.post('/questions', data);
    return response.data;
  }

  async updateQuestion(id: string, data: Partial<CreateQuestionData>): Promise<ApiResponse<Question>> {
    const response: AxiosResponse<ApiResponse<Question>> = await this.api.put(`/questions/${id}`, data);
    return response.data;
  }

  async deleteQuestion(id: string): Promise<ApiResponse<null>> {
    const response: AxiosResponse<ApiResponse<null>> = await this.api.delete(`/questions/${id}`);
    return response.data;
  }

  // Answer endpoints
  async getAnswers(questionId: string): Promise<ApiResponse<Answer[]>> {
    const response: AxiosResponse<ApiResponse<Answer[]>> = await this.api.get(`/questions/${questionId}/answers`);
    return response.data;
  }

  async createAnswer(questionId: string, data: CreateAnswerData): Promise<ApiResponse<Answer>> {
    const response: AxiosResponse<ApiResponse<Answer>> = await this.api.post(`/questions/${questionId}/answers`, data);
    return response.data;
  }

  async updateAnswer(id: string, data: Partial<CreateAnswerData>): Promise<ApiResponse<Answer>> {
    const response: AxiosResponse<ApiResponse<Answer>> = await this.api.put(`/answers/${id}`, data);
    return response.data;
  }

  async deleteAnswer(id: string): Promise<ApiResponse<null>> {
    const response: AxiosResponse<ApiResponse<null>> = await this.api.delete(`/answers/${id}`);
    return response.data;
  }

  async acceptAnswer(id: string): Promise<ApiResponse<Answer>> {
    const response: AxiosResponse<ApiResponse<Answer>> = await this.api.patch(`/answers/${id}/accept`);
    return response.data;
  }

  // Voting endpoints
  async voteQuestion(id: string, voteData: VoteData): Promise<ApiResponse<Question>> {
    const response: AxiosResponse<ApiResponse<Question>> = await this.api.post(`/questions/${id}/vote`, voteData);
    return response.data;
  }

  async voteAnswer(id: string, voteData: VoteData): Promise<ApiResponse<Answer>> {
    const response: AxiosResponse<ApiResponse<Answer>> = await this.api.post(`/answers/${id}/vote`, voteData);
    return response.data;
  }

  // Notification endpoints
  async getNotifications(): Promise<ApiResponse<Notification[]>> {
    const response: AxiosResponse<ApiResponse<Notification[]>> = await this.api.get('/users/notifications');
    return response.data;
  }

  async markNotificationAsRead(id: string): Promise<ApiResponse<Notification>> {
    const response: AxiosResponse<ApiResponse<Notification>> = await this.api.patch(`/users/notifications/${id}/read`);
    return response.data;
  }

  async markAllNotificationsAsRead(): Promise<ApiResponse<null>> {
    const response: AxiosResponse<ApiResponse<null>> = await this.api.patch('/users/notifications/read-all');
    return response.data;
  }

  // Tags endpoints
  async getPopularTags(): Promise<ApiResponse<string[]>> {
    const response: AxiosResponse<ApiResponse<string[]>> = await this.api.get('/questions/tags/popular');
    return response.data;
  }

  // Search endpoints
  async searchQuestions(query: string): Promise<ApiResponse<Question[]>> {
    const response: AxiosResponse<ApiResponse<Question[]>> = await this.api.get(`/questions/search?q=${encodeURIComponent(query)}`);
    return response.data;
  }
}

export const apiService = new ApiService();
export default apiService; 