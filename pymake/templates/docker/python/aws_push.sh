#parse('bash_header')

echo "Logging to AWS..."
login_aws=$(aws ecr get-login --no-include-email --region eu-west-2)
login_aws_sudo=$(echo sudo $login_aws)

echo "..."
$login_aws_sudo

echo "Pushing..."
docker push {docker_tag}