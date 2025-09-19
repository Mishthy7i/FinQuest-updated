import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class ProfileSetupPage extends StatefulWidget {
  final String jwtToken;

  const ProfileSetupPage({Key? key, required this.jwtToken}) : super(key: key);

  @override
  _ProfileSetupPageState createState() => _ProfileSetupPageState();
}

class _ProfileSetupPageState extends State<ProfileSetupPage> {
  final Map<String, TextEditingController> _controllers = {
    'Food': TextEditingController(),
    'Transport': TextEditingController(),
    'Entertainment': TextEditingController(),
    'Utilities': TextEditingController(),
  };

  bool _isLoading = false;
  String? _errorMessage;

  Future<void> _submitProfile() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final profileData = _controllers.map(
        (key, controller) =>
            MapEntry(key, double.tryParse(controller.text) ?? 0),
      );

      // Add salary to the profile data
      final salaryResponse = await http.get(
        Uri.parse('http://127.0.0.1:8000/profile/'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ${widget.jwtToken}',
        },
      );

      if (salaryResponse.statusCode == 200) {
        final salaryData = jsonDecode(salaryResponse.body);
        profileData['Income'] = salaryData['salary'] ?? 0;
      } else {
        setState(() {
          _errorMessage = 'Failed to fetch salary';
        });
        return;
      }

      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/profile/build'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ${widget.jwtToken}',
        },
        body: jsonEncode({'categories': profileData}),
      );

      if (response.statusCode != 200 && response.statusCode != 201) {
        final errorData = jsonDecode(response.body);
        setState(() {
          _errorMessage = errorData['message'] ?? 'Failed to submit profile';
        });
        return;
      }

      // Navigate to HomePage after successful profile submission
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => HomePage()),
      );
    } catch (e) {
      setState(() {
        _errorMessage = 'Network error. Please check your connection.';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Profile Setup')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            ..._controllers.entries.map(
              (entry) => TextField(
                controller: entry.value,
                decoration: InputDecoration(labelText: '${entry.key} Spending'),
                keyboardType: TextInputType.number,
              ),
            ),
            if (_errorMessage != null)
              Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: Text(
                  _errorMessage!,
                  style: TextStyle(color: Colors.red),
                ),
              ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _isLoading ? null : _submitProfile,
              child: _isLoading ? CircularProgressIndicator() : Text('Submit'),
            ),
          ],
        ),
      ),
    );
  }
}

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Home Page')),
      body: Center(child: Text('Welcome to the Home Page!')),
    );
  }
}
