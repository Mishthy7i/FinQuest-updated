import 'package:flutter/material.dart';
import '../services/transaction_service.dart';

class LedgerPage extends StatefulWidget {
  const LedgerPage({Key? key}) : super(key: key);

  void showAddTransactionModal(BuildContext context) {
    final ledgerState = context.findAncestorStateOfType<_LedgerPageState>();
    ledgerState?._showAddTransactionModal(context);
  }

  @override
  State<LedgerPage> createState() => _LedgerPageState();
}

class _LedgerPageState extends State<LedgerPage> {
  final TransactionService _transactionService = TransactionService();
  List<Map<String, dynamic>> _transactions = [];
  bool _isLoading = true;
  String _selectedFilter = 'This Month';

  @override
  void initState() {
    super.initState();
    _fetchTransactions();
  }

  Future<void> _fetchTransactions() async {
    try {
      final transactions = await _transactionService.fetchTransactions();
      setState(() {
        _transactions = transactions;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Failed to fetch transactions')),
      );
    }
  }

  Future<void> _addTransaction(Map<String, dynamic> transactionData) async {
    final success = await _transactionService.addTransaction(transactionData);
    if (success) {
      await _fetchTransactions();
      Navigator.pop(context);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Transaction added successfully!'),
          backgroundColor: Colors.green,
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Failed to add transaction')),
      );
    }
  }

  void _showAddTransactionModal(BuildContext context) {
    final _amountController = TextEditingController();
    final _categoryController = TextEditingController();
    final _modeController = TextEditingController();
    final _formKey = GlobalKey<FormState>();

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) {
        return AlertDialog(
          title: const Text("Add Transaction"),
          content: Form(
            key: _formKey,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextFormField(
                  controller: _amountController,
                  decoration: const InputDecoration(labelText: 'Amount'),
                  keyboardType: TextInputType.number,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter an amount';
                    }
                    if (double.tryParse(value) == null) {
                      return 'Please enter a valid number';
                    }
                    return null;
                  },
                ),
                TextFormField(
                  controller: _categoryController,
                  decoration: const InputDecoration(labelText: 'Category'),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter a category';
                    }
                    return null;
                  },
                ),
                TextFormField(
                  controller: _modeController,
                  decoration: const InputDecoration(labelText: 'Mode'),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter a mode';
                    }
                    return null;
                  },
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(ctx).pop(),
              child: const Text("Cancel"),
            ),
            ElevatedButton(
              onPressed: () async {
                if (_formKey.currentState!.validate()) {
                  final transactionData = {
                    'amount': double.tryParse(_amountController.text) ?? 0.0,
                    'category': _categoryController.text,
                    'mode': _modeController.text,
                  };
                  await _addTransaction(transactionData);
                }
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF4A90E2),
              ),
              child: const Text("Add"),
            ),
          ],
        );
      },
    );
  }

  List<Map<String, dynamic>> _getFilteredTransactions() {
    final now = DateTime.now();
    if (_selectedFilter == 'Today') {
      return _transactions.where((transaction) {
        final createdAt = DateTime.parse(transaction['created_at']);
        return createdAt.year == now.year &&
            createdAt.month == now.month &&
            createdAt.day == now.day;
      }).toList();
    } else if (_selectedFilter == 'Yesterday') {
      final yesterday = now.subtract(const Duration(days: 1));
      return _transactions.where((transaction) {
        final createdAt = DateTime.parse(transaction['created_at']);
        return createdAt.year == yesterday.year &&
            createdAt.month == yesterday.month &&
            createdAt.day == yesterday.day;
      }).toList();
    } else if (_selectedFilter == 'This Month') {
      return _transactions.where((transaction) {
        final createdAt = DateTime.parse(transaction['created_at']);
        return createdAt.year == now.year && createdAt.month == now.month;
      }).toList();
    }
    return _transactions;
  }

  @override
  Widget build(BuildContext context) {
    final filteredTransactions = _getFilteredTransactions();

    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "📊 Transaction Ledger",
            style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 20),
          DropdownButton<String>(
            value: _selectedFilter,
            items: const [
              DropdownMenuItem(value: 'Today', child: Text('Today')),
              DropdownMenuItem(value: 'Yesterday', child: Text('Yesterday')),
              DropdownMenuItem(value: 'This Month', child: Text('This Month')),
            ],
            onChanged: (value) {
              setState(() {
                _selectedFilter = value!;
              });
            },
          ),
          const SizedBox(height: 20),
          Expanded(
            child:
                _isLoading
                    ? const Center(child: CircularProgressIndicator())
                    : filteredTransactions.isEmpty
                    ? const Center(
                      child: Text(
                        'No transactions yet.\nTap + to add your first transaction!',
                        textAlign: TextAlign.center,
                        style: TextStyle(fontSize: 16, color: Colors.grey),
                      ),
                    )
                    : ListView.builder(
                      itemCount: filteredTransactions.length,
                      itemBuilder: (context, index) {
                        final transaction = filteredTransactions[index];
                        final isExpense = transaction['type'] == 'expense';
                        return Card(
                          child: ListTile(
                            leading: CircleAvatar(
                              backgroundColor:
                                  isExpense ? Colors.red : Colors.green,
                              child: Icon(
                                isExpense ? Icons.remove : Icons.add,
                                color: Colors.white,
                              ),
                            ),
                            title: Text(
                              '${transaction['category']} - ₹${transaction['amount']}',
                              style: const TextStyle(
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                            subtitle: Text('Mode: ${transaction['mode']}'),
                            trailing: Text(
                              transaction['created_at'] != null
                                  ? DateTime.parse(
                                    transaction['created_at'],
                                  ).toString().split(' ')[0]
                                  : 'Today',
                              style: const TextStyle(
                                fontSize: 12,
                                color: Colors.grey,
                              ),
                            ),
                          ),
                        );
                      },
                    ),
          ),
        ],
      ),
    );
  }
}
