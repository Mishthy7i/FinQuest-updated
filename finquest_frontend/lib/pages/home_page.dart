import 'package:flutter/material.dart';
import 'package:flutter_jwt/services/auth_service.dart';
import 'package:flutter_jwt/tabs/dashboard.dart';
import 'package:flutter_jwt/tabs/analytics.dart';
import 'package:flutter_jwt/tabs/leaderboard.dart';
import 'package:flutter_jwt/tabs/ledger.dart';
import 'package:flutter_jwt/pages/chatbot.dart'; // Import ChatbotPage

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _selectedIndex = 0;
  final AuthService _authService = AuthService();

  late final List<Widget> _pages;

  @override
  void initState() {
    super.initState();
    _pages = [
      const DashboardPage(),
      const Analytics(),
      const LeaderboardPage(),
      const LedgerPage(),
    ];
  }

  void _onTabTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBar(
        title: const Text("FinQuest"),
        centerTitle: true,
        elevation: 2,
        backgroundColor: const Color(0xFF4A90E2),
        foregroundColor: Colors.white,
        leading: IconButton(
          icon: const Icon(Icons.menu),
          onPressed: () => _scaffoldKey.currentState?.openDrawer(),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.smart_toy),
            onPressed: () {
              // Navigate to ChatbotPage
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const ChatbotPage()),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.notifications),
            onPressed: () {
              // Handle bell icon tap
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Notifications clicked')),
              );
            },
          ),
        ],
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(color: Color(0xFF4A90E2)),
              child: Text(
                'Welcome to FinQuest',
                style: TextStyle(color: Colors.white, fontSize: 20),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.settings),
              title: const Text('Settings'),
              onTap: () {
                Navigator.pop(context);
                // Handle settings tap
              },
            ),
            ListTile(
              leading: const Icon(Icons.info),
              title: const Text('About'),
              onTap: () {
                Navigator.pop(context);
                // Handle about tap
              },
            ),
            ListTile(
              leading: const Icon(Icons.logout),
              title: const Text('Logout'),
              onTap: () async {
                await _authService.logout();
                Navigator.pushReplacementNamed(context, '/splash');
              },
            ),
          ],
        ),
      ),
      body: _pages[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: _onTabTapped,
        type: BottomNavigationBarType.fixed,
        selectedItemColor: const Color(0xFF4A90E2),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: "Dashboard"),
          BottomNavigationBarItem(icon: Icon(Icons.event), label: "Analytics"),
          BottomNavigationBarItem(
            icon: Icon(Icons.emoji_events),
            label: "Leaderboard",
          ),
          BottomNavigationBarItem(icon: Icon(Icons.wallet), label: "Ledger"),
        ],
      ),
    );
  }
}
