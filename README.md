# velocity-gpt2-eks-example

## Train model in EC2

Create a gpu enabled EC2 instance. 
Train model with the steps outlined in [this Keras tutorial](https://keras.io/examples/generative/gpt2_text_generation_with_kerasnlp/)

Save the model with the Keras `model.save('<filename.keras>') method

Dockerize the model (see Dockerfile for example)
>**NOTE:** the tensorflow/tensorflow base image ships with Python3.8, which I updated to 3.10 for compatibility with FastAPI

Push to registry

## Deploy to EKS

Create an EKS cluster
Add a node group with GPU enabled
Deploy the Nvidia daemonset
Deploy the image built in the steps above
