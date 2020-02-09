"""AWS album upload thingy.

Usage:
  app.py upload_song <bucket_name> <path> <song_name> <album_name> <artist_name>
  app.py upload_album <bucket_name> <path> <album_name> <artist_name>
  app.py upload_artist <bucket_name> <path> <name>

Options:
  -h --help  Show this screen.
"""

import boto3
from docopt import docopt
import os

class Logger():
  def __init__(self):
    self.indent_level = 0

  def log(self, msg):
    print(' ' * self.indent_level + msg)

  def indent(self):
    self.indent_level += 2

  def outdent(self):
    self.indent_level -= 2
    self.indent_level = max(self.indent_level, 0)

class App():
  def __init__(self, bucket_name):
    self.bucket_name = bucket_name
    self.logger = Logger()

  def upload_song(self, artist_name, album_name, song_name, song_path):
    with open(song_path, 'rb') as song_bytes:
      data = song_bytes.read()
      s3 = boto3.resource('s3')
      path = artist_name + '/' + album_name + '/' + song_name
      self.logger.log(f'uploading {song_name} at {path}')
      s3.Bucket(self.bucket_name).put_object(Key=path, Body=data)

  def upload_album(self, path, album_name, artist_name):
    self.logger.log(f'album: {album_name}')
    for song in os.listdir(path):
      self.logger.indent()
      song_path = path + '/' + song
      if os.path.isfile(song_path):
        self.upload_song(
          artist_name=artist_name,
          album_name=album_name,
          song_name=song,
          song_path=song_path)
      self.logger.outdent()

  def upload_artist(self, path, name):
    print(f'artist: {name}')
    for album in os.listdir(path):
      self.logger.indent()
      self.upload_album(path + '/' + album, album, name)
      self.logger.outdent()

def main():
  arguments = docopt(__doc__)
  print(arguments)
  app = App(arguments['<bucket_name>'])
  if arguments['upload_album']:
    app.upload_album(arguments['<path>'], arguments['<album_name>'], arguments['<artist_name>'])
  elif arguments['upload_artist']:
    app.upload_artist(arguments['<path>'], arguments['<name>'])
  elif arguments['upload_song']:
    app.upload_song(
      artist_name=arguments['<artist_name>'],
      album_name=arguments['<album_name>'],
      song_name=arguments['<song_name>'],
      song_path=arguments['<path>']
    )

if __name__ == '__main__':
  main()
