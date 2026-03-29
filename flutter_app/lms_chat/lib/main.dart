import 'package:flutter/material.dart';
import 'dart:html' as html;
import 'dart:convert';

void main() {
  runApp(LMSAssistantApp());
}

class LMSAssistantApp extends StatefulWidget {
  @override
  _LMSAssistantAppState createState() => _LMSAssistantAppState();
}

class _LMSAssistantAppState extends State<LMSAssistantApp> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, String>> _messages = [];
  html.WebSocket? _socket;
  bool _connected = false;

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
        setState(() => _connected = true);
        _addMessage('System', 'Connected to LMS Assistant', 'system');
      };
      _socket!.onMessage = (event) {
        final data = jsonDecode(event.data);
        _addMessage('Agent', data['content'] ?? data['message'] ?? data.toString(), 'agent');
      };
      _socket!.onClose = (_) {
        setState(() => _connected = false);
        _addMessage('System', 'Disconnected. Reconnecting...', 'system');
        Future.delayed(Duration(seconds: 3), _connectWebSocket);
      };
    }
  }

  void _sendMessage() {
    final text = _controller.text.trim();
    if (text.isEmpty || _socket == null || _socket!.readyState != html.WebSocket.OPEN) return;
    _addMessage('You', text, 'user');
    _socket!.send(jsonEncode({'content': text}));
    _controller.clear();
  }

  void _addMessage(String sender, String text, String type) {
    setState(() {
      _messages.add({'sender': sender, 'text': text, 'type': type});
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LMS Assistant',
      theme: ThemeData(primarySwatch: Colors.green),
      home: Scaffold(
        appBar: AppBar(title: Text('🤖 LMS Assistant')),
        body: Column(
          children: [
            Expanded(
              child: ListView.builder(
                padding: EdgeInsets.all(8),
                itemCount: _messages.length,
                itemBuilder: (context, index) {
                  final msg = _messages[index];
                  final isUser = msg['type'] == 'user';
                  return Align(
                    alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                    child: Container(
                      margin: EdgeInsets.symmetric(vertical: 4),
                      padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                      decoration: BoxDecoration(
                        color: isUser ? Colors.green[100] : Colors.grey[300],
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(msg['sender']!,
                              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                          SizedBox(height: 4),
                          Text(msg['text']!),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
            Container(
              padding: EdgeInsets.all(8),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      decoration: InputDecoration(
                        hintText: 'Type a message...',
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(24)),
                      ),
                      onSubmitted: (_) => _sendMessage(),
                    ),
                  ),
                  SizedBox(width: 8),
                  IconButton(
                    icon: Icon(Icons.send),
                    onPressed: _sendMessage,
                    color: Colors.green,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
