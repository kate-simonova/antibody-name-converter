# MabNameDecoder & MabNameDecoder

MabNameDecoder is a web-based tool that decodes antibody names and provides users with information about the classification and characteristics of the input antibody. This tool allows to generate a new antibody name or ,on the other hand, decode the name to find out about the source and use of the antibody. This tool is designed for researchers, healthcare professionals, and others interested in understanding antibody nomenclature and its implications.

List of commands to execute:

```
git clone git@github.com:kate-simonova/antibody-name-converter.git

cd antibody-name-converter

docker build -t mab .
docker run -h localhost -p 9002:9000 -d --name mab IMAGEID
```

