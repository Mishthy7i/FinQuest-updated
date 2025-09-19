import 'package:flutter/material.dart';
import './pages/sign_up_page.dart';
import './pages//home_page.dart';
import './pages/sign_in_page.dart';
import './pages/splash_page.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final prefs = await SharedPreferences.getInstance();
  final token = prefs.getString('jwt_token');

  runApp(MyApp(isLoggedIn: token != null));
}

class MyApp extends StatelessWidget {
  final bool isLoggedIn;

  const MyApp({super.key, required this.isLoggedIn});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'FinQuest 💰',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: isLoggedIn ? const HomePage() : const OnboardingFlow(),
      routes: {
        '/splash': (context) => const OnboardingFlow(),
        '/home': (context) => const HomePage(),
        '/sign_in': (context) => const SignInPage(),
        '/sign_up': (context) => const SignUpPage(),
      },
    );
  }
}
