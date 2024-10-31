from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Routen

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Datenbankmodell
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200), nullable=False)
    album = db.Column(db.String(200), nullable=True)
    link = db.Column(db.String(300), nullable=False)
    cover = db.Column(db.String(300), nullable=True)
    added_by = db.Column(db.String(100), nullable=False)

# Datenbank initialisieren
with app.app_context():
    db.create_all()

# API-Routen
@app.route('/songs', methods=['POST'])
def add_song():
    data = request.get_json()
    new_song = Song(
        title=data['title'],
        artist=data['artist'],
        link=data['link'],
        cover=data.get('cover', '')
    )
    db.session.add(new_song)
    db.session.commit()
    return jsonify({
        'id': new_song.id,
        'title': new_song.title,
        'artist': new_song.artist,
        'link': new_song.link,
        'cover': new_song.cover
    }), 201

@app.route('/songs', methods=['GET'])
def get_songs():
    songs = Song.query.all()
    return jsonify([{
        'id': song.id,
        'title': song.title,
        'artist': song.artist,
        'link': song.link,
        'cover': song.cover
    } for song in songs])

@app.route('/songs/<int:id>', methods=['DELETE'])
def delete_song(id):
    song = Song.query.get(id)
    if song is None:
        return jsonify({'error': 'Song not found'}), 404
    db.session.delete(song)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25567, debug=True)