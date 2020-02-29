# change into cmd dir
cd cmd/agent/

GOOS=darwin  GOARCH=amd64 go build -trimpath -o builds/darwin/i2bn .
GOOS=linux   GOARCH=amd64 go build -trimpath -o builds/linux/i2bn .
GOOS=windows GOARCH=amd64 go build -trimpath -o builds/windows/i2bn .

# upload to GCP
gsutil cp -r ./builds/* gs://i2bn

# make publicly accessibly
gsutil acl ch -u AllUsers:R gs://i2bn/darwin/i2bn
gsutil acl ch -u AllUsers:R gs://i2bn/linux/i2bn
gsutil acl ch -u AllUsers:R gs://i2bn/windows/i2bn

# verify(lol?) URLs work
curl --silent https://storage.googleapis.com/i2bn/darwin/i2bn  -o /dev/null && echo "darwin works"
curl --silent https://storage.googleapis.com/i2bn/linux/i2bn   -o /dev/null && echo "linux works"
curl --silent https://storage.googleapis.com/i2bn/windows/i2bn -o /dev/null && echo "windows works"

# go back to top dir
cd -