"""AWS album upload thingy.

Usage:
  app.py upload_song <bucket_name> <path> <song_name> <album_name> <artist_name> [--profile=<profile_name>]
  app.py rename_song <bucket_name> <new_name> <song_name> <album_name> <artist_name> [--profile=<profile_name>]
  app.py upload_album <bucket_name> <path> <album_name> <artist_name> [--profile=<profile_name>]
  app.py upload_artist <bucket_name> <path> <name> [--profile=<profile_name>] --genre=<genre_name>

Options:
  -h --help                 Show this screen.
  --profile=<profile_name>  Use a profile besides the default one.
  --genre=<genre_name>      Specify genre for an artist.
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
  def __init__(self, bucket_name, profile):
    self.bucket_name = bucket_name
    self.logger = Logger()
    if profile:
      self.profile = profile
    else:
      self.profile = 'default'
    session = boto3.Session(profile_name=self.profile)
    self.s3 = session.resource('s3')
    self.ddb = session.resource('dynamodb').Table('music')


  def upload_song(self, artist_name, album_name, song_name, song_path):
    with open(song_path, 'rb') as song_bytes:
      data = song_bytes.read()
      path = artist_name + '/' + album_name + '/' + song_name
      self.logger.log(f'uploading {song_name} at {path}')
      self.s3.Bucket(self.bucket_name).put_object(Key=path, Body=data)
      self.ddb.put_item(
        TableName='music',
        Item={
          'PK': album_name,
          'SK': song_name
        }
      )

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
    self.ddb.put_item(
      TableName='music',
      Item={
        'PK': artist_name,
        'SK': album_name
      }
    )

  def upload_artist(self, path, name, genre):
    print(f'artist: {name}')
    for album in os.listdir(path):
      self.logger.indent()
      self.upload_album(path + '/' + album, album, name)
      self.logger.outdent()
    self.ddb.put_item(
      TableName='music',
      Item={
        'PK': genre,
        'SK': name
      }
    )
    self.ddb.put_item(
      TableName='music',
      Item={
        'PK': 'genre',
        'SK': genre
      }
    )


  def rename_song(self, new_name, song_name, album_name, artist_name):
    path = artist_name + '/' + album_name + '/' + song_name
    new_path = artist_name + '/' + album_name + '/' + new_name
    source_obj = self.bucket_name + '/' + path
    print(source_obj)
    self.s3.Object(self.bucket_name, new_path).copy_from(CopySource=source_obj)
    self.s3.Object(self.bucket_name, path).delete()
    self.ddb.delete_item(
      TableName='music',
      Key={
        'PK': album_name,
        'SK': song_name
      }
    )
    self.ddb.put_item(
      TableName='music',
      Item={
        'PK': album_name,
        'SK': new_name
      }
    )

def main():
  arguments = docopt(__doc__)
  app = App(arguments['<bucket_name>'], arguments['--profile'])
  if arguments['upload_album']:
    app.upload_album(arguments['<path>'], arguments['<album_name>'], arguments['<artist_name>'])
  elif arguments['upload_artist']:
    app.upload_artist(arguments['<path>'], arguments['<name>'], arguments['--genre'])
  elif arguments['upload_song']:
    app.upload_song(
      artist_name=arguments['<artist_name>'],
      album_name=arguments['<album_name>'],
      song_name=arguments['<song_name>'],
      song_path=arguments['<path>']
    )
  elif arguments['rename_song']:
    app.rename_song(
      new_name=arguments['<new_name>'],
      song_name=arguments['<song_name>'],
      album_name=arguments['<album_name>'],
      artist_name=arguments['<artist_name>']
    )

if __name__ == '__main__':
  main()
