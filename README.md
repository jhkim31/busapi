# BusApi

## 1. clone this project

## 2. build dockerfile

`$ docker build .`

## 3. run docker container
`$ docker run -p {forwadingPort}:5000 -it {ImageId} bash `

## 4. run main.py
`$ docker attach {containerId} `
`{containerId}$ python main.py `
