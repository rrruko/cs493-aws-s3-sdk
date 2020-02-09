aws s3 rm --recursive s3://cs493-joneetha-music

echo "Bucket is empty after reset:"
aws s3 ls s3://cs493-joneetha-music
echo

echo "Uploading a song:"
python3 app.py upload_song cs493-joneetha-music deafheaven/sunbather/01_dream_house 01_dream_house sunbather deafheaven --profile=s3role
echo "Listing contents of album:"
aws s3 ls s3://cs493-joneetha-music/deafheaven/sunbather/ --profile=s3role
echo

echo "Uploading an album:"
python3 app.py upload_album cs493-joneetha-music deafheaven/sunbather sunbather deafheaven --profile=s3role
echo "Listing contents of album:"
aws s3 ls s3://cs493-joneetha-music/deafheaven/sunbather/ --profile=s3role
echo

echo "Uploading an artist:"
python3 app.py upload_artist cs493-joneetha-music have_a_nice_life have_a_nice_life --profile=s3role
echo "Listing albums by artist:"
aws s3 ls s3://cs493-joneetha-music/have_a_nice_life/ --profile=s3role
echo "Listing contents of album:"
aws s3 ls s3://cs493-joneetha-music/have_a_nice_life/deathconsciousness/ --profile=s3role
