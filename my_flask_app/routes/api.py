from flask import Blueprint, request, jsonify
from app import db
from models import MessageThread
import openai
import requests

api_bp = Blueprint('api', __name__)

openai.api_key = app.config['OPENAI_API_KEY']

@api_bp.route('/save_thread', methods=['POST'])
def save_thread():
    data = request.json
    thread = MessageThread(
        user_id=data['user_id'],
        chat_id=data['chatId'],
        query=data['query'],
        response=data['response'],
        timestamp=data['timestamp']
    )
    db.session.add(thread)
    db.session.commit()
    return jsonify({"status": "success"})

@api_bp.route('/get_threads', methods=['GET'])
def get_threads():
    user_id = request.args.get('user_id')
    threads = MessageThread.query.filter_by(user_id=user_id).all()
    result = [{
        "chatId": thread.chat_id,
        "query": thread.query,
        "response": thread.response,
        "timestamp": thread.timestamp
    } for thread in threads]
    return jsonify(result)

@api_bp.route('/get_analytics', methods=['POST'])
def get_analytics():
    data = request.json
    user_id = data['user_id']
    query = data['query']
    threads = MessageThread.query.filter_by(user_id=user_id).all()
    messages = [{
        "query": thread.query,
        "response": thread.response,
        "timestamp": thread.timestamp
    } for thread in threads]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Analyze the following customer interactions: {messages}. Answer the query: {query}",
        max_tokens=150
    )
    return jsonify({"response": response.choices[0].text})
