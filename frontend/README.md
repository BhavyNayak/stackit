# StackIt Frontend

A modern, responsive React frontend for the StackIt Q&A platform. Built with TypeScript, Tailwind CSS, and React Router.

## Features

### 🎯 Core Features
- **User Authentication**: Login, register, and protected routes
- **Question Management**: Ask, view, edit, and delete questions
- **Answer System**: Post answers with rich text formatting
- **Voting System**: Upvote/downvote questions and answers
- **Tag System**: Categorize questions with tags
- **Search & Filter**: Find questions by title, tags, and content
- **Notifications**: Real-time notifications for answers and mentions

### 🎨 Rich Text Editor
- **Bold, Italic, Strikethrough** formatting
- **Numbered and bullet lists**
- **Emoji insertion**
- **Hyperlink insertion**
- **Image upload support**
- **Text alignment** (Left, Center, Right)

### 🔔 Notification System
- **Bell icon** in navigation with unread count
- **Real-time notifications** for:
  - New answers to your questions
  - Comments on your answers
  - Mentions using @username
- **Mark as read** functionality
- **Notification dropdown** with recent activity

### 🎨 Modern UI/UX
- **Responsive design** for all devices
- **Dark/light theme** support
- **Smooth animations** and transitions
- **Loading states** and error handling
- **Toast notifications** for user feedback

## Tech Stack

- **React 18** with TypeScript
- **React Router 6** for navigation
- **Tailwind CSS** for styling
- **React Quill** for rich text editing
- **Axios** for API communication
- **React Hot Toast** for notifications
- **Date-fns** for date formatting
- **Heroicons** for icons

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Backend API running on `http://localhost:8000`

### Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The build files will be created in the `build` directory.

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── NotificationDropdown.tsx
│   │   ├── ProtectedRoute.tsx
│   │   └── RichTextEditor.tsx
│   ├── contexts/
│   │   └── AuthContext.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   ├── Questions.tsx
│   │   ├── QuestionDetail.tsx
│   │   ├── AskQuestion.tsx
│   │   └── Profile.tsx
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   ├── index.tsx
│   └── index.css
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

## API Integration

The frontend communicates with the backend API through the `apiService` in `src/services/api.ts`. The service includes:

- **Authentication endpoints** (login, register, get current user)
- **Question endpoints** (CRUD operations, voting, search)
- **Answer endpoints** (CRUD operations, voting, accept)
- **Notification endpoints** (fetch, mark as read)
- **Tag endpoints** (popular tags)

## Key Components

### RichTextEditor
A custom component built with React Quill that provides:
- Full formatting toolbar
- Image upload support
- Emoji picker
- Link insertion
- Code highlighting

### NotificationDropdown
Real-time notification system with:
- Unread count badge
- Dropdown with recent notifications
- Mark as read functionality
- Different notification types (answer, comment, mention, vote)

### Header
Main navigation component with:
- Logo and branding
- Search functionality
- User menu
- Notification bell
- Responsive design

## Styling

The project uses Tailwind CSS with custom configuration:
- **Custom color palette** for primary, secondary, success, warning, and danger
- **Custom animations** for fade-in, slide-up, and bounce effects
- **Component classes** for buttons, inputs, cards, and tags
- **Responsive utilities** for mobile-first design

## State Management

The application uses React Context for state management:
- **AuthContext**: Manages user authentication state
- **Local state**: Component-level state for forms and UI
- **API state**: Server state managed through API calls

## Routing

Protected routes are implemented using:
- **ProtectedRoute component** for authentication checks
- **React Router 6** for navigation
- **Route guards** for admin-only pages

## Error Handling

Comprehensive error handling includes:
- **API error responses** with user-friendly messages
- **Network error handling** with retry mechanisms
- **Form validation** with real-time feedback
- **Loading states** for better UX

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 