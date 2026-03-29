import 'package:flutter/material.dart';
import 'dart:html' as html;

void main() {
  runApp(const LMSAssistantApp());
}

class LMSAssistantApp extends StatelessWidget {
  const LMSAssistantApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LMS Assistant',
      theme: ThemeData(primarySwatch: Colors.green),
      home: const ChatScreen(),
    );
  }
}

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, String>> _messages = [];
  html.WebSocket? _socket;

  @override
  void initState() {
    super.initState();
    _connectWebSocket();
  }

  void _connectWebSocket() {
    final accessKey = html.window.localStorage['accessKey'] ?? 
        html.window.prompt('Enter access key:', 'nanobot-secret-2024');
    if (accessKey != null) {
      html.window.localStorage['accessKey'] = accessKey;
      _socket = html.WebSocket('ws://${html.window.location.host}/ws/chat?access_key=$accessKey');
      _socket!.onOpen = (_) {
        _addMessage('System', 'Connected', 'system');
      };
      _socket!.onMessage = (event) {
        final data = event.data as String;
        _addMessage('Agent', data, 'agent');
      };
      _socket!.onClose = (_) {
        _addMessage('System', 'Disconnected', 'system');
      };
    }
  }

  void _sendMessage() {
    final text = _controller.text.trim();
    if (text.isEmpty || _socket == null) return;
    _addMessage('You', text, 'user');
    _socket!.send('{"content": "$text"}');
    _controller.clear();
  }

  void _addMessage(String sender, String text, String type) {
    setState(() {
      _messages.add({'sender': sender, 'text': text, 'type': type});
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🤖 LMS Assistant')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(8),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                final isUser = msg['type'] == 'user';
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 4),
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(
                      color: isUser ? Colors.green[100] : Colors.grey[300],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(msg['sender']!,
                            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                        const SizedBox(height: 4),
                        Text(msg['text']!),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          Container(
            padding: const EdgeInsets.all(8),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      hintText: 'Type a message...',
                      border: OutlineInputBorder(borderRadius: BorderRadius.all(Radius.circular(24))),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  icon: const Icon(Icons.send),
                  onPressed: _sendMessage,
                  color: Colors.green,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
