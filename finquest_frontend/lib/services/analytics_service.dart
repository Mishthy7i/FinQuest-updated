import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class AnalyticsService {
  static const String _baseUrl = 'http://127.0.0.1:7001';

  Future<List<Map<String, dynamic>>> fetchGoals() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('jwt_token');

    final response = await http.get(
      Uri.parse('$_baseUrl/goals/'),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      return List<Map<String, dynamic>>.from(jsonDecode(response.body));
    }
    throw Exception('Failed to fetch goals');
  }

  Future<bool> createGoal(Map<String, dynamic> goalData) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('jwt_token');

    final response = await http.post(
      Uri.parse('$_baseUrl/goals/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode(goalData),
    );

    return response.statusCode == 200;
  }

  Future<bool> updateGoal(int goalId, Map<String, dynamic> goalData) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('jwt_token');

    // For status-only updates, we need to get the current goal first
    // since the backend expects both amount and status
    try {
      final goals = await fetchGoals();
      final currentGoal = goals.firstWhere((goal) => goal['id'] == goalId);
      
      final fullGoalData = {
        'amount': currentGoal['amount'],
        'status': goalData['status'] ?? currentGoal['status'],
        ...goalData,
      };

      final response = await http.put(
        Uri.parse('$_baseUrl/goals/$goalId'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: jsonEncode(fullGoalData),
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Error updating goal: $e');
      return false;
    }
  }

  Future<List<Map<String, dynamic>>> fetchAvailableBadges() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('jwt_token');

    final response = await http.get(
      Uri.parse('$_baseUrl/available_badges/'),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      return List<Map<String, dynamic>>.from(jsonDecode(response.body));
    }
    throw Exception('Failed to fetch available badges');
  }

  Future<List<Map<String, dynamic>>> fetchTransactionAnalytics() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('jwt_token');

    final response = await http.get(
      Uri.parse('$_baseUrl/transactions/'),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final transactions = List<Map<String, dynamic>>.from(
        jsonDecode(response.body),
      );

      // Process analytics data
      Map<String, double> categoryTotals = {};
      Map<String, int> categoryCounts = {};
      double totalExpenses = 0;
      double totalIncome = 0;

      for (var transaction in transactions) {
        final category = transaction['category'] as String;
        final amount = (transaction['amount'] as num).toDouble();
        final type = transaction['type'] as String;

        if (type == 'expense') {
          totalExpenses += amount;
          categoryTotals[category] = (categoryTotals[category] ?? 0) + amount;
          categoryCounts[category] = (categoryCounts[category] ?? 0) + 1;
        } else if (type == 'income') {
          totalIncome += amount;
        }
      }

      return [
        {
          'type': 'summary',
          'totalExpenses': totalExpenses,
          'totalIncome': totalIncome,
          'balance': totalIncome - totalExpenses,
          'transactionCount': transactions.length,
        },
        {
          'type': 'categoryBreakdown',
          'categoryTotals': categoryTotals,
          'categoryCounts': categoryCounts,
        },
      ];
    }
    throw Exception('Failed to fetch transaction analytics');
  }
}
