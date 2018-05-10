#parse('bash_header')

# Delete all untagged images
docker rmi -f $(docker images | grep "^<none>" | awk '{print $3}') 2>/dev/null

# Move to this directory
cd "$(dirname "$0")"

# Create docker image
build -t {docker_tag} .