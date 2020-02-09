trap "exit" INT

BLUE='\033[0;34m'
NC='\033[0m'

aws s3 rm --recursive s3://cs493-joneetha-music

printf "${BLUE}Bucket is empty after reset:${NC}\n"
aws s3 ls s3://cs493-joneetha-music
printf ""

printf "${BLUE}Uploading a song:${NC}\n"
python3 app.py upload_song cs493-joneetha-music deafheaven/sunbather/01_dream_house 01_dream_house sunbather deafheaven --profile=s3role
printf "${BLUE}Listing contents of album:${NC}\n"
aws s3 ls s3://cs493-joneetha-music/deafheaven/sunbather/ --profile=s3role
printf "${BLUE}Renaming the song:${NC}\n"
python3 app.py rename_song cs493-joneetha-music xXxDrEaM_HoUsExXx 01_dream_house sunbather deafheaven --profile=s3role
printf "${BLUE}Listing contents of album:${NC}\n"
aws s3 ls s3://cs493-joneetha-music/deafheaven/sunbather/ --profile=s3role
printf ""

printf "${BLUE}Uploading an album:${NC}\n"
python3 app.py upload_album cs493-joneetha-music deafheaven/sunbather sunbather deafheaven --profile=s3role
printf "${BLUE}Listing contents of album:${NC}\n"
aws s3 ls s3://cs493-joneetha-music/deafheaven/sunbather/ --profile=s3role
printf ""

printf "${BLUE}Uploading an artist:${NC}\n"
python3 app.py upload_artist cs493-joneetha-music have_a_nice_life have_a_nice_life --profile=s3role
printf "${BLUE}Listing albums by artist:${NC}\n"
aws s3 ls s3://cs493-joneetha-music/have_a_nice_life/ --profile=s3role
printf "${BLUE}Listing contents of album:${NC}\n"
aws s3 ls s3://cs493-joneetha-music/have_a_nice_life/deathconsciousness/ --profile=s3role
