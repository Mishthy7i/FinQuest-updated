# Flutter JWT Authentication App

A simple Flutter app with JWT authentication for hackathon/demo purposes.

## Features

- Sign up with username, name, email, password, date of birth, and salary
- Sign in with email and password
- JWT token-based authentication
- Home page with transaction list
- Add transactions via floating action button modal
- Logout functionality
- Simple state management with Provider

## Screens

1. **Sign In Page** - Login with email/password, link to signup
2. **Sign Up Page** - Register new user, link to signin
3. **Splash Page** - Welcome screen for new users after first login
4. **Home Page** - Shows transaction list, add transaction FAB, logout

## API Integration

The app connects to a backend API at `http://localhost:8000` with these endpoints:

- `POST /auth/signup` - User registration
- `POST /auth/login` - User login (returns JWT token)
- `POST /transactions/add` - Add new transaction (requires JWT)
- `GET /transactions` - Get user transactions (requires JWT)

## Running the App

1. Make sure you have Flutter installed
2. Clone the project
3. Run `flutter pub get` to install dependencies
4. Start your backend API server on localhost:8000
5. Run `flutter run` to start the app

## Basic Architecture

- **Models**: Simple data classes for User and Transaction
- **Services**: ApiService handles all HTTP requests
- **Providers**: AuthProvider and TransactionProvider for state management
- **Screens**: Basic UI screens for signup, signin, splash, and home
- **Main**: App entry point with auth checking logic
