"""AWS album upload thingy.

Usage:
  app.py upload_album <bucket_name> <path> <name>
  app.py upload_artist <bucket_name> <path> <name>

Options:
  -h --help  Show this screen.
"""

import boto3
from docopt import docopt
import os

bucket_name = None

def upload_song(artist_name, song_name, data):
  s3 = boto3.resource('s3')
  s3.Bucket(artist_name).put_object(Key=song_name, Body=data)

def upload_album(path, name):
  for song in os.listdir(path):
    song_path = path + '/' + song
    if os.path.isfile(song_path):
      print(f'found file {song}')
      with open(song_path, 'rb') as song_bytes:
        upload_song(
          artist_name=bucket_name,
          song_name=song,
          data=song_bytes.read())

def upload_artist(path, name):
  pass

def main():
  arguments = docopt(__doc__)
  print(arguments)
  bucket_name = arguments['<bucket_name>']
  if arguments['upload_album']:
    upload_album(arguments['<path>'], arguments['<name>'])
  elif arguments['upload_artist']:
    upload_artist(arguments['<path>'], arguments['<name>'])

if __name__ == '__main__':
  main()
